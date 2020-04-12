# Image Inpainting for Irregular Holes Using Partial Convolutions

abstract
========
기존에는 표준적인 convolutional network : 색깔 차이를 보이거나 흐릿하다는 문제점
-> partial convolutions : convolution이 유효한 픽셀에 대해서'만' masked, renormalized되는 방식  

Introduction
==========  
Goal : irregular hole pattern에도 이미지 복원을 견고하게 잘 해내는 모델을 제안하고, 따로 후처리가 필요없이 이미지가 자연스럽게 보여지도록 예측을 잘 해내는 것이다.  

최근 image inpainting 접근법 및 문제점   
1) Non-learning Based model : use image statistics  
problems  
구멍을 채우기 위해서 통계적인 방법을 사용,
시각적으로 의미를 지니지 않는 결과, 작은 구멍에 대해서만 성능이 잘 나타남,

2) Deep learning Based model : use deeplearning  
이미지에 convolutional filters를 적용하고 구멍은 고정된 초기값을 채워넣는다. 
problems  
이 방식은 구멍을 어떻게 초기화하느냐에 따라 결과가 다르게 나타나고 post-processing을 필요로 하는 방식.  

3) focus on rectangular shaped holes  
problems  
limit the utility of these models in application  
  
-> 이 논문에서는 구멍 초기화에 상관없이 이미지 복원을 잘하고  
비싼 post processing을 필요로 하지 않는 방법을 모색하고자 함.  






