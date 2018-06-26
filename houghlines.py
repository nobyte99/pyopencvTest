# coding: utf-8
'''
Created on 2014年9月28日

@author: xhj
'''

import cv2
import numpy as np

def LineDetect(img):
    '''
    输入必须是二值图像
    '''
    #图像二值化
    img = cv2.GaussianBlur(img,(3,3),0) 
    edges = cv2.Canny(img, 50, 150, apertureSize=3)
    #二值化
    lines = cv2.HoughLines(edges, 1, np.pi/180, 118)
    result = img.copy()  
    for line in lines[0]:  
        rho = line[0] #第一个元素是距离rho  
        theta= line[1] #第二个元素是角度theta  
        print rho  
        print theta  
        if  (theta < (np.pi/4. )) or (theta > (3.*np.pi/4.0)): #垂直直线  
                    #该直线与第一行的交点  
            pt1 = (int(rho/np.cos(theta)),0)  
            #该直线与最后一行的焦点  
            pt2 = (int((rho-result.shape[0]*np.sin(theta))/np.cos(theta)),result.shape[0])  
            #绘制一条白线  
            cv2.line( result, pt1, pt2, (255))  
        else: #水平直线  
            # 该直线与第一列的交点  
            pt1 = (0,int(rho/np.sin(theta)))  
            #该直线与最后一列的交点  
            pt2 = (result.shape[1], int((rho-result.shape[1]*np.cos(theta))/np.sin(theta)))  
            #绘制一条直线  
            cv2.line(result, pt1, pt2, (255), 1) 
            
    cv2.imshow('Canny', edges )  
    cv2.imshow('Result', result)  
    
    # 概率分段直线检测
    lines = cv2.HoughLines(edges,1,np.pi/180,118)  
    result = img.copy()  
      
    #经验参数  
    minLineLength = 20
    maxLineGap = 2  
    lines = cv2.HoughLinesP(edges,1,np.pi/180,80,minLineLength,maxLineGap)  
    for x1,y1,x2,y2 in lines[0]:  
        cv2.line(img,(x1,y1),(x2,y2),(0,0,255),2)  
      
    cv2.imshow('Result1', img)  
    cv2.waitKey(0)  
    cv2.destroyAllWindows()   


if __name__ == '__main__':
    img = cv2.imread(r"E:\pyopencv\imgs\stuff.jpg", 0) #读入灰度图像 
    LineDetect(img)