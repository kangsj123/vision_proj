# Generative Image Inpainting with Contextual Attention

abstract
--------
### 딥러닝 기반 접근 방식    
장점: 시각적으로 그럴듯한 이미지 구조와 질감을 생성  
단점: 가끔 주변 이미지와 어울리지 않는 왜곡되거나 흐릿한 이미지 생성  
* 공간적으로 거리가 먼 위치에서 값을 가져올때 CNN의 비효율성 때문.  
* 주변 이미지에서 값을 가져오는 전통적인 이미지 합성 방식에서는 이 문제 해결 가능.  

--> 1. 새로운 이미지 구조를 합성 가능하고, 2. 주변 이미지 피쳐를 활용하는 'new deep generative model-based' 방식을 제안  

Introduction  
---------

image inpainting 응용 분야 : 사진 편집, 이미지 기반 렌더링, 컴퓨터를 이용한 사진 기법 등  
image inpainting에서 가장 중요한 것은 missing regions가 주변 이미지와 시각적, 의미적으로 그럴 듯하게 합성되어야 하는 것.    

Early works    
- background patch를 가져와서 hole을 채우는 texture synthesis와 유사한 방식  
- background inpainting(배경 복원에는 유리)  
- missing regions에 들어갈 값이 배경 내에 있다는 것을 가정한 것이기 때문에  
복잡하거나, 반복되지 않는 구조 등을 복원하는 경우 어려움을 겪는다.  

Recent works  
- CNN과 GAN의 영향으로 성장   
- convolutional encoder-decoder network로 나타내어 기존 pixels와 생성된 pixel간의 일관성을 높일 수 있도록.  
- high structured image 생성에 유리(얼굴, 사물 등)  
- 문제점 : 주변 이미지와 어울리지 않게 1. 경계가 부자연스럽거나, 2. 왜곡된 구조를 나타내거나, 3. 흐릿한 텍스쳐를 생성  
- 문제점이 나타나는 이유 : hole region과 이와 먼 위치의 pixel간의 correlation을 찾으려고 할때 생기는 CNN의 비효율성 때문  
- recent works는 visual quality를 향상시키지만, 수백번의 iteration과 수분의 이미지 처리 시간이 수반된다.  

### 이 논문에서 제시한 네트워크  
최근 방식의 문제점을 기반으로 2단계의 네트워크를 제시했다.  

1. first stage  
- a simple dilated convolutional network  

2. second stage  
- contextual attention module   
- known patch를 convolutional filters로 사용하여 생성된 patch를 처리하는데 사용.  
- spatial coherency를 높여주는 spatial propagation layer를 포함.  
  
전체 네트워크는 reconstruction losses, two Wasserstein GAN losses로 학습시킨다.  
실험은 faces, textures, natural images 등을 포함한 여러 데이터셋을 사용하였다.  
- CelebA faces, CelebA-HQ faces, DTD textures, ImageNet, Places2  

Related Work 
-------
### 1. Image inpainting  
기존 work는 크게 두 가지로 나누어 볼 수 있다.  

#### 1) traditional diffusion or patch-based approach  
- 배경의 이미지를 hole로 가져오는 방식으로, variational algorithm이나 patch similarity 사용  
- stationary texture에서만 잘 작동 -> non stationary에서 잘 작동하지 않는 문제 해결하기 위한 다양한 방법 제시됨   

#### 2) learning based approach
- deep learning and GAN based  
- small regions 복원 -> large holes 복원으로 발전  
  - context encoders가 large hole을 복원하기 위한 dnn을 학습시키며  
    reconstruction loss & generative adversarial loss를 objective function으로 한다.  
- 더 나아가서, global & local discriminator를 이용하여 이미지 전체와 부분에 있어서 coherent한지 평가한다.  
- channel-wise fully connected layer 대신 dilated convolution을 사용한다.  

### 2. Attention modeling   
- deep convolutional neural networks에서 spatial attention을 배우는 studies가 많다.  
- STN : for object classification tasks, 파라미터를 예측할 수 있는 localization module을 가지고 있다.  
- appearance flow : predict offset vectors  

### 3. Improved Generative Inpainting Network  
*논문에서 제시한 네트워크*  
- 기존 state-of-the-art inpainting model을 개선하여 이 논문에서 새로운 네트워크를 구성하였다.  
- two-stage coarse-to-fine network architecture  
  : receptive field의 사이즈가 충분히 큰 것이 중요하다.  
  
  - input : 직사각형 hole을 흰 색으로 채운 이미지 256x256, hole을 나타내는 binary mask  
  학습된 모델은 다양한 사이즈의 이미지와 여러 구멍이 있는 이미지를 input으로 받아들일 수 있다.  
  - output : final completed image (복원한 이미지)   
  - first network: initial coarse prediction   
    - reconstruction loss로 학습된다.   
  - second network: predict refined results(coarse prediction as inputs)      
    - reconstruction & GAN loss로 학습된다.  

- 효율성을 위해 thin & deep scheme 으로 디자인되었고 더 적은 파라미더들을 사용한다.  
- detail  
  - 모든 convolution layers에 mirror padding 적용  
<img src="./img/mirror_padding.jpg" width="60%" height="60%"></img>  
  - batch normalization layers 제거 -> color coherence를 악화시킨다.  
  - ReLU 대신 ELU를 사용    
  - global과 local feature representations를 분리 -> 붙이는 것보다 분리하는 것이 더 잘 작동.  

- Global and local Wasserstein GANs  
  - WGAN-GP의 modified된 버전 제안  
  - second-stage refinement network의 output에 WGAN-GP loss를 적용한다(현재 GAN losses보다 잘 작동한다.)    
  - WGAN은 Earth-Mover distance 사용  
  - objective function: Kantorovich-Rubinstein duality를 적용하여 구성된다.  
  <img src="./img/wgan-gp_objective_function.jpg" width="60%" height="60%"></img>  
  
- Spatially discounted reconstruction loss  

### 4. Image Inpainting with Contextual Attention  

### 1) Contextual Attention  
 The contextual attention layer learns where to borrow or
copy feature information from known background patches
to generate missing patches.  

### 2) Unified Inpainting Network  
Output features from two encoders are aggregated and fed into a 5 single decoder to obtain the final output.  

For training, given a raw image x, sample a binary image mask m at a random location.  

