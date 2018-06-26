# coding: utf-8
'''
Created on 2014��9��21��

直方图： 描述了图像中某一灰度级别的像素占总像素的比例，从而描绘了图像的灰度分布，直方图可以单独计算图像中某一区域
的直方图，但是计算时分母必须是整个图像的像素总数。也就是必须正则化于整幅图像。

像素数值必定  0=< pixel <=255,即在区间【0，255】之间。
可见：直方图可以叠加。

@author: xhj
'''

import cv2
import numpy as np
import matplotlib.pyplot as plt

def calcAndDrawHist(image, color):    
    hist= cv2.calcHist([image], [0], None, [256], [0.0,255.0])    
    minVal, maxVal, minLoc, maxLoc = cv2.minMaxLoc(hist)    
    histImg = np.zeros([256,256,3], np.uint8)    
    hpt = int(0.9* 256);    
        
    for h in range(256):    
        intensity = int(hist[h]*hpt/maxVal)    
        cv2.line(histImg,(h,256), (h,256-intensity), color)    
            
    return histImg;

def calcDrawHistChannel(img):  
    '''
       根据直方图含义自己所写的函数，和上边的calcAndDrawHist函数所显示的图像完全相同。
    '''
    if img.ndim == 3:
        x = [i for i in range(256)]
        for i in range(3):
            hist = cv2.calcHist([img],[i],None, [256],[0.0,255.0])
            plt.plot(x,hist/hist.sum())   #使用matplotlib进行折线图绘制
        
        plt.show()
    

if __name__ == '__main__':
    img = cv2.imread(r'E:\pyopencv\imgs\fruits.jpg')
    calcDrawHistChannel(img)
    
    img = cv2.imread(r"E:\pyopencv\imgs\fruits.jpg")    
    b, g, r = cv2.split(img)    
    
    histImgB = calcAndDrawHist(b, [255, 0, 0])    
    histImgG = calcAndDrawHist(g, [0, 255, 0])    
    histImgR = calcAndDrawHist(r, [0, 0, 255])    
        
    cv2.imshow("histImgB", histImgB)    
    cv2.imshow("histImgG", histImgG)    
    cv2.imshow("histImgR", histImgR)    
    cv2.imshow("Img", img)    
    cv2.waitKey(0)    
    cv2.destroyAllWindows()   