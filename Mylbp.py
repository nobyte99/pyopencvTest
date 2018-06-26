# coding: utf-8
''' 
Created on 2016年12月10日

提取图像的lbp特征，并打印并显示出来

@author: xhj
'''

import cv2
import numpy as np
import bitstring

# 得到code数字表示的一串的lbp数值中最小的一个
def GetMinLbpCode(code):    
    s = 255  
    for i in xrange(8):
        code  = (code << 1 | code >>7) & 0xFF 
        #print code,bin(code)
        if code < s:
            s = code
        
    return s

'''
按照基本3*3方式提取基本的lbp特征，生成图像的lbp图谱

@note:
lbp算法对于最外围像素的处理，并不假定外围像素为0或1，而是将行-2，列-2，仅仅计算内部像素 
basic 3*3 lbp algorithm：
对于图像中的一个3*3像素块，判断该像素块的中心像素和周边8个像素的比较，大则外围赋值为1，小则赋值为0，最终从（0,0）位置逆时针旋转得到一个8位数字，作为计算得到的3*3的lbp值

注意： 上述算法没有体现lbp的旋转不变形，如果要实现旋转不变性，应该求位置旋转得到的8个lbp数字中的最小的一个。
已经实现了旋转不变形，必须调用GetMinLbpCode（code）,就可以了得到不管怎么旋转任意图像获得的lbp图像都是同一个。

@param img: 输入的图像数据，注意必须是灰度图像
@return: 
    返回提取的lbp图谱,和输入的图像数据（行-2，列-2）相同
'''
def ExtractLBPFromIMG(img):
    # 建立lbp图谱，并初始化为0
    (row,colm) = img.shape
    row = row -2
    colm = colm -2
    lbpImg = np.zeros( (row, colm), np.uint8 )
    for i in xrange(row):
        ii = i+1
        for j in xrange(colm):
            code = lbpImg[i][j]            
            jj = j+1
            center = img[ii][jj]
            code = code | ((1 if img[i - 1][j - 1] >= center else 0) << 7);
            code = code | ((1 if img[i - 1][ j] >= center else 0) << 6);
            code = code | ((1 if img[i - 1][ j + 1] >= center else 0) << 5);
            code = code | ((1 if img[i][ j + 1] >= center else 0) << 4);
            code = code | ((1 if img[i + 1][ j + 1] >= center else 0) << 3);
            code = code | ((1 if img[i + 1][ j] >= center else 0) << 2);
            code = code | ((1 if img[i + 1][ j - 1] >= center else 0) << 1);
            code = code | ((1 if img[i][ j - 1] >= center else 0) << 0);
            lbpImg[i][j] = code  #GetMinLbpCode(code) 
    print lbpImg
    showImg("lbpimg",lbpImg, True)          
    


#strJPGFilePath=r'../imgs/resources/image/plate_locate.jpg'
strJPGFilePath=r'../imgs/o1.jpg'


def showImg(title,img,isClose):
    cv2.imshow(title, img)
    k = cv2.waitKey(0)
    if isClose:
        cv2.destroyAllWindows()

def test_main():
    # open jpg
    img = cv2.imread(strJPGFilePath,0)  # 读取图像
    (row,colm) = img.shape
    showImg("test", img, True)
    ExtractLBPFromIMG(img)
    
if __name__ == '__main__':
    # 打开灰度图像，并抽取特征
    test_main()
    