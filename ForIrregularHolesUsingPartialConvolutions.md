# Image Inpainting for Irregular Holes Using Partial Convolutions  

abstract  
--------  
기존에는 표준적인 convolutional network : 색깔 차이를 보이거나 흐릿하다는 문제점  
-> partial convolutions : convolution이 유효한 픽셀에 대해서'만' masked, renormalized되는 방식  

Introduction & Related work    
-------- 
Goal : irregular hole pattern에도 이미지 복원을 견고하게 잘 해내는 모델을 제안하고,  
따로 후처리가 필요없이 이미지가 자연스럽게 보여지도록 예측을 잘 해내는 것이다.  

## 최근 image inpainting 접근법 및 문제점   
__1) Non-learning Based model__ : use image statistics  
problems     
- 구멍을 채우기 위해서 통계적인 방법을 사용  
- 시각적으로 의미를 지니지 않는 결과  
- 작은 구멍에 대해서만 성능이 잘 나타남(==variance is low)  
- large computation cost  

__2) Deep learning Based model__ : use deeplearning  
이미지에 convolutional filters를 적용하고 구멍은 고정된 초기값을 채워넣는다.  
problems      
- 구멍을 어떻게 초기화하느냐에 따라 결과가 다르게 나타남.  
- post-processing을 필요로 하는 방식.  

__3) focus on rectangular shaped holes__    
problems      
limit the utility of these models in application  
  
__-> 이 논문에서는 구멍 초기화에 상관없이 이미지 복원을 잘하고, irregular hole에 잘 대응할 수 있도록 큰 이미지 벤치마크를 사용했으며    
비싼 post processing을 필요로 하지 않는 방법을 모색하고자 함.__    

Approach  
------  
__1. Partial Convolutional Layer__    
partial convolution은 다음과 같이 연산한다:  
<img src="./img/partialconv.jpg" width="60%" height="30%"></img>

W : convolution filter weights  
b : bias  
X : feature values for the current convolution window(input으로 들어오는 feature)  
M : binary mask(input으로 들어오는 Mask)     

각 partial convolution 연산 이후에는, 마스크를 다음과 같이 업데이트 한다:  
<img src="./img/mask.jpg" width="30%" height="15%"></img>  
0 -> 구멍 포함  
1 -> 구멍 포함 안함  

__2. Network Architecture and Implementation__   
<img src="./img/pconv_network.jpg" width="60%" height="60%"></img>  
image/mask 사이즈 : CxHxW  
UNet-like architecture 사용 : partial convolutional 레이어들 + nearest neighbor up-sampling  
마지막 partial convolutional 레이어의 인풋 : 구멍을 포함한 원본 이미지 + 원본 마스크 -> 아웃풋 이미지에 인풋 이미지 정보를 전달하기 위함.  

__3. Loss Functions__    
아래의 전체 Loss는 각종 Loss들이 조합이다.  
<img src="./img/pconv_total_loss.jpg" width="60%" height="60%"></img>  
1) hole loss : hole인 부분에 대한 loss   
<img src="./img/pconv_hole_loss.jpg" width="30%" height="30%"></img>  
2) valid loss : non hole인 부분에 대한 loss  
<img src="./img/pconv_valid_loss.png" width="30%" height="30%"></img>  
3) perceptual loss : I out과 I comp 픽셀간의 차이를 줄이기 위함.  
I out : 모델을 타고 나오는 결과 이미지  
I comp : I out에서 non-hole부분을 원래 input pixel값으로 바꾼 것  
<img src="./img/pconv_perceptual_loss.jpg" width="60%" height="60%"></img>  
4) L style out loss  
<img src="./img/pconv_style_out_loss.jpg" width="60%" height="60%"></img>  
5) L style composited output loss  
<img src="./img/pconv_style_comp_loss.jpg" width="60%" height="60%"></img>  
6) total variation loss : hole의 경계에 대한 loss  
<img src="./img/pconv_total_variation_loss.jpg" width="60%" height="60%"></img>  


Experiments  
-----  
1. 이전 다른 논문에서는 임의로 직사각형 구멍(hole)을 제거한 데이터셋을 생성하였는데, 이 논문에서는 이를 개선하여 다양한 모양과 크기를 지닌 마스크를 생성했다.  
-> mask, image 모두 512x512  
-> 55,116 masks for training set/ 24,866 masks for test set 에서 random dilation, rotation, cropping을 통해 데이터 늘렸다.  
-> image border와 가까운 hole은 성능을 낮추기 때문에 test set을 image border에서 hole이 인접한 mask와 인접하지 않은 mask로 나누었다. 그리고 hole size에 따라서 mask를 6가지로 분류하였다. (6x2=12가지)

2. dataset: 3 image datasets(ImageNet, Places2, CelebA-HQ)  

3. Comparisons : PM, GL, GntIpt, Conv, Pconv(이 논문 방식)  

4. User Study  
unlimited time: 비교를 위해, 서로 다른 method를 사용한 이미지 두 개를 사람들에게 보여주고, 어떤 이미지가 더 현실적으로 보이는지 고르도록 시간을 무한정 준다.  
limited time: 각 method와 ground truth의 두 가지 이미지를 보여주고, 제한된 시간 안에 사람들에게 어떤 이미지가 더 현실적으로 보이는지 고르도록 한다.  

<img src="./img/user_study.jpg" width="60%" height="60%"></img>   


Discussion & Extension  
---
1. 장점 : hole control 가능(shape, location, distance from the image borders), hole size가 증가함에 따라 성능이 크게 저하되지 않는다.  
2. 여전히 failure cases 존재(문에 창살이 있는 경우, hole이 매우 큰 경우)  
3. 




