## Image Inpainting for Irregular Holes Using Partial Convolutions

abstract
--------
기존에는 표준적인 convolutional network : 색깔 차이를 보이거나 흐릿하다는 문제점
              |
              v
partial convolutions : convolution이 유효한 픽셀에 대해서'만' masked, renormalized되는 방식  

Introduction
-------------  
Goal : irregular hole pattern에도 이미지 복원을 견고하게 잘 해내는 모델을 제안하고, 따로 후처리가 필요없이 이미지가 자연스럽게 보여지도록 예측을 잘 해내는 것이다.  

