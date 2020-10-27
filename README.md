# 졸업 프로젝트  
```
진행 학기 : 4학년 1,2학기 (2020.03 - 2020.11)  
참가 인원 : 2인1팀  
지도 교수님 : 김태현 교수님  
졸업 프로젝트 주제 : image inpainting    
목표 : image inpainting에서 사용된 딥러닝 방식을 이해하고 응용해보기   
```
## 1. Abstract

어떤 요소들이 image inpainting의 성능에 영향을 끼칠 것인지 생각해보고자 하고, 결과를 분석하는 자동화된 코드를 작성하여 테스트를 한 후 결과를 측정해보고자 한다.

## 2. Introduction

### 2.1. Image Inpainting

- **Image Inpainting**이란 이미지에서 노이즈나 지워진 부분을 복원하는 것으로 이를 수행했던 초기 방법과 최근 방법은 다르다.
    - 초기 방법 : 주변 픽셀 값을 이용하여 비어있는 값을 예측하여 채우는 방식([참고](https://docs.opencv.org/master/df/d3d/tutorial_py_inpainting.html)) 사용
    - 최근 방법 : 딥러닝을 이용한 방식으로 CNN과 같은 특정 네트워크를 이용하여 학습시킨 모델 사용

## 3. Related Work

### 3.1. Generative Image Inpainting with Contextual Attention 21 Mar 2018
|
[논문](https://arxiv.org/pdf/1801.07892.pdf) |
[코드](https://github.com/JiahuiYu/generative_inpainting) |
[리뷰](https://github.com/stellakang/vision_proj/blob/master/GenerativeImageInpaintingWithContextualAttention.md) |

### 3.2. Image Inpainting for Irregular Holes Using Partial Convolutions 15 Dec 2018
|
[논문](https://arxiv.org/abs/1804.07723) |
[코드](https://github.com/MathiasGruber/PConv-Keras/blob/master/libs/pconv_model.py) |
[리뷰](https://github.com/kangsj123/vision_proj/blob/master/ForIrregularHolesUsingPartialConvolutions.md) |

### 3.3. Free-Form Image Inpainting with Gated Convolution 22 Oct 2019
|
[논문](https://arxiv.org/pdf/1806.03589.pdf) |
[코드](https://github.com/JiahuiYu/generative_inpainting) |
[리뷰](https://github.com/stellakang/vision_proj/blob/master/FreeFormImageInpaintingWithGatedConvolution.md) |
## 4. Approach

### 4.1. 성능 평가 기준

Mask의 Size에 따라 이미지 복원정도가 어떻게 달라지는지 테스트를 통해 확인하고, image inpainting의 성능에 끼치는 영향에 대한 결과를 분석하고자 한다.

### 4.2. 결과 분석 지표

성능 평가를 위한 결과를 분석하기 위한 지표로 PSNR과 SSIM metric을 사용하였다.

- PSNR
<img src="./img/metric1.png" width="300">
PSNR metric은 원본 이미지와 데이터 손실이 있는 이미지 간의 화질 차이를 측정하기 위한 metric으로, 이를 위해 사용되는 MSE는 원본 이미지와 데이터의 손실이 있는 이미지 간의 픽셀 대 픽셀 차이값의 제곱합을 평균낸 값이다.  

- SSIM
<img src="./img/metric2.png" width="300">
SSIM metric은 수치적인 에러가 아닌 인간의 시각적 화질 차이 및 유사도를 평가하기 위해 고안된 방법으로, 이를 이용하여 두 이미지의 휘도, 대비 및 구조를 비교하고자 한다.

### 4.3. 테스트를 위해 사용한 모델

테스트를 위해 사용한 모델은 'Generative Image Inpainting with Contextual Attention' ([링크](https://arxiv.org/pdf/1801.07892.pdf)) 이다. 이는 places2 dataset으로 pretrained된 모델이다.

### 4.4 테스트 데이터셋

테스트를 위해 사용한 데이터셋은 [places2](http://places2.csail.mit.edu/download.html) 이다. (링크의 places365-standard의 high resolution images의 test images)

### 4.5 테스트 과정

- 1)places2 dataset의 이미지와 2)가운데에 직사각형으로 위치한 mask 파일을 이용하여 prediction 시킨 결과를 얻는다.
- 방법
    1. [논문 repository](https://github.com/JiahuiYu/generative_inpainting)를 다운받고(clone) `Run`에 나와있는 환경 설정 및 pretrained model 다운로드
    2. [generate.yml](https://github.com/stellakang/vision_proj/blob/master/evaluation/mask-size/generate.yml)에 정보 기입
        - `sample_set_directory`: test dataset의 path (ex. "examples/test_large")
        - `test_set_directory`: prediction을 진행할 위치 & 이미지 복원 결과로 나온 이미지를 저장. 경로 생성하므로 경로 존재하지 않아도 됨. (ex. "examples/test_places2")
        - `masksize_options`: 가운데에 위치할 마스크의 `height*width` 정보 (ex. `["10*10", "20*20", "30*30"]`)
        - `model_directory`: train된 모델의 path (ex. "model_logs/release_places2_256")
    3. 1)에서 다운받은 repository 내에 `generate.yml`, `test_mask_size.py`를 위치시킨다.
    4. `python test_mask_size.py`를 실행한다.  [작성 코드](https://github.com/stellakang/vision_proj/blob/master/evaluation/mask-size)

## 5. Result

### 5.1. 요약

mask의 size에 따라 이미지 복원 정도가 어떻게 테스트해본 결과,

### 5.2. 실험 결과
1. PSNR metric

    ![psnr](./img/psnr_graph.png)  
    
    | | 10x10 | 20x20 | 30x30 | 40x40 | 50x50 | 60x60 |   
    |:---:|:---:| :---: | :---: |:---:|:---:|:---:|  
    | PSNR | 95.69 | 94.06 | 91.94 | 89.77	| 87.80 | 85.81 |   
    
2. SSIM metric

    ![ssim](./img/ssim_graph.png) 
    
    | | 10x10 | 20x20 | 30x30 | 40x40 | 50x50 | 60x60 |   
    |:---:|:---:| :---: | :---: |:---:|:---:|:---:|   
    | SSIM | 0.999999951504037 | 0.9999994279626380 | 0.999997875733462 | 0.999994670819185	| 0.999989010766895 | 0.999979951577578 |   
  


