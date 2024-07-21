import cv2
import numpy as np

def detect_circular_contours(image):
    # 转换为灰度图像
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # 使用高斯模糊来减少噪声
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # 使用Canny边缘检测
    edges = cv2.Canny(blurred, 50, 150)

    # 查找轮廓
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 遍历所有轮廓
    for contour in contours:
        # 计算轮廓的圆度
        area = cv2.contourArea(contour)
        if area < 50:  # 忽略小轮廓
            continue
        perimeter = cv2.arcLength(contour, True)
        if perimeter == 0:
            continue
        circularity = 4 * np.pi * (area / (perimeter * perimeter))

        # 检查圆度是否在合理范围内
        if 0.7 < circularity < 1.2:
            # 绘制轮廓
            cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)

    return image

def process_image(image_path):
    # 读取图像
    image = cv2.imread(image_path)
    if image is None:
        print(f"无法读取图像: {image_path}")
        return

    # 检测并绘制圆形轮廓
    result_image = detect_circular_contours(image)

    # 显示结果
    cv2.imshow('Detected Circular Contours', result_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# 调用函数并传入图像路径
process_image('test.jpg')
