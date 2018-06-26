# coding: utf-8
'''
Created on 2014年9月28日

@author: xhj
'''

import cv2
import numpy as np


if __name__ == '__main__':
    # read img
    grayimg = cv2.imread(r'E:\pyopencv\imgs\stuff.jpg',0)
    # binary
    ret, binary = cv2.threshold(grayimg,127,255,cv2.THRESH_BINARY)
    contours, hierarchy = cv2.findContours(binary,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    img = grayimg.copy()
    cv2.drawContours(grayimg,contours,-1,(0,0,255),3) 
    
    cv2.imshow('img', img)
    cv2.imshow('contour0', grayimg)
    cv2.imshow('contour1', binary)
    cv2.waitKey(0)
    cv2.destroyAllWindows()    