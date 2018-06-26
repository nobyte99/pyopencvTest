# coding: utf-8
'''
Created on 2014��9��23��

可以观察图像中灰度的变化。某些图像中包含大量的强度不变的区域（如蓝天），
而在其他图像中的灰度变化可能会非常快（如包含许多小物体的拥挤的图像）。因此，
观察图像中这些变化的频率就构成了另一条分类图像的方法。这个观点称为频域。
而通过观察图像灰度分布来分类图像称为空间域。

频域分析将图像分成从低频到高频的不同部分。低频对应图像强度变化小的区域，
而高频是图像强度变化非常大的区域。目前已存在若干转换方法，如傅立叶变换或余弦变换，
可以用来清晰的显示图像的频率内容。注意，由于图像是一个二维实体，所以其由水平频率（水平方向的变化）
和竖直频率（竖直方向的变化）共同组成。

在频率分析领域的框架中，滤波器是一个用来增强图像中某个波段或频率并阻塞（或降低）其他频率波段的操作。
低通滤波器是消除图像中高频部分，但保留低频部分。高通滤波器消除低频部分

@author: xhj
'''


import cv2
import numpy as np

def filter(img):
    '''
       这些滤波不仅可以处理灰度图像，也可处理rgb图像
    '''
    cv2.imshow('img_org',img)
    
    # 平滑, 周围点权重相同
    img1 = cv2.blur(img,(5,5))
    cv2.imshow('img_blur',img1)
    
    # 高斯模糊， 周围点权重不同
    gaussimg = cv2.GaussianBlur(img, (5,5),1.5)
    cv2.imshow('img_gauss', gaussimg)
    
    # 中值滤波，消除噪声
    zzimg = cv2.medianBlur(img,5)
    cv2.imshow('img_zzfilter',zzimg)
    
    

if __name__ == '__main__':
    img = cv2.imread(r'E:\pyopencv\imgs\fruits.jpg')
    filter(img)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()