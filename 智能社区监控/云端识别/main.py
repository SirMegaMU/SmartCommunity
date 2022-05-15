import urllib.request
import cv2
import numpy as np

url='http://192.168.137.205/cam-hi.jpg'
def face_detection(image):
	# 转成灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 创建一个级联分类器 加载一个.xml分类器文件 它既可以是Haar特征也可以是LBP特征的分类器
    face_detecter = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    body_detecter = cv2.CascadeClassifier('haarcascade_fullbody.xml')
    # 多个尺度空间进行人脸检测   返回检测到的人脸区域坐标信息
    faces = face_detecter.detectMultiScale(image=gray, scaleFactor=1.1, minNeighbors=5)
    bodys = body_detecter.detectMultiScale(image=gray, scaleFactor=1.1, minNeighbors=5)
    print('检测人脸信息如下L:', faces ,'\n检测人体信息如下:',bodys)
    for x, y, w, h in faces:
        # 在原图像上绘制矩形标识
        cv2.rectangle(img=image, pt1=(x, y), pt2=(x+w, y+h), color=(0, 0, 255), thickness=2)
    for x, y, w, h in bodys:
        cv2.rectangle(img=image, pt1=(x, y), pt2=(x+w, y+h), color=(0, 255, 0), thickness=2)
    cv2.imshow('result', image)


while True:
    imgResp=urllib.request.urlopen(url)
    imgNp=np.array(bytearray(imgResp.read()),dtype=np.uint8)
    img=cv2.imdecode(imgNp,-1)
    face_detection(img)

    # all the opencv processing is done here
    if ord('q')==cv2.waitKey(10):
        exit(0)
