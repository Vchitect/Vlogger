# Vlogger
[![arXiv](https://img.shields.io/badge/arXiv-2310.20700-b31b1b.svg)](https://arxiv.org/abs/2310.20700)
[![Project Page](https://img.shields.io/badge/SEINE-Website-green)](https://vchitect.github.io/SEINE-project/)
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2FVchitect%2FSEINE&count_bg=%23F59352&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=visitors&edge_flat=false)](https://hits.seeyoufarm.com)

This repository is the official implementation of [Vlogger](https://arxiv.org/abs/2310.20700):

**[Vlogger: Make Your Dream A Vlog](https://arxiv.org/abs/2310.20700)**


<iframe width="748" height="422" src="https://youtu.be/ZRD1-jHbEGk" title="AI&#39;s Premiere: Mr. Polar Bear&#39;s Fantastic Journey | The First 3-Min All-AI-Produced Video" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" allowfullscreen></iframe>

##  Setup

### Prepare Environment
```
conda create -n vlogger python==3.10.11
conda activate vlogger
pip install -r requirements.txt
```

### Download our model and T2I base model

Our model is based on Stable diffusion v1.4, you may download [Stable Diffusion v1-4](https://huggingface.co/CompVis/stable-diffusion-v1-4) and [OpenCLIP-ViT-H-14](https://huggingface.co/laion/CLIP-ViT-H-14-laion2B-s32B-b79K) to the director of ``` pretrained ```
.
Download our model checkpoint (from [google drive](https://drive.google.com/file/d/1pAH73kz2QRfD2Dxk4lL3SrHvLAlWcPI3/view?usp=drive_link) or [hugging face](https://huggingface.co/GrayShine/Vlogger/tree/main)) and save to the directory of ```pretrained```


Now under `./pretrained`, you should be able to see the following:
```
├── pretrained
│   ├── vlogger.pt
│   ├── stable-diffusion-v1-4
│   ├── OpenCLIP-ViT-H-14
│   │   ├── ...
└── └── ├── ...
        ├── ...
```
## Usage
### Inference for (T+I)2V 
Run the following command to get the I2V results:
```python
python sample_scripts/with_mask_sample.py
```
The generated video will be saved in ```results/mask_no_ref```.
### Inference for (T+I+ref)2V 
Run the following command to get the I2V results:
```python
python sample_scripts/with_mask_ref_sample.py
```
The generated video will be saved in ```results/mask_ref```.

#### More Details
You may modify ```configs/with_mask_sample.yaml``` to change the (T+I)2V conditions.

You may modify ```configs/with_mask_ref_sample.yaml``` to change the (T+I+ref)2V conditions.
For example:

```ckpt``` is used to specify a model checkpoint.

```text_prompt``` is used to describe the content of the video.

```input_path``` is used to specify the path to the image.

```ref_path``` is used to specify the path to the reference image.

```save_path``` is used to specify the path to the generated video.


## Results
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
      <div class="text" style=" text-align:center;">
        Underwater environment cosmetic bottles.
      </div>
  </td>
</tr>

<tr>
  <td><img src="input/i2v/A_big_drop_of_water_falls_on_a_rose_petal.png" width="400"></td>
  <td>
      <img src="examples/TI2V/A_big_drop_of_water_falls_on_a_rose_petal.gif" width="400">
      <br>
      <div class="text" style=" text-align:center;">
        A big drop of water falls on a rose petal.
      </div>
  </td>
</tr>

<tr>
  <td><img src="input/i2v/A_fish_swims_past_an_oriental_woman.png" width="400"></td>
  <td>
      <img src="examples/TI2V/A_fish_swims_past_an_oriental_woman.gif" width="400">
      <br>
      <div class="text" style=" text-align:center;">
        A fish swims past an oriental woman.
      </div>
  </td>
</tr>

<tr>
  <td><img src="input/i2v/Cinematic_photograph_View_of_piloting_aaero.png" width="400"></td>
  <td>
      <img src="examples/TI2V/Cinematic_photograph_View_of_piloting_aaero.gif" width="400">
      <br>
      <div class="text" style=" text-align:center;">
        Cinematic photograph. View of piloting aaero.
      </div>
  </td>
</tr>

<tr>
  <td><img src="input/i2v/Planet_hits_earth.png" width="400"></td>
  <td>
      <img src="examples/TI2V/Planet_hits_earth.gif" width="400">
      <br>
      <div class="text" style=" text-align:center;">
        Planet hits earth.
      </div>
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
      <div class="text" style=" text-align:center;">
        A deer looks at the sunset behind him.
      </div>
  </td>
  <td>
      <img src="examples/T2V/A_duck_is_teaching_math_to_another_duck.gif"/>
      <br>
      <div class="text" style=" text-align:center;">
        A duck is teaching math to another duck.
      </div>
  </td>
</tr>
<tr>
  <td>
      <img src="examples/T2V/Bezos_explores_tropical_rainforest.gif"/>
      <br>
      <div class="text" style=" text-align:center;">
        Bezos explores tropical rainforest.
      </div>
  </td>
  <td>
      <img src="examples/T2V/Light_blue_water_lapping_on_the_beach.gif"/>
      <br>
      <div class="text" style=" text-align:center;">
        A deer looks at the sunset behind him.
      </div>
  </td>
</tr>

</table>

## BibTeX
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
**Shaobin Zhuang**: [zhuangshaobin@pjlab.org.cn](mailto:zhuangshaobin@pjlab.org.cn)

**Kunchang Li**: [likunchang@pjlab.org.cn](mailto:likunchang@pjlab.org.cn)

**Xinyuan Chen**: [chenxinyuan@pjlab.org.cn](mailto:chenxinyuan@pjlab.org.cn)

**Yaohui Wang**: [wangyaohui@pjlab.org.cn](mailto:wangyaohui@pjlab.org.cn)  

## Acknowledgements
The code is built upon [SEINE](https://github.com/Vchitect/SEINE), [LaVie](https://github.com/Vchitect/LaVie), [diffusers](https://github.com/huggingface/diffusers) and [Stable Diffusion](https://github.com/CompVis/stable-diffusion), we thank all the contributors for open-sourcing. 


## License
The code is licensed under Apache-2.0, model weights are fully open for academic research and also allow **free** commercial usage. To apply for a commercial license, please contact zhuangshaobin@pjlab.org.cn.
=======
