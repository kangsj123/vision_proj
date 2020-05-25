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
- ### 문제점 : 주변 이미지와 어울리지 않게 1. 경계가 부자연스럽거나, 2. 왜곡된 구조를 나타내거나, 3. 흐릿한 텍스쳐를 생성  
- ### 문제점이 나타나는 이유 : hole region과 이와 먼 위치의 pixel간의 correlation을 찾으려고 할때 생기는 CNN의 비효율성 때문  
- recent works는 visual quality를 향상시키지만, 수백번의 iteration과 수분의 이미지 처리 시간이 수반된다.  

### 이 논문에서 제시한 네트워크  
최근 방식의 문제점을 기반으로 2단계의 네트워크를 제시했다.  

#### 1. first stage  
- a simple dilated convolutional network  

#### 2. second stage  
- contextual attention module   
- known patch를 convolutional filters로 사용하여 생성된 patch를 처리하는데 사용.  
- spatial coherency를 높여주는 spatial propagation layer를 포함.  
  
전체 네트워크는 reconstruction losses, two Wasserstein GAN losses로 학습시킨다.  
실험은 faces, textures, natural images 등을 포함한 여러 데이터셋을 사용하였다.  
- CelebA faces, CelebA-HQ faces, DTD textures, ImageNet, Places2  

Related Work 
-------


