# coding: utf-8
'''
Created on 2014年9月23日

通过定义特定的矩阵来形成图像元素（十字，椭圆，圆，矩形）等来对需要处理的图形进行
腐蚀erode或者膨胀dilate  运算，二种运算进行一定的顺序组合之后
生成的灰度图，进行二值化后就可以探测图像中的物体边缘

基本形态学原理， 开运算，闭运算的含义
闭运算用来连接被误分为许多小块的对象，而开运算用于移除由图像噪音形成的斑点。

@author: xhj
'''
import cv2
import numpy as np

def MorphologyProcess(img):
    '''
       输入灰度图像，得到图像的腐蚀和膨胀结果，最终输出图像中物体的边缘二值图像
    '''
    # 定义图像元素
    cross = np.zeros((5,5),np.uint8)
    cross[:,2]=1
    cross[2,:]=1
    
    # 腐蚀， 图像总物体边缘收缩
    imgerode=  cv2.erode(img, cross)
    
    cv2.namedWindow('erode')
    cv2.imshow('erode',imgerode)
    
    # 膨胀, 图像中物体边缘膨胀
    imgdilate = cv2.dilate(img, cross)
    
    cv2.namedWindow('dilate')
    cv2.imshow('dilate',imgdilate)

    # 进行开运算， 
    imgopen = cv2.morphologyEx(img, cv2.MORPH_OPEN, cross)
    cv2.imshow('open',imgopen)
    
    # 闭运算
    imgclose = cv2.morphologyEx(img, cv2.MORPH_CLOSE, cross)
    cv2.imshow('close', imgclose)
    
    # 边缘检测，很简单，膨胀后图像-腐蚀后图像=图像中物体边缘， 之后进行二值化
    edgeimg = cv2.absdiff(imgdilate, imgerode)
    # 二值化
    retval, result = cv2.threshold(edgeimg, 40, 255, cv2.THRESH_BINARY)
    cv2.imshow('edgeBin',result)
    retval, result1 = cv2.threshold(edgeimg, 40, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow('edgeBin_inv',result1)
    # 二值化后取反
    edgeimgbininv= cv2.bitwise_not(result)
    cv2.imshow('edgeBininv',edgeimgbininv)

def MorphologJuezi(img):
    # 结合图像，为了处理橘子的边界，我们首先进行open运算，消除句子中包含的开运算小点点。再次基础上进行膨胀和腐蚀，后求边界
    # 定义图像元素
#     cross = np.zeros((5,5),np.uint8)
#     cross[:,2]=1
#     cross[2,:]=1
    
    cross = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))

    imgopen = cv2.morphologyEx(img, cv2.MORPH_OPEN, cross)
    cv2.imshow('edgeBin__1',imgopen)
    imgdilate = cv2.dilate(imgopen,cross)
    imgerode = cv2.erode(imgopen, cross)
    edgeimg = cv2.absdiff(imgdilate, imgerode)
    # 二值化
    retval, result = cv2.threshold(edgeimg, 40, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow('edgeBin_juezi',result)
    
if __name__ == '__main__':
    img = cv2.imread(r'E:\pyopencv\imgs\stuff.jpg')
    img1 = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    cv2.namedWindow('img')
    cv2.imshow('img',img1)
    
    MorphologyProcess(img1)
    MorphologJuezi(img1)
    cv2.waitKey(0)
    cv2.destroyAllWindows()