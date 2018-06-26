# coding: utf-8
'''
Created on 2014年9月21日

@author: xhj
'''
import cv2
import numpy as np
from numpy import ndarray
import random

def salt(img,n):
    for i in range(n):
        i = int(random.random()*img.shape[0])
        j = int(random.random()*img.shape[1])
        if img.ndim ==2:
            img[i,j] = 255
        else:
            img[i,j,0]= 255
            img[i,j,1]= 255
            img[i,j,2]= 255
    return img
      
def ImgChannelSplit(img):
    if img.ndim == 3:
        r,g,b = cv2.split(img) #分理处rgb三色通道
        cv2.namedWindow('blue')
        cv2.imshow('blue',b)
        cv2.namedWindow('green')
        cv2.imshow('green',g)
        cv2.namedWindow('red')
        cv2.imshow('red',r)
        return r,g,b
#     elif img.ndim == 2:  # 灰度图像不能分离rgb通道
#         black,write = cv2.split(img)
#         cv2.namedWindow('black')
#         cv2.imshow('black',b)
        
def imgbright(img,bright_scale):
    if img.ndim == 3:
        img *= bright_scale
    return img 

if __name__ == '__main__':
    img = cv2.imread(r'E:\pyopencv\imgs\fruits.jpg')
    cv2.namedWindow('img_org')
    cv2.imshow('img_org',img)
    img1 = salt(img.copy(),3000)
    cv2.namedWindow('img_done')
    cv2.imshow('img_done',img1)
    
    r,g,b = ImgChannelSplit(img)
    
    imgcopy = cv2.merge([r,g,b])   #合并rgb三色通道
    cv2.namedWindow('merge')
    cv2.imshow('merge',imgcopy)
    
    # 图像变亮
    img2=imgbright(img.copy(), 1.1)
    cv2.namedWindow('imgbright')
    cv2.imshow('imgbright',img2)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    