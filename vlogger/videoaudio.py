import os
import ast
from IPython.display import Audio
import nltk  # we'll use this to split into sentences
import numpy as np

from bark import generate_audio, SAMPLE_RATE
from moviepy.editor import concatenate_videoclips, concatenate_audioclips
from moviepy.editor import VideoFileClip, AudioFileClip, AudioClip, CompositeAudioClip
import librosa
import soundfile as sf
import math


def make_audio(en_prompt_file, output_dir):
    print("Begin to make the aside!")
    prompt_list = []
    with open(en_prompt_file, 'r', encoding='utf-8') as f:
        video_prompts = f.read()
        video_fragments = ast.literal_eval(video_prompts)
        for video_fragment in video_fragments:
            prompt_list.append(video_fragment["video fragment description"])

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    for i, prompt in enumerate(prompt_list):
        sentences = nltk.sent_tokenize(prompt)
        SPEAKER = "v2/en_speaker_1"
        silence = np.zeros(int(0.25 * SAMPLE_RATE))  # quarter second of silence

        pieces = []
        for sentence in sentences:
            audio_array = generate_audio(sentence, history_prompt=SPEAKER)
            # audio_array = generate_audio(sentence)
            pieces += [audio_array, silence.copy()]
        audio = Audio(np.concatenate(pieces), rate=SAMPLE_RATE)
        with open(os.path.join(output_dir, str(i) + ".wav"), 'w+b') as f:
            f.write(audio.data)


def merge_video_audio(video_dir, audio_dir, output_dir):
    video_fnames = []
    for fname in os.listdir(video_dir):
        if not fname.startswith("result"):
            video_fnames.append(fname)
    audio_fnames = []
    for fname in os.listdir(audio_dir):
        if not fname.startswith("result") and not fname.startswith("fast"):
            audio_fnames.append(fname)
    video_fnames.sort(key=lambda x: int(x.split('.')[0]))
    audio_fnames.sort(key=lambda x: int(x.split('.')[0]))
    assert len(video_fnames) == len(audio_fnames), 'The number of videos is not equal to audios.'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    audios = []
    for i, (video_fname, audio_fname) in enumerate(zip(video_fnames, audio_fnames)):
        video = VideoFileClip(os.path.join(video_dir, video_fname))
        audio = AudioFileClip(os.path.join(audio_dir, audio_fname))

        video_duration = video.duration
        audio_duration = audio.duration
        if audio_duration > video_duration:
            y, sr = librosa.load(os.path.join(audio_dir, audio_fname))
            speed_change = audio_duration / video_duration
            y_stretched = librosa.effects.time_stretch(y, rate=speed_change)
            sf.write(os.path.join(audio_dir, "fast_video.wav"), y_stretched, sr)
            audio = AudioFileClip(os.path.join(audio_dir, "fast_video.wav"))
        else:
            silence_len = math.ceil(video_duration * audio.fps) / audio.fps  # make sure the silence duration not less than required
            silence = AudioClip(lambda t: [0] * audio.nchannels, duration=silence_len, fps=audio.fps)
            audio = CompositeAudioClip([audio, silence])
        
        audios.append(audio)
        video = video.set_audio(audio)
        video.write_videofile(os.path.join(output_dir, str(i) + ".mp4"))
    final_audio = concatenate_audioclips(audios)
    final_audio.write_audiofile(os.path.join(audio_dir, "result" + ".wav"))



def concatenate_videos(video_dir, output_dir=None):
    if output_dir is None:
        output_dir = video_dir
    video_fnames = []
    for fname in os.listdir(video_dir):
        if not fname.startswith("result") and not fname.startswith("audio"):
            video_fnames.append(fname)
    video_fnames.sort(key=lambda x: int(x.split('.')[0]))
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    video_clips = [VideoFileClip(os.path.join(video_dir, video_fname)) for video_fname in video_fnames]
    audio_clips = [video.audio for video in video_clips]

    final_video = concatenate_videoclips(video_clips, method="compose")
    final_audio = concatenate_audioclips(audio_clips)

    final_clip = final_video.set_audio(final_audio)
    final_clip.write_videofile(os.path.join(output_dir, "result.mp4"))
