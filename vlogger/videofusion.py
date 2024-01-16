import torch
import os
from decord import VideoReader, cpu
import numpy as np
import torchvision


def fusion(path):
    fnames = []
    for fname in os.listdir(path):
        if not fname.startswith("result"):
            fnames.append(fname)
    fnames.sort(key=lambda x: int(x.split('.')[0]))
    for i, fname in enumerate(fnames):
        fpath = os.path.join(path, fname)
        video = VideoReader(fpath, ctx=cpu(0))
        video = video[:].asnumpy()
        if i == 0:
            result = video
        else:
            result = np.concatenate((result, video), axis=0)
    torchvision.io.write_video(path + "/" + "result" + '.mp4', result, fps=8)

