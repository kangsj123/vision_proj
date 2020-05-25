# Generative Image Inpainting with Contextual Attention

abstract
--------
### 딥러닝 기반 접근 방식    
장점: 시각적으로 그럴듯한 이미지 구조와 질감을 생성  
단점: 가끔 주변 이미지와 어울리지 않는 왜곡되거나 흐릿한 이미지 생성  
* 공간적으로 거리가 먼 위치에서 값을 가져오는 convolutional neural network 때문.  
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


