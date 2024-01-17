import torch
import os
os.environ['CURL_CA_BUNDLE'] = ''
import argparse
from omegaconf import OmegaConf
from diffusers import DiffusionPipeline
from vlogger.planning_utils.gpt4_utils import (ExtractProtagonist,
                                               ExtractAProtagonist,
                                               split_story,
                                               patch_story_scripts,
                                               refine_story_scripts,
                                               protagonist_place_reference1,
                                               translate_video_script,
                                               time_scripts,
                                               )


def main(args):
    story_path = args.story_path
    save_script_path = os.path.join(story_path.rsplit('/', 1)[0], "script")
    if not os.path.exists(save_script_path):
            os.makedirs(save_script_path)
    with open(story_path, "r") as story_file:
        story = story_file.read()
        
    # summerize protagonists and places
    protagonists_places_file_path = os.path.join(save_script_path, "protagonists_places.txt")
    if args.only_one_protagonist:
        character_places = ExtractAProtagonist(story, protagonists_places_file_path)
    else:
        character_places = ExtractProtagonist(story, protagonists_places_file_path)
    print("Protagonists and places OK", flush=True)
    
    # make script
    script_file_path = os.path.join(save_script_path, "video_prompts.txt")
    video_list = split_story(story, script_file_path)
    video_list = patch_story_scripts(story, video_list, script_file_path)
    video_list = refine_story_scripts(video_list, script_file_path)
    print("Scripts OK", flush=True)
    
    # think about the protagonist in each scene
    reference_file_path = os.path.join(save_script_path, "protagonist_place_reference.txt")
    reference_lists = protagonist_place_reference1(video_list, character_places, reference_file_path)
    print("Reference protagonist OK", flush=True)
    
    # translate the English script to Chinese
    zh_file_path = os.path.join(save_script_path, "zh_video_prompts.txt")
    zh_video_list = translate_video_script(video_list, zh_file_path)
    print("Translation OK", flush=True)
    
    # schedule the time of script
    time_file_path = os.path.join(save_script_path, "time_scripts.txt")
    time_list = time_scripts(video_list, time_file_path)
    print("Time script OK", flush=True)
    
    # make reference image
    base = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-base-1.0", 
                                             torch_dtype=torch.float16, 
                                             variant="fp16", 
                                             use_safetensors=True,
                                             ).to("cuda")
    refiner = DiffusionPipeline.from_pretrained("stabilityai/stable-diffusion-xl-refiner-1.0",
                                                text_encoder_2=base.text_encoder_2,
                                                vae=base.vae,
                                                torch_dtype=torch.float16,
                                                use_safetensors=True,
                                                variant="fp16",
                                                ).to("cuda")
    ref_dir_path = os.path.join(story_path.rsplit('/', 1)[0], "ref_img")
    if not os.path.exists(ref_dir_path):
            os.makedirs(ref_dir_path)
    for key, value in character_places.items():
        prompt = key + ", " + value
        img_path = os.path.join(ref_dir_path, key + ".jpg")
        image = base(prompt=prompt, 
                     output_type="latent", 
                     height=1024, 
                     width=1024, 
                     guidance_scale=7
                     ).images[0]
        image = refiner(prompt=prompt, image=image[None, :]).images[0]
        image.save(img_path)
    print("Reference image OK", flush=True)
    

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, default="configs/vlog_write_script.yaml")
    args = parser.parse_args()
    omega_conf = OmegaConf.load(args.config)
    main(omega_conf)
