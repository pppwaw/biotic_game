import cv2
import numpy as np

def process_frame(frame):
    # 转换为 HSV 色彩空间
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # 定义衣藻的颜色范围
    lower_green = np.array([120, 90, 200])
    upper_green = np.array([30, 120, 255])

    # 创建遮罩来提取绿色区域
    mask = cv2.inRange(hsv, lower_green, upper_green)

    # 使用形态学操作去除噪声
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    # 查找轮廓
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 绘制轮廓
    for contour in contours:
        if cv2.contourArea(contour) > 50:  # 忽略小轮廓
            cv2.drawContours(frame, [contour], -1, (0, 255, 0), 2)

    return frame

def process_video(video_path):
    # 打开视频文件
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"无法打开视频: {video_path}")
        return

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # 处理每一帧
        processed_frame = process_frame(frame)

        # 显示结果
        cv2.imshow('Detected Chlorella', processed_frame)

        # 按 'q' 键退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放视频捕获对象并关闭所有窗口
    cap.release()
    cv2.destroyAllWindows()

# 调用函数并传入视频路径
process_video('video/chlamy_PDMS.avi')
