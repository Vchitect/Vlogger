import torch
import ast
import os
import cv2 as cv
from PIL import Image, ImageDraw, ImageFont
from decord import VideoReader, cpu
import torchvision
import numpy as np


def captioning(en_prompt_file, zh_prompt_file, input_video_dir, output_video_dir):
    prompt_list = []
    with open(en_prompt_file, 'r', encoding='utf-8') as f:
        video_prompts = f.read()
        video_fragments = ast.literal_eval(video_prompts)
        for video_fragment in video_fragments:
            prompt_list.append(video_fragment["video fragment description"])
            
    video_fnames = []
    for fname in os.listdir(input_video_dir):
        try:
            int(fname.split('.')[0])
            video_fnames.append(fname)
        except:
            continue
    video_fnames.sort(key=lambda x: int(x.split('.')[0]))

    font_face = cv.FONT_HERSHEY_COMPLEX
    if not os.path.exists(output_video_dir):
        os.makedirs(output_video_dir)
    for i in range(len(video_fnames)):
        font_zh = ImageFont.truetype(font='MSYH.TTC', size=18)
        fontScale = 0.4
        video_path = os.path.join(input_video_dir, video_fnames[i])
        video = VideoReader(video_path, ctx=cpu(0))
        video = video[:].asnumpy()
        (fw, fh), bh = cv.getTextSize(prompt_list[i], font_face, fontScale, 1)
        pos_en = (int((video[0].shape[1] - fw) / 2), 300)
        if pos_en[0] < 0:
            scale = video[0].shape[1] / fw
            fontScale *= scale
            pos_en = (0, 300)
        for j in range(video.shape[0]):
            cv.putText(video[j], prompt_list[i], pos_en, font_face, fontScale, (255, 255, 255), 1, cv.LINE_AA)
            img = Image.fromarray(cv.cvtColor(video[j], cv.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(img)
            img = np.array(img)
            video[j] = cv.cvtColor(img, cv.COLOR_RGB2BGR)
        torchvision.io.write_video(output_video_dir + "/" + str(i) + '.mp4', video, fps=8)
    print("Caption OK", flush=True)

