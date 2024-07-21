import cv2
import numpy as np

img = cv2.imread("test.png")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
blurred = cv2.GaussianBlur(gray, (5, 5), 1)
edges = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
# 先膨胀后腐蚀
kernel = np.ones((5, 5), np.uint8)
closing = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)
# Canny
edges = cv2.Canny(closing, 30, 70)
cv2.imshow("edges", edges)
cv2.waitKey(0)