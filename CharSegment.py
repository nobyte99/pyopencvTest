# coding: utf-8
'''
Created on 2016年12月21日

字符分割算法，目的是为了从提取的一副标准车牌图像中，分割为一个一个的字符图像；方便后续的字符识别模块进行字符识别，最终转换为车牌号码
字符分割算法流程：（该算法输入必须是一个标准的车牌图像，如  ..\imgs\resources\image\chars_identify.jpg）
pre_1、车牌颜色判断《pass，不处理，输入图像应该为一个灰度图像》  
pre_2、车牌图像二值化 
3、水平方向字符分割， 目的去除车牌图像中的边框和周围的四个柳钉，车牌识别仅仅关心汉字、字母和数字 
4、垂直方向字符分割，目的利用垂直投影对各个字符进行分割，分割为一个一个的字符图像。

@author: xhj
'''

import Mylbp as lbp
import cv2
import numpy as np

import matplotlib.pyplot as plt



'''
得到输入的一行中连续1的最大长度，如 11100110，最多有3个连续的1

'''
def GetMaxLengthOfSeg1(Line):
    listLength=[]
    iLen = len(Line)
    iPre = Line[0]
    iChangeCount=0
    for i in xrange(iLen-1):
        itmp = Line[i]
        j = i+1
        jtmp = Line[j]
        iPre = (iPre + jtmp) if jtmp == 1 else 0
        listLength.append(iPre)
        iChangeCount += jtmp ^ itmp
        
    
    return max(listLength), iChangeCount
        

# clip img
def clipImg(img, x,y,w,h):
    #clipImg = cv2.getRectSubPix(img, (x,y),(h,w))
    clipImg = img[y:y+h,x:x+w]
    return clipImg      

# clip img
def Contour_x(contour):
    (x,y,w,h) = cv2.boundingRect(contour)
    return x


'''
执行水平扫描的Fisher准则分割，
算法流程：来自于《车牌字符分割及识别算法研究》，白建华，西安电子科技大学
# 1、在输入图像上上下扩展H/5，设原图高度H，上扩H/5,下扩H/5，共阔2H/5作为待处理图像
# 2、使用下列水平差分公式求取图像的水平差分图像
#     水平差分公式：
#     g(i,j) = | f(i,j) - f(i,j+1) |
#     
#         其中，f(i,j)为原图像在i,j出的灰度值，i为图像高度，j为图像宽度
#     g(i,j)为获得差分图像在原图处的灰度值
#     
# 3、将水平差分图像作为输入图像，利用Fisher判别准则求取车牌图像的 上下边界
# Fisher判别准则：
算法的精髓在于充分利用车牌区域的水平投影和垂直投影进行车牌字符切分，并且利用一些规则进行异常车牌的处理。在论文的图3.1中可以看出这种方法的有效性。
该算法非常简单，实现非常容易。效果一般，需要进行后期异常处理。
1、进行水平投影，获得车牌字符区域
2、进行垂直投影，获得字符车牌区域


除了水平投影和垂直投影进行分割之外，还有别的方法可以进行分割比如论文《车牌字符分割与识别算法的研究与实现》 安徽工业大学，号称效果很好？


@param img: 输入的灰度图像
@return：
          水平分割后的图像
'''

'''
进行水平投影，很简单就是操作numpy矩阵，进行x轴的统计。
@param img: 输入的二值图像
@return: 
    返回的车牌字符区域
'''
def GetLevelSeg(img):
    imgT = img.T
    LevelValues = sum(imgT)
    
    #找到距离波峰最近的两个LevelValues的两个波底进行区域切分
    x = np.linspace(0, len(LevelValues), len(LevelValues))
    plt.figure(figsize=(80,40))
    #LevelValuesfft = np.fft.fft(LevelValues)
    print len(x),len(LevelValues)
    iLen = len(LevelValues)
    for i in xrange(1,iLen-1,1):
        LevelValues[i] = sum(LevelValues[i-1:i+2])/3 
    #plt.plot(x,LevelValues.T,label="levelValues",color="red",linewidth=2)
    
#     #求LevelValues的均值，并且将LevelValues二值化 begin    
#     iMean = (float(sum(LevelValues))/iLen)*0.55  #这个做法不合理，应该根据行中跳变来计算更加合理
#     for i in xrange(iLen):
#         LevelValues[i] = 1 if LevelValues[i] > iMean else 0
#     plt.plot(x,LevelValues.T,label="levelValues",color="green",linewidth=2)
#     plt.title("PyPlot First Example")
#  
#     plt.legend()
#     plt.show()
#     #从上述的LevelValues的中间，分别向上、下扫描第一个值为0的位置，就是车牌的上下边界
#     iMiddlePos = iLen/2
#     # 向上扫描
#     for iTop in xrange(iMiddlePos,0,-1):
#         if LevelValues[iTop] == 0:
#             break
#     for iBottom in xrange(iMiddlePos,iLen, 1):
#         if LevelValues[iBottom] == 0:
#             break
#     #根据上下边界切分车牌上下边界
#     imgNoTopBottom = img[iTop:iBottom][:][:]
#     #imgNoTopBottom = imgNoTopBottom.T
#     #求LevelValues的均值，并且将LevelValues二值化 end
    
    
    #求LevelValues的均值，并且将LevelValues二值化 begin    ,LevelValues为行跳变数，而不是和值
    for i in xrange(0,iLen,1):
        t  = img[i]
        _,tmp = GetMaxLengthOfSeg1(t)
        LevelValues[i] = tmp
    iMean = 7  #这个做法不合理，应该根据行中跳变来计算更加合理，默认跳变至少要大于7次；跳变的水平切割要比其他方式好的多的多。
    for i in xrange(iLen):
        LevelValues[i] = 1 if LevelValues[i] >= iMean else 0
    plt.plot(x,LevelValues.T,label="levelValues",color="green",linewidth=2)
    plt.title("PyPlot First Example")
  
    plt.legend()
    plt.show()
    #从上述的LevelValues的中间，分别向上、下扫描第一个值为0的位置，就是车牌的上下边界
    iMiddlePos = iLen/2
    # 向上扫描
    for iTop in xrange(iMiddlePos,0,-1):
        if LevelValues[iTop] == 0:
            break
    for iBottom in xrange(iMiddlePos,iLen, 1):
        if LevelValues[iBottom] == 0:
            break
    #根据上下边界切分车牌上下边界
    imgNoTopBottom = img[iTop:iBottom][:]

    lbp.showImg("imgNoTopBottom", imgNoTopBottom, True)
    
    # 利用垂直投影和车牌先验知识对imgNoTopBottom进行垂直分割，1、采用垂直投影分割、2采用字符轮廓分割、3、采用连通区域分割
    iCharHeight = iBottom-iTop+1 # 字符高度
    iCharWidth  = iCharHeight/2  # 字符宽度
    iMarginInChars = 12/90*iCharHeight # 字符间隔
    iSpotWidth = 10/90*iCharHeight     # 车牌中小圆点宽度
    
    #2、采用字符轮廓法进行分割，轮廓法处理的是上述已经处理了上下边界的图像imgNoTopBottom
    # 绘出轮廓    
    contours, _ = cv2.findContours(imgNoTopBottom.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    cv2.drawContours(imgNoTopBottom,contours,-1,(255,0,0),3)
    colors = [(0,255,0),(255,0,0),(0,0,255)]
    sortedContours = sorted( contours, key = Contour_x, reverse = False ) 
    for cnt in sortedContours: #对于所有的轮廓，查找外接矩形，判断是否是一个汉字或者一个数字或字母
#         Box2DRect = cv2.minAreaRect(cnt)         
        (x,y,w,h) = cv2.boundingRect(cnt)
        k = float(w)/h
        print x,y,w,h,k
        clipImg1 =  clipImg(imgNoTopBottom, x,y,w,h)
        lbp.showImg('DrawRectImg',clipImg1, True)
        if k > 0.5 * (1.25) or k < 0.5 * 0.75 or h < 10 or h > 35:
            continue
#         DrawRectImg = imgNoTopBottom.copy()
#         cv2.rectangle(DrawRectImg,(x,y),(x+w,y+h),colors[i%3],2)
#         cv2.drawContours(DrawRectImg, cnt,-1, colors[i%3],3)
        i+=1
        clipImg1 =  clipImg(imgNoTopBottom, x,y,w,h)
        lbp.showImg('DrawRectImg',clipImg1, True)
#     lbp.showImg("imgNoTopBottomContours", imgNoTopBottom, True)
  
    
    
    
    
    

        
     
        
    

# 执行图像二值化操作，暂时使用最基本的二值化方法
def GetImgBin(img):
    # 二值化
    ret, binImg = cv2.threshold(img,70,250,cv2.THRESH_OTSU | cv2.THRESH_BINARY )
    return binImg

     

strJPGFilePath=r'../imgs/resources/image/chars_identify.jpg'
def test_main():
    # open jpg
    img = cv2.imread(strJPGFilePath,0)  # 读取图像    
    binImg = GetImgBin(img)
    lbp.showImg("test", binImg, True)
    
    GetLevelSeg(binImg)
    


if __name__ == '__main__':
    test_main()