# -*- coding:utf-8 -*-
import cv2
import numpy as np
import time
  
camera = cv2.VideoCapture(0) # 参数0表示第一个摄像头
# 判断视频是否打开
if (camera.isOpened()):
    print('Open')
else:
    print('摄像头未打开')
background = cv2.imread('img.png',0)#读入一幅图像
es = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 4))
while True:
    # 按'q'健退出循环
    key = cv2.waitKey(1) & 0xFF
    # 读取视频流
    grabbed, img = camera.read()
    gray1 = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray1, (21, 21), 0)#可在这添加处理程序
    #！！！等相机稳定后按下W选择背景
    if key == ord('w'):
        background = gray
        print('背景已选定')
    diff = cv2.absdiff(gray, background)
    binary = cv2.threshold(diff, 25, 255, cv2.THRESH_BINARY)[1]#二值化阈值处理
    dilation = cv2.dilate(binary, es, iterations=2) # 形态学膨胀<--可在这添加处理程序
    contours, hierarchy = cv2.findContours(dilation.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    for c in contours:
        # 对于矩形区域，只显示大于给定阈值的轮廓，所以一些微小的变化不会显示。
        if cv2.contourArea(c) < 1500: 
            continue
        (x, y, w, h) = cv2.boundingRect(c) # 该函数计算矩形的边界框
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow('img', img)
    cv2.imshow('dilation', dilation)
 
    if key == ord('q'):
        break
camera.release()#ubuntu一定要释放相机资源否则要重启才能再次使用
cv2.destroyAllWindows()