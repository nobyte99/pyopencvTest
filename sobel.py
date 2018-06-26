# coding: utf-8
'''
Created on 2014��9��24��

Sobel算子依然是一种过滤器，只是其是带有方向的

dst = cv2.Sobel(src, ddepth, dx, dy[, dst[, ksize[, scale[, delta[, borderType]]]]])  
前四个是必须的参数：

    第一个参数是需要处理的图像；
    第二个参数是图像的深度(就是每个点的颜色数)，-1表示采用的是与原图像相同的深度。目标图像的深度必须大于等于原图像的深度；
    dx和dy表示的是求导的阶数，0表示这个方向上没有求导，一般为0、1、2。

其后是可选的参数：

    dst不用解释了；
    ksize是Sobel算子的大小，必须为1、3、5、7。
    scale是缩放导数的比例常数，默认情况下没有伸缩系数；
    delta是一个可选的增量，将会加到最终的dst中，同样，默认情况下没有额外的值加到dst中；
    borderType是判断图像边界的模式。这个参数默认值为cv2.BORDER_DEFAULT。
@author: xhj
'''
import cv2
import numpy as np


def sobel_figureEdge(img):
    #求导后图像深度可能大于uint8，因此用uint16表示
    x = cv2.Sobel(img, cv2.CV_16S,1,0)
    y = cv2.Sobel(img, cv2.CV_16S,0,1)
    
    #图像深度转为正常的uint8
    absx = cv2.convertScaleAbs(x)
    absy = cv2.convertScaleAbs(y)
    
    #由于在x，y两个方向上sobel，还需要合并起来
    dst = cv2.addWeighted(absx,0.5, absy,0.5, 0)
    
    cv2.imshow('img_org',img)
    cv2.imshow('img_sobel',dst)
    
    cv2.waitKey(0)
    cv2.destroyAllWindows()



if __name__ == '__main__':
    img = cv2.imread(r'E:\pyopencv\imgs\stuff.jpg')
    sobel_figureEdge(img)
    