import cv2
import numpy as np

def detect_circular_contours(image, prev_contours=None):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 1)

    # 使用自适应阈值
    edges = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # 形态学操作
    kernel = np.ones((3,3), np.uint8)
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    valid_contours = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 100:
            continue
        perimeter = cv2.arcLength(contour, True)
        if perimeter == 0:
            continue
        circularity = 4 * np.pi * (area / (perimeter * perimeter))
        if 0.6 < circularity < 1.2:
            valid_contours.append(contour)

    # 如果有前一帧的轮廓，进行时间一致性处理
    if prev_contours is not None:
        final_contours = []
        for contour in valid_contours:
            if any(cv2.matchShapes(contour, prev, cv2.CONTOURS_MATCH_I2, 0) < 0.1 for prev in prev_contours):
                final_contours.append(contour)
        valid_contours = final_contours if final_contours else valid_contours

    for contour in valid_contours:
        cv2.drawContours(image, [contour], -1, (255, 0, 0), 2)

    return image, valid_contours

def init(frame):
    box = cv2.selectROI('1', frame, False)
    cv2.destroyWindow('1')
    trac = cv2.TrackerCSRT_create()
    trac.init(frame, box)
    return trac, box

cap = cv2.VideoCapture('chlamy.avi')
if not cap.isOpened():
    print('Cannot open camera')

ret, frame = cap.read()
frame = cv2.resize(frame, (1920, 1080))

trac, box = init(frame)
prev_contours = None

while True:
    ret, frame = cap.read()
    if not ret:
        print('Cannot read image')
        break

    frame = cv2.resize(frame, (1920, 1080))
    frame, contours = detect_circular_contours(frame, prev_contours)
    prev_contours = contours

    suc, box = trac.update(frame)
    if suc:
        x, y, w, h = [int(i) for i in box]
        cv2.rectangle(frame, (x,y), (x+w,y+h), (255,0,0), 2, 1)
    else:
        cv2.putText(frame, 'R', (100,80), cv2.FONT_HERSHEY_PLAIN, 0.75, (0,0,255), 2)

    cv2.imshow('frame', frame)

    key = cv2.waitKey(1) & 0xff
    if key == 27:
        break
    elif key == ord('r'):
        trac, box = init(frame)

cv2.waitKey(0)
cap.release()
cv2.destroyAllWindows()