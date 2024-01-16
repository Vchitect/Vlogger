import torch

torch.backends.cuda.matmul.allow_tf32 = True
torch.backends.cudnn.allow_tf32 = True
import os
import sys
try:
    import utils
    from diffusion import create_diffusion
except:
    sys.path.append(os.path.split(sys.path[0])[0])
    import utils
    from diffusion import create_diffusion
import argparse
import torchvision
from PIL import Image
from einops import rearrange
from models import get_models
from diffusers.models import AutoencoderKL
from models.clip import TextEmbedder
from omegaconf import OmegaConf
from pytorch_lightning import seed_everything
from utils import mask_generation_before
from diffusers.utils.import_utils import is_xformers_available
from transformers import CLIPVisionModelWithProjection, CLIPImageProcessor
from vlogger.videofusion import fusion
from vlogger.videocaption import captioning
from vlogger.videoaudio import make_audio, merge_video_audio, concatenate_videos
from vlogger.STEB.model_transform import ip_scale_set, ip_transform_model, tca_transform_model
from vlogger.planning_utils.gpt4_utils import (readscript, 
                                               readtimescript, 
                                               readprotagonistscript, 
                                               readreferencescript, 
                                               readzhscript)


def auto_inpainting(args, 
                    video_input, 
                    masked_video, 
                    mask, 
                    prompt, 
                    image, 
                    vae, 
                    text_encoder, 
                    image_encoder, 
                    diffusion, 
                    model, 
                    device,
                    ):
    image_prompt_embeds = None
    if prompt is None:
        prompt = ""
    if image is not None:
        clip_image = CLIPImageProcessor()(images=image, return_tensors="pt").pixel_values
        clip_image_embeds = image_encoder(clip_image.to(device)).image_embeds
        uncond_clip_image_embeds = torch.zeros_like(clip_image_embeds).to(device)
        image_prompt_embeds = torch.cat([clip_image_embeds, uncond_clip_image_embeds], dim=0)
        image_prompt_embeds = rearrange(image_prompt_embeds, '(b n) c -> b n c', b=2).contiguous()
        model = ip_scale_set(model, args.ref_cfg_scale)
        if args.use_fp16:
            image_prompt_embeds = image_prompt_embeds.to(dtype=torch.float16)
    b, f, c, h, w = video_input.shape
    latent_h = video_input.shape[-2] // 8
    latent_w = video_input.shape[-1] // 8

    if args.use_fp16:
        z = torch.randn(1, 4, 16, latent_h, latent_w, dtype=torch.float16, device=device) # b,c,f,h,w
        masked_video = masked_video.to(dtype=torch.float16)
        mask = mask.to(dtype=torch.float16)
    else:
        z = torch.randn(1, 4, 16, latent_h, latent_w, device=device) # b,c,f,h,w

    masked_video = rearrange(masked_video, 'b f c h w -> (b f) c h w').contiguous()
    masked_video = vae.encode(masked_video).latent_dist.sample().mul_(0.18215)
    masked_video = rearrange(masked_video, '(b f) c h w -> b c f h w', b=b).contiguous()
    mask = torch.nn.functional.interpolate(mask[:,:,0,:], size=(latent_h, latent_w)).unsqueeze(1)
    masked_video = torch.cat([masked_video] * 2)
    mask = torch.cat([mask] * 2)
    z = torch.cat([z] * 2)
    prompt_all = [prompt] + [args.negative_prompt]

    text_prompt = text_encoder(text_prompts=prompt_all, train=False)
    model_kwargs = dict(encoder_hidden_states=text_prompt, 
                        class_labels=None, 
                        cfg_scale=args.cfg_scale,
                        use_fp16=args.use_fp16,
                        ip_hidden_states=image_prompt_embeds)
    
    # Sample images:
    samples = diffusion.ddim_sample_loop(model.forward_with_cfg, 
                                         z.shape, 
                                         z, 
                                         clip_denoised=False, 
                                         model_kwargs=model_kwargs, 
                                         progress=True, 
                                         device=device,
                                         mask=mask, 
                                         x_start=masked_video, 
                                         use_concat=True,
                                         )
    samples, _ = samples.chunk(2, dim=0) # [1, 4, 16, 32, 32]
    if args.use_fp16:
        samples = samples.to(dtype=torch.float16)

    video_clip = samples[0].permute(1, 0, 2, 3).contiguous() # [16, 4, 32, 32]
    video_clip = vae.decode(video_clip / 0.18215).sample # [16, 3, 256, 256]
    return video_clip


def main(args):
    # Setup PyTorch:
    if args.seed:
        torch.manual_seed(args.seed)
    torch.set_grad_enabled(False)
    device = "cuda" if torch.cuda.is_available() else "cpu"
    seed_everything(args.seed)

    model = get_models(args).to(device)
    model = tca_transform_model(model).to(device)
    model = ip_transform_model(model).to(device)
    if args.enable_xformers_memory_efficient_attention:
        if is_xformers_available():
            model.enable_xformers_memory_efficient_attention()
        else:
            raise ValueError("xformers is not available. Make sure it is installed correctly")
    if args.use_compile:
        model = torch.compile(model)

    ckpt_path = args.ckpt 
    state_dict = torch.load(ckpt_path, map_location=lambda storage, loc: storage)['ema']
    model_dict = model.state_dict()
    pretrained_dict = {}
    for k, v in state_dict.items():
        if k in model_dict:
            pretrained_dict[k] = v
    model_dict.update(pretrained_dict)
    model.load_state_dict(model_dict)

    model.eval()  # important!
    diffusion = create_diffusion(str(args.num_sampling_steps))
    vae = AutoencoderKL.from_pretrained(args.pretrained_model_path, subfolder="vae").to(device)
    text_encoder = text_encoder = TextEmbedder(args.pretrained_model_path).to(device)
    image_encoder = CLIPVisionModelWithProjection.from_pretrained(args.image_encoder_path).to(device)
    if args.use_fp16:
        print('Warnning: using half percision for inferencing!')
        vae.to(dtype=torch.float16)
        model.to(dtype=torch.float16)
        text_encoder.to(dtype=torch.float16)
    print("model ready!\n", flush=True)
    
    
    # load protagonist script
    character_places = readprotagonistscript(args.protagonist_file_path)
    print("protagonists ready!", flush=True)

    # load script
    video_list = readscript(args.script_file_path)
    print("video script ready!", flush=True)
    
    # load reference script
    reference_lists = readreferencescript(video_list, character_places, args.reference_file_path)
    print("reference script ready!", flush=True)
    
    # load zh script
    zh_video_list = readzhscript(args.zh_script_file_path)
    print("zh script ready!", flush=True)
    
    # load time script
    key_list = []
    for key, value in character_places.items():
        key_list.append(key)
    time_list = readtimescript(args.time_file_path)
    print("time script ready!", flush=True)
    

    # generation begin
    sample_list = []
    for i, text_prompt in enumerate(video_list):
        sample_list.append([])
        for time in range(time_list[i]):
            if time == 0:
                print('Generating the ({}) prompt'.format(text_prompt), flush=True)
                if reference_lists[i][0] == 0 or reference_lists[i][0] > len(key_list):
                    pil_image = None
                else:
                    pil_image = Image.open(args.reference_image_path[reference_lists[i][0] - 1])
                    pil_image.resize((256, 256))
                video_input = torch.zeros([1, 16, 3, args.image_size[0], args.image_size[1]]).to(device)
                mask = mask_generation_before("first0", video_input.shape, video_input.dtype, device) # b,f,c,h,w
                masked_video = video_input * (mask == 0)
                samples = auto_inpainting(args, 
                                          video_input, 
                                          masked_video, 
                                          mask, 
                                          text_prompt, 
                                          pil_image, 
                                          vae, 
                                          text_encoder, 
                                          image_encoder, 
                                          diffusion, 
                                          model, 
                                          device,
                                          )
                sample_list[i].append(samples)
            else:
                if sum(video.shape[0] for video in sample_list[i]) / args.fps >= time_list[i]:
                    break
                print('Generating the ({}) prompt'.format(text_prompt), flush=True)
                if reference_lists[i][0] == 0 or reference_lists[i][0] > len(key_list):
                    pil_image = None
                else:
                    pil_image = Image.open(args.reference_image_path[reference_lists[i][0] - 1])
                    pil_image.resize((256, 256))
                pre_video = sample_list[i][-1][-args.researve_frame:]
                f, c, h, w = pre_video.shape
                lat_video = torch.zeros(args.num_frames - args.researve_frame, c, h, w).to(device)
                video_input = torch.concat([pre_video, lat_video], dim=0)
                video_input = video_input.to(device).unsqueeze(0)
                mask = mask_generation_before(args.mask_type, video_input.shape, video_input.dtype, device)
                masked_video = video_input * (mask == 0)
                video_clip = auto_inpainting(args, 
                                             video_input, 
                                             masked_video, 
                                             mask, 
                                             text_prompt, 
                                             pil_image, 
                                             vae, 
                                             text_encoder, 
                                             image_encoder, 
                                             diffusion, 
                                             model, 
                                             device,
                                             )
                sample_list[i].append(video_clip[args.researve_frame:])
                print(video_clip[args.researve_frame:].shape)

        # transition
        if args.video_transition and i != 0:
            video_1 = sample_list[i - 1][-1][-1:]
            video_2 = sample_list[i][0][:1]
            f, c, h, w = video_1.shape
            video_middle = torch.zeros(args.num_frames - 2, c, h, w).to(device)
            video_input = torch.concat([video_1, video_middle, video_2], dim=0)
            video_input = video_input.to(device).unsqueeze(0)
            mask = mask_generation_before("onelast1", video_input.shape, video_input.dtype, device)
            masked_video = masked_video = video_input * (mask == 0)
            video_clip = auto_inpainting(args, 
                                         video_input, 
                                         masked_video, 
                                         mask, 
                                         "smooth transition, slow motion, slow changing.", 
                                         pil_image, 
                                         vae, 
                                         text_encoder, 
                                         image_encoder, 
                                         diffusion, 
                                         model, 
                                         device,
                                         )
            sample_list[i].insert(0, video_clip[1:-1])

        # save videos
        samples = torch.concat(sample_list[i], dim=0)
        samples = samples[0: time_list[i] * args.fps]
        if not os.path.exists(args.save_origin_video_path):
            os.makedirs(args.save_origin_video_path)
        video_ = ((samples * 0.5 + 0.5) * 255).add_(0.5).clamp_(0, 255).to(dtype=torch.uint8).cpu().permute(0, 2, 3, 1).contiguous()
        torchvision.io.write_video(args.save_origin_video_path + "/" + f"{i}" + '.mp4', video_, fps=args.fps)
    
    # post processing
    fusion(args.save_origin_video_path)
    captioning(args.script_file_path, args.zh_script_file_path, args.save_origin_video_path, args.save_caption_video_path)
    fusion(args.save_caption_video_path)
    make_audio(args.script_file_path, args.save_audio_path)
    merge_video_audio(args.save_caption_video_path, args.save_audio_path, args.save_audio_caption_video_path)
    concatenate_videos(args.save_audio_caption_video_path)
    print('final video save path {}'.format(args.save_audio_caption_video_path))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="./configs/vlog_read_script_sample.yaml")
    args = parser.parse_args()
    omega_conf = OmegaConf.load(args.config)
    save_path = omega_conf.save_path
    save_origin_video_path = os.path.join(save_path, "origin_video")
    save_caption_video_path = os.path.join(save_path.rsplit('/', 1)[0], "caption_video")
    save_audio_path = os.path.join(save_path.rsplit('/', 1)[0], "audio")
    save_audio_caption_video_path = os.path.join(save_path.rsplit('/', 1)[0], "audio_caption_video")
    if omega_conf.sample_num is not None:
        for i in range(omega_conf.sample_num):
            omega_conf.save_origin_video_path = save_path + f'-{i}'
            omega_conf.save_caption_video_path = save_caption_video_path + f'-{i}'
            omega_conf.save_audio_path = save_audio_path + f'-{i}'
            omega_conf.save_audio_caption_video_path = save_audio_caption_video_path + f'-{i}'
            omega_conf.seed += i
            main(omega_conf)
    else:
        omega_conf.save_origin_video_path = save_path
        omega_conf.save_caption_video_path = save_caption_video_path
        omega_conf.save_audio_path = save_audio_path
        omega_conf.save_audio_caption_video_path = save_audio_caption_video_path
        main(omega_conf)
