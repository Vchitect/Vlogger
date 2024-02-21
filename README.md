<div align="center">

<a href="https://arxiv.org/abs/2401.09414">
<img width="743" alt="image" src="https://github.com/zhuangshaobin/Vlogger/assets/24236723/2885982e-5b18-48b3-97b1-966298329350">
</a>

[Shaobin Zhuang](https://github.com/zhuangshaobin), [Kunchang Li](https://scholar.google.com/citations?user=D4tLSbsAAAAJ), [Xinyuan Chen†](https://scholar.google.com/citations?user=3fWSC8YAAAAJ), [Yaohui Wang†](https://scholar.google.com/citations?user=R7LyAb4AAAAJ), [Ziwei Liu](https://scholar.google.com/citations?user=lc45xlcAAAAJ), [Yu Qiao](https://scholar.google.com/citations?user=gFtI-8QAAAAJ&hl), [Yali Wang†](https://scholar.google.com/citations?user=hD948dkAAAAJ)

[![arXiv](https://img.shields.io/badge/arXiv-2401.09414-b31b1b.svg)](https://arxiv.org/abs/2401.09414)
[![Project Page](https://img.shields.io/badge/Vlogger-Website-green)](https://zhuangshaobin.github.io/Vlogger.github.io/)
[![Hugging Face Model](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Models-yellow)](https://huggingface.co/GrayShine/Vlogger)
[![Hugging Face Space](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-yellow)](https://huggingface.co/spaces/GrayShine/Vlogger-ShowMaker)
[![YouTube Video](https://img.shields.io/badge/YouTube-Video-red)](https://youtu.be/ZRD1-jHbEGk)
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fzhuangshaobin%2FVlogger&count_bg=%23F59352&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=visitors&edge_flat=false)](https://hits.seeyoufarm.com)
</div>
</div>


In this work, we present **Vlogger**, a generic AI system for generating a **minute**-level video blog (i.e., vlog) of user descriptions. Different from short videos with a few seconds, vlog often contains a complex storyline with diversified scenes, which is challenging for most existing video generation approaches. To break through this bottleneck, our Vlogger smartly leverages Large Language Model (LLM) as Director and decomposes a long video generation task of vlog into four key stages, where we invoke various foundation models to play the critical roles of vlog professionals, including (1) Script, (2) Actor, (3) ShowMaker, and (4) Voicer. With such a design of mimicking human beings, our Vlogger can generate vlogs through explainable cooperation of top-down planning and bottom-up shooting. Moreover, we introduce a novel video diffusion model, **ShowMaker**, which serves as a videographer in our Vlogger for generating the video snippet of each shooting scene. By incorporating Script and Actor attentively as textual and visual prompts, it can effectively enhance spatial-temporal coherence in the snippet. Besides, we design a concise mixed training paradigm for ShowMaker, boosting its capacity for both T2V generation and prediction. Finally, the extensive experiments show that our method achieves state-of-the-art performance on zero-shot T2V generation and prediction tasks. More importantly, Vlogger can generate over 5-minute vlogs from open-world descriptions, without loss of video coherence on script and actor.


<div align="center">
<video src="https://github.com/zhuangshaobin/Vlogger/assets/94739615/1e8dd246-d3b9-49e9-8eee-d40b6d8523b9" controls="controls" width="500" height="300"></video>
<b>A compressed version of generated <a href="https://youtu.be/ZRD1-jHbEGk">Teddy Travel</a>.</b>
</div>

## Usage

<details>
  <summary><h3>Setup</h3></summary>

<h4>Prepare Environment</h4>

```bash
conda create -n vlogger python==3.10.11
conda activate vlogger
pip install -r requirements.txt
```

<h4>Download our model and T2I base model</h4>

Our model is based on Stable diffusion v1.4, you may download [Stable Diffusion v1-4](https://huggingface.co/CompVis/stable-diffusion-v1-4) and [OpenCLIP-ViT-H-14](https://huggingface.co/laion/CLIP-ViT-H-14-laion2B-s32B-b79K) to the director of ``` pretrained ```
.
Download our model(ShowMaker) checkpoint (from [google drive](https://drive.google.com/file/d/1pAH73kz2QRfD2Dxk4lL3SrHvLAlWcPI3/view?usp=drive_link) or [hugging face](https://huggingface.co/GrayShine/Vlogger/tree/main)) and save to the directory of ```pretrained```


Now under `./pretrained`, you should be able to see the following:
```
├── pretrained
│   ├── ShowMaker.pt
│   ├── stable-diffusion-v1-4
│   ├── OpenCLIP-ViT-H-14
│   │   ├── ...
└── └── ├── ...
        ├── ...
```

</details>


<details>
  <summary><h3>Inference for LLM planning and make reference image</h3></summary>
        
Run the following command to get script, actors and protagonist:

```python
python sample_scripts/vlog_write_script.py
```

- The generated scripts will be saved in ```results/vlog/$your_story_dir/script```.

- The generated reference images will be saved in ```results/vlog/$your_story_dir/img```.

- :warning: Enter your openai key in the 7th line of the file ```vlogger/planning_utils/gpt4_utils.py```
</details>

<details>
  <summary><h3>Inference for vlog generation</h3></summary>
        
Run the following command to get the vlog:

```python
python sample_scripts/vlog_read_script_sample.py
```

- The generated scripts will be saved in ```results/vlog/$your_story_dir/video```.
</details>

<details>
  <summary><h3>Inference for (T+I)2V </h3></summary>
        
Run the following command to get the (T+I)2V results:

```python
python sample_scripts/with_mask_sample.py
```

- The generated video will be saved in ```results/mask_no_ref```.
</details>

<details>
  <summary><h3>Inference for (T+I+Ref)2V</h3></summary>
        
Run the following command to get the (T+I+Ref)2V results:

```python
python sample_scripts/with_mask_ref_sample.py
```

- The generated video will be saved in ```results/mask_ref```.
</details>

<details>
  <summary><h3>More Details</h3></summary>
        
You may modify ```configs/with_mask_sample.yaml``` to change the (T+I)2V conditions and modify ```configs/with_mask_ref_sample.yaml``` to change the (T+I+Ref)2V conditions.
For example:

- ```ckpt``` is used to specify a model checkpoint.

- ```text_prompt``` is used to describe the content of the video.

- ```input_path``` is used to specify the path to the image.

- ```ref_path``` is used to specify the path to the reference image.

- ```save_path``` is used to specify the path to the generated video.
</details>



## Results
### (T+Ref)2V Results
<table class="center">
<tr>
  <td style="text-align:center;width: 50%" colspan="1"><b>Reference Image</b></td>
  <td style="text-align:center;width: 50%" colspan="1"><b>Output Video</b></td>
</tr>
<tr>
  <td><img src="examples/TR2V/image/Egyptian_Pyramids.png" width="250">
      <br>
<!--       <div class="text" style=" text-align:center;">
        Scene Reference
      </div> -->
      <p align="center">Scene Reference</p>
  </td>
  <td>
      <img src="examples/TR2V/video/Fireworks_explode_over_the_pyramids.gif" width="400">
      <br>
<!--       <div class="text" style=" text-align:center;">
        Fireworks explode over the pyramids.
      </div> -->
          <p align="center">Fireworks explode over the pyramids.</p>
  </td>
</tr>

<tr>
  <td><img src="examples/TR2V/image/Great_Wall.png" width="250">
      <br>
<!--       <div class="text" style=" text-align:center;">
        Scene Reference
      </div> -->
      <p align="center">Scene Reference</p>
  </td>
  <td>
      <img src="examples/TR2V/video/The_Great_Wall_burning_with_raging_fire.gif" width="400">
      <br>
<!--       <div class="text" style=" text-align:center;">
        The Great Wall burning with raging fire.
      </div> -->
          <p align="center">The Great Wall burning with raging fire.</p>
  </td>
</tr>

<tr>
  <td><img src="examples/TR2V/image/a_green_cat.png" width="250">
      <br>
<!--       <div class="text" style=" text-align:center;">
        Object Reference
      </div> -->
      <p align="center">Object Reference</p>
  </td>
  <td>
      <img src="examples/TR2V/video/A_cat_is_running_on_the_beach.gif" width="400">
      <br>
<!--       <div class="text" style=" text-align:center;">
        A cat is running on the beach.
      </div> -->
          <p align="center">A cat is running on the beach.</p>
  </td>
</tr>

</table>

### (T+I)2V Results
<table class="center">
<tr>
  <td style="text-align:center;width: 50%" colspan="1"><b>Input Image</b></td>
  <td style="text-align:center;width: 50%" colspan="1"><b>Output Video</b></td>
</tr>
<tr>
  <td><img src="input/i2v/Underwater_environment_cosmetic_bottles.png" width="400"></td>
  <td>
      <img src="examples/TI2V/Underwater_environment_cosmetic_bottles.gif" width="400">
      <br>
<!--       <div class="text" style=" text-align:center;">
        Underwater environment cosmetic bottles.
      </div> -->
          <p align="center">Underwater environment cosmetic bottles.</p>
  </td>
</tr>

<tr>
  <td><img src="input/i2v/A_big_drop_of_water_falls_on_a_rose_petal.png" width="400"></td>
  <td>
      <img src="examples/TI2V/A_big_drop_of_water_falls_on_a_rose_petal.gif" width="400">
      <br>
<!--       <div class="text" style=" text-align:center;">
        A big drop of water falls on a rose petal.
      </div> -->
          <p align="center">A big drop of water falls on a rose petal.</p>
  </td>
</tr>

<tr>
  <td><img src="input/i2v/A_fish_swims_past_an_oriental_woman.png" width="400"></td>
  <td>
      <img src="examples/TI2V/A_fish_swims_past_an_oriental_woman.gif" width="400">
      <br>
<!--       <div class="text" style=" text-align:center;">
        A fish swims past an oriental woman.
      </div> -->
          <p align="center">A fish swims past an oriental woman.</p>
  </td>
</tr>

<tr>
  <td><img src="input/i2v/Cinematic_photograph_View_of_piloting_aaero.png" width="400"></td>
  <td>
      <img src="examples/TI2V/Cinematic_photograph_View_of_piloting_aaero.gif" width="400">
      <br>
<!--       <div class="text" style=" text-align:center;">
        Cinematic photograph. View of piloting aaero.
      </div> -->
          <p align="center">Cinematic photograph. View of piloting aaero.</p>
  </td>
</tr>

<tr>
  <td><img src="input/i2v/Planet_hits_earth.png" width="400"></td>
  <td>
      <img src="examples/TI2V/Planet_hits_earth.gif" width="400">
      <br>
<!--       <div class="text" style=" text-align:center;">
        Planet hits earth.
      </div> -->
          <p align="center">Planet hits earth.</p>
  </td>
</tr>
</table>


### T2V Results
<table>
<tr>
  <td style="text-align:center;width: 66%" colspan="2"><b>Output Video</b></td>
</tr>
<tr>
  <td>
      <img src="examples/T2V/A_deer_looks_at_the_sunset_behind_him.gif"/>
      <br>
<!--       <div class="text" style=" text-align:center;">
        A deer looks at the sunset behind him.
      </div> -->
          <p align="center">A deer looks at the sunset behind him.</p>
  </td>
  <td>
      <img src="examples/T2V/A_duck_is_teaching_math_to_another_duck.gif"/>
      <br>
<!--       <div class="text" style=" text-align:center;">
        A duck is teaching math to another duck.
      </div> -->
          <p align="center">A duck is teaching math to another duck.</p>
  </td>
</tr>
<tr>
  <td>
      <img src="examples/T2V/Bezos_explores_tropical_rainforest.gif"/>
      <br>
<!--       <div class="text" style=" text-align:center;">
        Bezos explores tropical rainforest.
      </div> -->
          <p align="center">Bezos explores tropical rainforest.</p>
  </td>
  <td>
      <img src="examples/T2V/Light_blue_water_lapping_on_the_beach.gif"/>
      <br>
<!--       <div class="text" style=" text-align:center;">
        Light blue water lapping on the beach.
      </div> -->
          <p align="center">Light blue water lapping on the beach.</p>
  </td>
</tr>

</table>

## BibTeX
```bibtex
@article{zhuang2024vlogger,
title={Vlogger: Make Your Dream A Vlog},
author={Zhuang, Shaobin and Li, Kunchang and Chen, Xinyuan and Wang, Yaohui and Liu, Ziwei and Qiao, Yu and Wang, Yali},
journal={arXiv preprint arXiv:2401.09414},
year={2024}
}
```

```bibtex
@article{chen2023seine,
title={SEINE: Short-to-Long Video Diffusion Model for Generative Transition and Prediction},
author={Chen, Xinyuan and Wang, Yaohui and Zhang, Lingjun and Zhuang, Shaobin and Ma, Xin and Yu, Jiashuo and Wang, Yali and Lin, Dahua and Qiao, Yu and Liu, Ziwei},
journal={arXiv preprint arXiv:2310.20700},
year={2023}
}
```

```bibtex
@article{wang2023lavie,
  title={LAVIE: High-Quality Video Generation with Cascaded Latent Diffusion Models},
  author={Wang, Yaohui and Chen, Xinyuan and Ma, Xin and Zhou, Shangchen and Huang, Ziqi and Wang, Yi and Yang, Ceyuan and He, Yinan and Yu, Jiashuo and Yang, Peiqing and others},
  journal={arXiv preprint arXiv:2309.15103},
  year={2023}
}
```


## Disclaimer
We disclaim responsibility for user-generated content. The model was not trained to realistically represent people or events, so using it to generate such content is beyond the model's capabilities. It is prohibited for pornographic, violent and bloody content generation, and to generate content that is demeaning or harmful to people or their environment, culture, religion, etc. Users are solely liable for their actions. The project contributors are not legally affiliated with, nor accountable for users' behaviors. Use the generative model responsibly, adhering to ethical and legal standards.

## Contact Us
**Shaobin Zhuang**: [zhuangshaobin@pjlab.org.cn](mailto:zhuangshaobin@pjlab.org.cn), **Kunchang Li**: [likunchang@pjlab.org.cn](mailto:likunchang@pjlab.org.cn)

**Xinyuan Chen**: [chenxinyuan@pjlab.org.cn](mailto:chenxinyuan@pjlab.org.cn), **Yaohui Wang**: [wangyaohui@pjlab.org.cn](mailto:wangyaohui@pjlab.org.cn)  

## Acknowledgements
The code is built upon [SEINE](https://github.com/Vchitect/SEINE), [LaVie](https://github.com/Vchitect/LaVie), [diffusers](https://github.com/huggingface/diffusers) and [Stable Diffusion](https://github.com/CompVis/stable-diffusion), we thank all the contributors for open-sourcing. 


## License

The code is licensed under Apache-2.0, model weights are fully open for academic research and also allow **free** commercial usage. To apply for a commercial license, please contact zhuangshaobin@pjlab.org.cn.

