# coding: utf-8
'''
Created on 2014��9��21��

@author: xhj
'''

import cv2
from cv2 import *
import numpy as np

def readShowImg(imgfile):
    img = cv2.imread(imgfile)  # 读取图像
    
    ShowImg(img)
   
def ShowImg(img):
    cv2.namedWindow('Image')  
    cv2.imshow('Image',img)    # 在上边创建的命名窗口中显示图像
    cv2.waitKey(0)             # 等待图像显示
    cv2.destroyWindow('Image')    # good practice

def copyImg2Img(imgf1, imgf2):
    img = cv2.imread(imgf1,cv2.CV_LOAD_IMAGE_GRAYSCALE)  # 读取RGB三色的灰度图像
    img2 = img.copy()
    print cv2.imwrite(imgf2,img2,[int(cv2.IMWRITE_JPEG_QUALITY), 5])
    cv2.imshow('Image1',img2)
    img3 = np.zeros(img.shape, np.uint8)
    ShowImg(img3)
    
    
if __name__ == '__main__':
    #readShowImg(r'E:\pyopencv\imgs\fruits.jpg')
    copyImg2Img(r'E:\pyopencv\imgs\fruits.jpg',r'E:\pyopencv\imgs\fruits1.jpg')