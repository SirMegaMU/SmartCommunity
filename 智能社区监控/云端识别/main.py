import urllib.request
import cv2
import numpy as np

url='http://192.168.137.205/cam-hi.jpg'


def movement_detection(image):
    # 初始化差分器
    bg_subtractor = cv2.createBackgroundSubtractorKNN(detectShadows=True)
    erode_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3, 3))
    dilate_kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    # 捕捉帧，获取背景掩膜
    fg_mask = bg_subtractor.apply(image)
    # 对掩膜应用阈值获得黑白图像，进行平滑处理
    _, thresh = cv2.threshold(fg_mask, 244, 255, cv2.THRESH_BINARY)
    cv2.erode(thresh, erode_kernel, thresh, iterations=2)
    cv2.dilate(thresh, dilate_kernel, thresh, iterations=2)
    # 设置轮廓阈值
    contours, hier = cv2.findContours(thresh, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    # 绘制边框
    for c in contours:
        if cv2.contourArea(c) > 1000:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(image, (x, y), (x+w, y+h), (255, 255, 0), 2)
    return [image,fg_mask,thresh]

def human_detection(image):
	# 转成灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 创建一个Haar特征级联分类器
    face_detecter = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    body_detecter = cv2.CascadeClassifier('haarcascade_fullbody.xml')
    # 多个尺度空间进行人脸检测   返回检测到的人脸和人体区域坐标信息
    faces = face_detecter.detectMultiScale(image=gray, scaleFactor=1.1, minNeighbors=5)
    bodys = body_detecter.detectMultiScale(image=gray, scaleFactor=1.1, minNeighbors=5)
    print('检测人脸信息如下:', faces ,'\n检测人体信息如下:',bodys)
    # 在原图像上绘制区域标识
    for x, y, w, h in faces:
        cv2.circle(img=image, center=(x + w // 2, y + h // 2), radius=w // 2, color=[0, 0, 255], thickness=2)
    for x, y, w, h in bodys:
        cv2.rectangle(img=image, pt1=(x, y), pt2=(x+w, y+h), color=(0, 255, 0), thickness=2)
    return image


while True:
    imgResp=urllib.request.urlopen(url)
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img=cv2.imdecode(imgNp,-1)
    img1=human_detection(img)
    img2=movement_detection(img)
    cv2.namedWindow('human_detection', cv2.WINDOW_NORMAL | cv2.WINDOW_KEEPRATIO)
    cv2.imshow('human_detection', img1)
    # cv2.imshow('mog', img2[1])
    # cv2.imshow('thresh', img2[2])
    # cv2.imshow('movement_detection', img2[0])
    # 退出
    if ord('q')==cv2.waitKey(10):
        exit(0)
