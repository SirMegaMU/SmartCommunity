import cv2


# 加载视频
cap = cv2.VideoCapture('xinbaodao.flv')
# 创建一个级联分类器 加载一个.xml分类器文件 它既可以是Haar特征也可以是LBP特征的分类器
face_detect = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
body_detecter = cv2.CascadeClassifier('haarcascade_fullbody.xml')
    
while True:
    # 读取视频片段
    ret, frame = cap.read()
    if not ret:  # 读完视频后falg返回False
        break
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5)
    # 灰度处理
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # 多个尺度空间进行人脸检测   返回检测到的人脸区域坐标信息
    face_zone = face_detect.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=8)
    body_zone = body_detecter.detectMultiScale(image=gray, scaleFactor=1.1, minNeighbors=5)
    
    # 绘制矩形和圆形检测人脸
    for x, y, w, h in face_zone:
        cv2.rectangle(frame, pt1=(x, y), pt2=(x + w, y + h), color=[0, 0, 255], thickness=2)
    for x, y, w, h in body_zone:
        cv2.rectangle(frame, pt1=(x, y), pt2=(x+w, y+h), color=(0, 255, 0), thickness=2)
    
    # 显示图片
    cv2.imshow('video', frame)
    # 设置退出键和展示频率
    if ord('q') == cv2.waitKey(40):
        break

# 释放资源
cv2.destroyAllWindows()
cap.release()