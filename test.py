import cv2
import numpy as np


def process_maze_image(image_path):
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print("无法读取图像")
        return
    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 应用自适应阈值处理
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # 检测轮廓
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_CCOMP, cv2.CHAIN_APPROX_SIMPLE)

    # 创建一个掩膜来绘制轮廓
    mask = np.zeros_like(gray)
    cv2.drawContours(mask, contours, -1, (255), thickness=cv2.FILLED)

    # 使用掩膜分割图像
    segmented = cv2.bitwise_and(image, image, mask=mask)

    # 检测和标记圆形区域
    for i, contour in enumerate(contours):
        # 只处理外部轮廓
        if hierarchy[0][i][3] != -1:
            continue

        # 创建一个局部掩膜来检测圆形
        local_mask = np.zeros_like(gray)
        cv2.drawContours(local_mask, [contour], -1, (255), thickness=cv2.FILLED)

        # 使用霍夫圆检测
        circles = cv2.HoughCircles(local_mask, cv2.HOUGH_GRADIENT, dp=1.2, minDist=20, param1=50, param2=30,
                                   minRadius=10, maxRadius=30)

        if circles is None:
            # 如果没有检测到圆形，则在分割图像上标记该区域
            cv2.drawContours(segmented, [contour], -1, (0, 255, 0), thickness=3)
        else:
            print("检测到圆形，跳过该区域")

    # 显示结果
    cv2.imshow('Processed Maze', segmented)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# 示例调用
process_maze_image('test.jpg')
