# coding: utf-8
# 将jpg从BGR转换为HSV空间，并设置HSV区域到蓝色区域，获取蓝色物体

import cv2
import numpy as np
import Mylbp as lbp

isDebug=True

#main_test1
def PlateLocate_Color(img):
    
    cv2.namedWindow('frame')
    cv2.imshow('frame', img)
    k = cv2.waitKey(0)
    
    cv2.destroyAllWindows()
    img = cv2.GaussianBlur(img,(5,5),0)
    hsvImg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower_blue = np.array([100,90,90])  #0.35
    upper_blue = np.array([140,255,255]) # 1
    
    lower_red = np.array([0,150,150])
    upper_red = np.array([10,255,255])
    
    #根据阈值构建掩盖模型
    mask1 = cv2.inRange(hsvImg,lower_blue, upper_blue)
    mask2 = cv2.inRange(hsvImg,lower_red, upper_red)
    
    mask = cv2.bitwise_or(mask1, mask2)
    
    
    #bit
    res = cv2.bitwise_and(img,img, mask = mask1)
    
    
    
    cv2.imshow('frame', img)
    cv2.imshow('mask',mask)
    cv2.imshow('res',res)
    k = cv2.waitKey(0)
    
    cv2.destroyAllWindows()

import random

def subimage(image, center, theta, width, height): #抠图并旋转
    theta *= np.pi / 180 # convert to rad

    v_x = (np.cos(theta), np.sin(theta))
    v_y = (-np.sin(theta), np.cos(theta))
    s_x = center[0] - v_x[0] * (width / 2) - v_y[0] * (height / 2)
    s_y = center[1] - v_x[1] * (width / 2) - v_y[1] * (height / 2)

    mapping = np.array([[v_x[0],v_y[0], s_x],
                        [v_x[1],v_y[1], s_y]])

    return cv2.warpAffine(image,mapping,(width, height),flags=cv2.WARP_INVERSE_MAP,borderMode=cv2.BORDER_REPLICATE)


#main_test1
def PlateLocate_Sobel(img):    
    isClose = True
    
    lbp.showImg('frame', img, isClose)
    
    img = cv2.GaussianBlur(img,(5,5),0) # 高斯模糊，5
    grayImg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY) #会度化
    
    
    #根据sobel算子去轮廓
    x = cv2.Sobel(grayImg, cv2.CV_16S,1,0,3)
    y = cv2.Sobel(grayImg, cv2.CV_16S,0,1,3)
    
    sobelImgx = cv2.convertScaleAbs(x)
    sobelImgy = cv2.convertScaleAbs(y)
    
    #由于在x，y两个方向上sobel，还需要合并起来
    sobelImg = cv2.addWeighted(sobelImgx,1, sobelImgy,0, 0)
    
    cv2.imshow('gray', grayImg)

    lbp.showImg('gray', grayImg, False)
    lbp.showImg('sobel',sobelImg, isClose)

    
    # 二值化
    ret, binImg = cv2.threshold(sobelImg,70,250,cv2.THRESH_OTSU | cv2.THRESH_BINARY)

    lbp.showImg('binary',binImg, isClose)
    
    # close operation, step 1, expand; step 2, shrink
    iMorphSizeWidth = 17
    iMorphSizeHeight = 3
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (iMorphSizeWidth, iMorphSizeHeight))
    closedImg = cv2.morphologyEx(binImg, cv2.MORPH_CLOSE, rectKernel)
    # 下列操作也许可以提高精度
    #closedImg = cv2.erode(closedImg,None, iterations = 4)
    #closedImg = cv2.dilate(closedImg,None, iterations = 4)

    lbp.showImg('closed',closedImg, isClose)

    
    # 绘出轮廓
    
    contours, _ = cv2.findContours(closedImg.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
#     cv2.drawContours(img,contours,-1,(255,0,0),3) 
#     cv2.imshow('contourImg',img)
#     k = cv2.waitKey(0)
#     cv2.destroyAllWindows()
    
    # 根据矩形面积对contour排序
    sortedContours = sorted( contours, key = cv2.contourArea, reverse = True )
    
    
    #判断矩形是否是一个车牌区域，通过宽高比（标准3.14），面积（标准440*140），倾斜角度（》30不对）进行判断
    MayBeCarNoContours=[]
    for cnt in sortedContours:
        Box2DRect = cv2.minAreaRect(cnt)
        ((x,y),(w,h),angle) = Box2DRect
        
    colors = [(0,255,0),(255,0,0),(0,0,255)]
    i=0
    
    listMayBeImg = []
    
    # 绘制边界矩形
    for cnt in sortedContours:
        Box2DRect = cv2.minAreaRect(cnt)
        box = np.int0(cv2.boxPoints(Box2DRect))
        print Box2DRect 
        ((center_x,center_y),(w,h),angle) = Box2DRect
        if h==0 or abs(angle+90) > 30 or cv2.contourArea(cnt) / 440*140 <0.9:
            continue
#         
#         MayBeCarNoContours.append(cnt)
#         print 'one',w,h ,float(w)/h, w*h, angle
        #DrawRectImg = cv2.rectangle(img,(x,y),(x+w, y+h),(0,255,0),2)
         
        (x,y,w,h) = cv2.boundingRect(cnt)
        print (x,y,w,h)
        DrawRectImg = img.copy()
        cv2.rectangle(DrawRectImg,(x,y),(x+w,y+h),colors[i%3],2)
        cv2.drawContours(DrawRectImg, cnt,-1, colors[i%3],3)
        i+=1

        lbp.showImg('DrawRectImg',DrawRectImg, isClose)

        
        #抓出图像，显示，然后旋转扶正 ,最后，缩放为为（136,36）大小的图片，送入SVM模型进行是否为车牌图片的判断。        
        clipImg1 = clipImg(img, x,y,w,h)
        RightImg=RotateImg(img, cnt)
        RightImg = cv2.resize(RightImg,(136,36))
        
        lbp.showImg('RightImg',RightImg, isClose)
        listMayBeImg.append(RightImg)
    
    return listMayBeImg

# clip img
def clipImg(img, x,y,w,h):
    #clipImg = cv2.getRectSubPix(img, (x,y),(h,w))
    clipImg = img[y:y+h,x:x+w]
    cv2.imshow('ClipImg', clipImg)
    k = cv2.waitKey(0)
    cv2.destroyAllWindows()
    return clipImg

import math
# 选择图像扶正
def RotateImg(img, cnt):
    #得到旋转角度 
    center, wh, angle = cv2.minAreaRect(cnt)
    
    angle = angle+90
    wh = (int(math.ceil(wh[0])),int(math.ceil(wh[1])))
    root_mat = cv2.getRotationMatrix2D(center, angle, 1)
    wh = (wh[1],wh[0])
    ( cols,rows, _) = img.shape
    rotated = cv2.warpAffine(img, root_mat, ( rows, cols), flags=cv2.INTER_CUBIC)

    RotateIMG = cv2.getRectSubPix(rotated, wh, center)    
    
    cv2.imshow('RotateIMG', RotateIMG)
    k = cv2.waitKey(0)
    cv2.destroyAllWindows()
    return RotateIMG

#旋转图像，just for test rotate
def RotateImgDo(img, angle):
    ( cols,rows,_) = img.shape
    center = (int(rows/2), int(cols/2))
    cv2.circle(img, center, 5,(0,255,0),-1)
    root_mat = cv2.getRotationMatrix2D(center, angle, 1)
    
    rotated = cv2.warpAffine(img, root_mat, ( rows, cols), flags=cv2.INTER_CUBIC)
    RotateIMG = cv2.getRectSubPix(rotated, ( rows-1300, cols-200 ), center)
    #  cv2.warpAffine(img,mapping,(width, height),flags=cv2.WARP_INVERSE_MAP,borderMode=cv2.BORDER_REPLICATE)
    
    cv2.imshow('RotateIMG', RotateIMG)
    k = cv2.waitKey(0)
    cv2.destroyAllWindows()
    #return RotateIMG

# 要加载SVM训练的车牌区域判断，首先需要提取图像特征，然后加载SVM模型文件，之后才能判断

#加载SVM模型文件,返回SVMModel
def GetSVMModel(strModelFile):    
    objSVMModel = cv2.SVM()
    objSVMModel.load(strModelFile)
    return objSVMModel

'''    
 抽取图像特征,用的easyPR，必须符合easyPR提取的特征
 注意，这里抽取的LBP特征
 @param MayBeImg: 输入的图像
 @return: 
        返回抽取的LBP图谱 
 '''
def ExtractFeatureFromImg(MayBeImg):
    #输入图片转换为灰度图
    img = cv2.cvtColor(MayBeImg, cv2.COLOR_RGB2GRAY) #灰度化
    return lbp.ExtractLBPFromIMG(img)
    
    
      

strJPGFilePath=r'../imgs/resources/image/plate_locate.jpg'
strModelFile = r'../imgs/resources/model/svm.xml'
def test_main():
    # open jpg
    img = cv2.imread(strJPGFilePath,cv2.IMREAD_COLOR)  # 读取图像
    print  img.shape
    listMayBeImg = PlateLocate_Sobel(img)
    #RotateImgDo(img,0)
    #clipImg(img,23,1,444,255)
    #得到SVM
    objSVMModel = GetSVMModel(strModelFile)
    for MayBeImg in listMayBeImg:
        y_val_svm  = objSVMModel.predict(MayBeImg)        
        print y_val_svm


from cv2.ml import *

# ann 字符识别
def ann2Char():
    
    neuralClassify = cv2.ml.ANN_MLP_create()
    neuralClassify.setLayerSizes(np.array([9, 5, 9], dtype=np.uint8))
    
    

if __name__ == '__main__':
    test_main()
    
