# coding: utf-8
'''
Created on 2014��9��28��

@author: xhj
'''
import cv2



if __name__ == '__main__':
    img = cv2.imread(r'E:\pyopencv\imgs\OpticalFlow0.jpg',0)
    
    equalimg = cv2.equalizeHist(img)
    cv2.imshow('img',img)
    cv2.imshow('equal',equalimg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()