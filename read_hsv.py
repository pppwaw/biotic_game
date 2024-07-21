import cv2
import numpy as np


def get_hsv_value(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        hsv_value = hsv[y, x]
        print(f'HSV值: {hsv_value}')


# 读取图像
cap = cv2.VideoCapture('video/chlamy_PDMS.avi')
if not cap.isOpened():
    print('Cannot open camera')
    exit()
ret, image = cap.read()
cap.release()

# 转换为 HSV 色彩空间
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# 创建窗口并设置鼠标回调函数
cv2.namedWindow('HSV Picker')
cv2.setMouseCallback('HSV Picker', get_hsv_value)

while True:
    cv2.imshow('HSV Picker', image)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
