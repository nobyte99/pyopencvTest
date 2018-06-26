# coding:utf-8
'''
Created on 2016年11月28日
红：[ 255,0,0 ]
绿：[ 0,255,0 ]
蓝：[ 0,0,255 ]
输出颜色值对应的HSV数值

@author: xhj
'''
import cv2
import numpy as np
if __name__ == '__main__':
    arrayRed = np.uint8([[[255,0,0]]])
    arrayGreen = np.uint8([[[0,255,0]]])
    arrayYellow = np.uint8([[[0,0,255]]])
    
    hsvRed = cv2.cvtColor(arrayRed,cv2.COLOR_RGB2HSV)
    print hsvRed
    hsvGreen = cv2.cvtColor(arrayGreen,cv2.COLOR_RGB2HSV)
    print hsvGreen
    hsvYellow = cv2.cvtColor(arrayYellow,cv2.COLOR_RGB2HSV)
    print hsvYellow