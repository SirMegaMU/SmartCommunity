import cv2
import numpy as np

# 读取图片时似乎是要用绝对路径？

# 图片大小重塑
input_shape = (300,300)
# 人名列表
id_dict = {}
# 已经被识别有用户名的人脸个数
Total_face_num = 0  
# 加载人脸检测模型
faceDetector = cv2.FaceDetectorYN_create(model='yunet.onnx', config='', input_size=input_shape)
# 加载人脸识别模型
faceRecognizer = cv2.FaceRecognizerSF_create(model='face_recognizer_fast.onnx', config='')
# 读取图片
image1 = cv2.imread('avatar.jpg')
image2 = cv2.imread('detected.jpg')
#改变图片大小
image1 = cv2.resize(image1,input_shape)
image2 = cv2.resize(image2,input_shape)
# 进行人脸检测
face1_detect = faceDetector.detect(image1)
face2_detect = faceDetector.detect(image2)
if face1_detect[1] is None or face2_detect[1] is None:
    print('------ 未发现人脸！')
    exit(0)
# 人脸对比
faces_detect = (face1_detect[1], face2_detect[1])
images = (image1, image2)

# 框出人脸并画出人脸的关键点
for i in range(len(images)):
    for face_index, face_coords in enumerate(faces_detect[i]):

        thickness = 2

        # 准确度
        accuracy = face_coords[-1]

        # 坐标转成int类型
        coords = face_coords[:-1].astype(np.int32)

        # 框出人脸
        cv2.rectangle(images[i], (coords[0], coords[1]), (coords[0] + coords[2], coords[1] + coords[3]), (0, 255, 0), thickness)

        # 画出左右瞳孔、左右嘴角、鼻尖的位置
        cv2.circle(images[i], (coords[4], coords[5]), 2, (255, 0, 0), thickness)
        cv2.circle(images[i], (coords[6], coords[7]), 2, (0, 0, 255), thickness)
        cv2.circle(images[i], (coords[8], coords[9]), 2, (0, 255, 0), thickness)
        cv2.circle(images[i], (coords[10], coords[11]), 2, (255, 0, 255), thickness)
        cv2.circle(images[i], (coords[12], coords[13]), 2, (0, 255, 255), thickness)

        # 显示准确度
        cv2.putText(images[i], 'The accuracy of: {:.2f}'.format(accuracy), (1, 16), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

        # 显示图片
        cv2.imshow('image{:d}'.format(i), images[i])

# 人脸对齐,alignCrop返回的是人脸图像
face1_align = faceRecognizer.alignCrop(image1, face1_detect[1])
face2_align = faceRecognizer.alignCrop(image1, face2_detect[1])
# 提取维度特征
face1_feature = faceRecognizer.feature(face1_align)
face2_feature = faceRecognizer.feature(face2_align)
# 进行对比
cosine_similarity_threshold = 0.363
l2_similarity_threshold = 1.128

# 人脸识别（余弦匹配方式）
cosine_score = faceRecognizer.match(face1_feature, face2_feature, cv2.FaceRecognizerSF_FR_COSINE)

# 人脸识别（L2匹配方式）
l2_score = faceRecognizer.match(face1_feature, face2_feature, cv2.FaceRecognizerSF_FR_NORM_L2)

msg = '不是同一个人'
if cosine_score >= cosine_similarity_threshold:
    msg = '是同一个人'
print('------ 两张人脸图像%s！余弦阈值：%0.3f，余弦值：%0.3f。\n（注：余弦值越高表示相似度越高，最大值为1.0）' % (msg, cosine_similarity_threshold, cosine_score))


msg = '不是同一个人'
if l2_score <= l2_similarity_threshold:
    msg = '是同一个人'
print('------ 两张人脸图像%s！L2距离：%0.3f，阈值：%0.3f。\n（注：L2距离越低表示相似度越高，最小值为0.0）' % (msg, l2_score, l2_similarity_threshold))

cv2.waitKey()




