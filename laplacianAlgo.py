# coding: utf-8
'''
Created on 2014��9��24��

图像中的边缘区域，像素值会发生“跳跃”，对这些像素求导，
在其一阶导数在边缘位置为极值，这就是Sobel算子使用的原理——极值处就是边缘。

如果对像素值求二阶导数，会发现边缘处的导数值为0。
Laplace函数实现的方法是先用Sobel 算子计算二阶x和y导数，再求和：

@author: xhj
'''

import cv2
import numpy as np

def laplacian_figureEdge(img):
    '''
       处理前最好先降噪，但是下面处理没有降噪
    '''
    gray_lap = cv2.Laplacian(img, cv2.CV_16S, ksize=3)
    dst = cv2.convertScaleAbs(gray_lap)
    cv2.imshow('laplacian',dst)  
    cv2.waitKey(0)  
    cv2.destroyAllWindows()       


if __name__ == '__main__':
    img = cv2.imread(r'E:\pyopencv\imgs\stuff.jpg')
    laplacian_figureEdge(img)