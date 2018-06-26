#!\usr\bin\python.exe
#-*- coding: UTF-8 -*-
"""
本文件仅仅处理ascII输入的latin维文，对于输入的unicode编码的可能无法处理！
文件将输入的latin维文单词切分成音节的形式输入。
"""
import sys

# Definition for an interval.
# class Interval(object):
#     def __init__(self, s=0, e=0):
#         self.start = s
#         self.end = e

# class Solution(object):
#     def maximumGap(self, nums):
#         """
#         :type nums: List[int]
#         :rtype: int
#         """
#         iLen = len(nums)
#         if iLen <2:
#             return 0
#         
#         import math
#         #基数排序
#         def baseSquence(nums):
#             tong = {}
#             listReturn = nums[:]
#             bian = int(math.floor(math.log10(max(nums))))+1
#             print bian
#             for b in range(bian):
#                 print listReturn
#                 # 分配
#                 for i,c in enumerate(listReturn):                    
#                     j = c//(10**b)%10
#                     tong[j] = tong.get(j,[])+[c]
#                 print tong
#                 listReturn = []
#                 # 收集
#                 for i in range(10):
#                     listReturn += tong.get(i,[])
#                 tong.clear()
#             return listReturn
#         
#         
#         numss =  baseSquence(nums)
#         return numss
#         iLen = len(numss)
#         imax = 0 
#         for i in range(iLen-1):
#             ii = numss[i+1] - numss[i]
#             if ii > imax:
#                 imax = ii
#         return imax
            

# class Solution(object):
#     import sys
#     def calculateMinimumHP(self, dungeon):
#         """
#         :type dungeon: List[List[int]]
#         :rtype: int
#         """
#         x = len(dungeon)
#         if x ==0:
#             return 0
#         y = len(dungeon[0])
#         #所有的节点都填充路径最小值和当前值，
#         #当前值用于dp的迭代，而最小值，用于返回。
#         board = []
#         for i in range(x):
#             board.append([(-sys.maxint, -sys.maxint)]*y)
#         board[0][0] = (dungeon[0][0],dungeon[0][0])
#         iLenxy = (x,y)
#         visited=[]
#         visited.append((0,0))
#         iResult = [-sys.maxint]
#         # 我们限定上下左右都可以走动，那么只有同时更改了当前节点的（最大路径代价，到节点后的最大生命）的，才能够在本结点继续移动，否则，本结点不通
#         def isFind(visited,dungeon,board,pos_xy,iLenxy): # 从后向前搜
#             (x,y) = pos_xy
#             (iLenx,iLeny) = iLenxy
#             if board[x][y][0] <= iResult[0]:  #剪纸
#                 return
#                        
#             if x == iLenx-1 and y == iLeny-1:  #  todo判断是否到达了最终节点，到了就返回
#                 #print visited,'\n', board[iLenx-1][iLeny-1]
#                 if board[iLenx-1][iLeny-1][0] > iResult[0]:
#                     iResult[0] = board[iLenx-1][iLeny-1][0]
#                 #print iResult[0]
#                 return            
#             
#             # 上, x-1,y,是否可以从此节点向下走，取决于能够更新节点的值，能更新的，就能走，否则就不能走
#             if x-1 >=0 and (x-1,y) not in visited:
#                 #计算从posxy过来后，本结点的值
#                 (maxCost,CurCost) = board[x][y]
#                 #计算过本结点会耗费的值
#                 nextCost = CurCost + dungeon[x-1][y]
#                 netxtMaxCost = min(maxCost, nextCost)
#                 # 需要和当前节点已有的cost比较
#                 (nowMaxCost, nowNextCost ) = board[x-1][y]
#                                 
#                 # 判断是否更新，由于我们求最小的cost，因此如果maxcost变小，我们就更新
#                 if  nowMaxCost < netxtMaxCost: # 更新
#                     old = board[x-1][y]
#                     board[x-1][y] =(netxtMaxCost,nextCost)
#                     visited.append((x-1,y))
#                     #print visited,'\n', board
#                     isFind(visited,dungeon, board,(x-1,y), iLenxy)
#                     board[x-1][y] = old
#                     visited.remove((x-1,y))
#                 elif nowMaxCost == netxtMaxCost:
#                     if nextCost > nowNextCost:
#                         old = board[x-1][y]
#                         board[x-1][y] =(netxtMaxCost,nextCost)
#                         visited.append((x-1,y))
#                         #print visited,'\n', board
#                         isFind(visited,dungeon, board,(x-1,y), iLenxy)
#                         board[x-1][y] = old
#                         visited.remove((x-1,y))
#                     
#                 
#                     
#             # 下，x+1,y
#             if x+1 <iLenxy[0] and (x+1, y) not in visited:
#                 #计算从posxy过来后，本结点的值
#                 (maxCost,CurCost) = board[x][y]
#                 #计算过本结点会耗费的值
#                 nextCost = CurCost + dungeon[x+1][y]
#                 netxtMaxCost = min(maxCost, nextCost)
#                 # 需要和当前节点已有的cost比较
#                 (nowMaxCost, nowNextCost ) = board[x+1][y]
#                                 
#                 # 判断是否更新，由于我们求最小的cost，因此如果maxcost变小，我们就更新
#                 if  nowMaxCost < netxtMaxCost: # 更新
#                     old =board[x+1][y]                    
#                     board[x+1][y] =(netxtMaxCost,nextCost)
#                     visited.append((x+1,y))
#                     #print visited,'\n', board
#                     isFind(visited,dungeon, board,(x+1,y), iLenxy)
#                     board[x+1][y] = old
#                     visited.remove((x+1,y))
#                 elif nowMaxCost == netxtMaxCost:
#                     if nextCost > nowNextCost:
#                         old =board[x+1][y]
#                         board[x+1][y] =(netxtMaxCost,nextCost)
#                         visited.append((x+1,y))
#                         #print visited,'\n', board
#                         isFind(visited,dungeon, board,(x+1,y), iLenxy)
#                         board[x+1][y] = old
#                         visited.remove((x+1,y))
#                     
#             #zuo, x,y-1
#             if y-1 >=0 and (x,y-1) not in visited:
#                 #计算从posxy过来后，本结点的值
#                 (maxCost,CurCost) = board[x][y]
#                 #计算过本结点会耗费的值
#                 nextCost = CurCost + dungeon[x][y-1]
#                 netxtMaxCost = min(maxCost, nextCost)
#                 # 需要和当前节点已有的cost比较
#                 (nowMaxCost, nowNextCost ) = board[x][y-1]
#                                 
#                 # 判断是否更新，由于我们求最小的cost，因此如果maxcost变小，我们就更新
#                 if  nowMaxCost < netxtMaxCost: # 更新
#                     old = board[x][y-1]
#                     board[x][y-1] =(netxtMaxCost,nextCost)
#                     visited.append((x,y-1))
#                     #print visited,'\n', board
#                     isFind(visited,dungeon, board,(x,y-1), iLenxy)
#                     board[x][y-1] = old
#                     visited.remove((x,y-1))
#                 elif nowMaxCost == netxtMaxCost:
#                     if nextCost > nowNextCost:
#                         old = board[x][y-1]
#                         board[x][y-1] =(netxtMaxCost,nextCost)
#                         visited.append((x,y-1))
#                         #print visited,'\n', board
#                         isFind(visited,dungeon, board,(x,y-1), iLenxy)
#                         board[x][y-1] = old 
#                         visited.remove((x,y-1))
#                     
#                         
#             #you, x,y+1
#             if y+1 <iLenxy[1] and (x,y+1) not in visited:
#                 #计算从posxy过来后，本结点的值
#                 (maxCost,CurCost) = board[x][y]
#                 #计算过本结点会耗费的值
#                 nextCost = CurCost + dungeon[x][y+1]
#                 netxtMaxCost = min(maxCost, nextCost)
#                 # 需要和当前节点已有的cost比较
#                 (nowMaxCost, nowNextCost ) = board[x][y+1]
#                                 
#                 # 判断是否更新，由于我们求最小的cost，因此如果maxcost变小，我们就更新
#                 if  nowMaxCost < netxtMaxCost: # 更新
#                     old = board[x][y+1]
#                     board[x][y+1] =(netxtMaxCost,nextCost)                    
#                     visited.append((x,y+1))
#                     #print visited,'\n', board
#                     isFind(visited,dungeon, board,(x,y+1), iLenxy)
#                     board[x][y+1] = old
#                     visited.remove((x,y+1))
#                 elif nowMaxCost == netxtMaxCost:
#                     if nextCost > nowNextCost:
#                         old = board[x][y+1]                        
#                         board[x][y+1] =(netxtMaxCost,nextCost)
#                         visited.append((x,y+1))
#                         #print visited,'\n', board
#                         isFind(visited,dungeon, board,(x,y+1), iLenxy)
#                         board[x][y+1] = old 
#                         visited.remove((x,y+1))   
#             
#             
#         isFind(visited,dungeon,board,(0,0),iLenxy)
#         
#         cost = iResult[0]
#         if cost <=0:
#             cost = -cost
#             return cost+1
#         else:
#             return 1

class Solution(object):
    def RectangleArea(self, heights, i,j):
        #if i != j:
        minValue = min(heights[i:j+1])
        #else:
        #    minValue = heights[i]
        #print i,j, minValue
        return (j-i+1)*minValue
    def largestRectangleArea(self, heights):
        """
        :type heights: List[int]
        :rtype: int
        """
        # 使用stack进行操作，
        stack=[]
        iLen = len(heights)
        if iLen == 0:
            return 0
        # 第一个元素进站
        i = 0
        heights.append(-1)
        iLen +=1
        minHeight = -1
        
        i=0
        while i < iLen:
            print stack, i, minHeight
            if len(stack) == 0 or heights[stack[-1]] <= heights[i]:
                stack.append(i)
                i+=1
                continue
            #出栈计算所求大小
            nowHeight = stack[-1]
            stack.pop()
            size=0;
            if(len( stack )==0):
                size=heights[nowHeight]*i;
            else:
                size=heights[nowHeight]*(i-stack[-1]-1);
            
            minHeight=max(size ,minHeight)
  
        return minHeight

        
            
        
def findEle(strr):
        iLen = len(strr)
        if iLen == 0:
            return ''
        i = 1
        while i < iLen:
            if strr[i] != '/':
                i+=1
            else:
                break
        return (strr[0:i+1], strr[i:])    

def removeLast(strr):
        iLen = len(strr)
        if iLen == 0:
            return ''
        i = 1
        while i<=iLen:
            i+=1
            if strr[-i] == '/':
                return strr[:-i+1]
        return '/'                                

class Solutions(object):
    def newInteger(self, n):
        """
        :type n: int
        :rtype: int
        """
        def integ(n):
            print n
            if n<9:
                return n
            gewei = n%9
            qita = n//9
            if qita >=10:
                qita = integ(qita)
            
            return int(str(qita)+str(gewei))
        
        return integ(n)                
                
                
        
if __name__ == "__main__":
    
    s = Solutions()
    print s.newInteger(100)
 
      

    
#     path="/a/./b/../../c/"
#     strr = '' 
#     print findEle(path)
#     print removeLast(path)
