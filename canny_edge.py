# coding: utf-8
'''
Created on 2014��9��24��

canny只能处理灰度图

@author: xhj
'''

import cv2
import numpy as np

def canny_edge(img):
    '''
        只能处理灰度图像
    '''
    # gauss降噪
    img = cv2.GaussianBlur(img,(3,3),0)  
    canny = cv2.Canny(img, 50, 150)
    
    cv2.imshow('Canny', canny)  
    cv2.waitKey(0)  
    cv2.destroyAllWindows()  

if __name__ == '__main__':
    img = cv2.imread(r'E:\pyopencv\imgs\stuff.jpg',0)
    canny_edge(img)