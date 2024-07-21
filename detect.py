import cv2
import numpy as np
import threading

def detect_init(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (5, 5), 1)
    edges = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    kernel = np.ones((3, 3), np.uint8)
    closing = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=2)

    # 距离变换
    dist_transform = cv2.distanceTransform(closing, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)
    sure_fg = np.uint8(sure_fg)

    # 找背景
    sure_bg = cv2.dilate(closing, kernel, iterations=3)
    unknown = cv2.subtract(sure_bg, sure_fg)

    # 标记标签
    ret, markers = cv2.connectedComponents(sure_fg)
    markers = markers + 1
    markers[unknown == 255] = 0

    markers = cv2.watershed(image, markers)
    image[markers == -1] = [255, 0, 0]

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def detect_circular_contours(image, prev_contours=None):
    contours = detect_init(image)
    valid_contours = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 50:
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

    # for contour in valid_contours:
    #     cv2.drawContours(image, [contour], -1, (255, 0, 0), 2)

    return image, valid_contours


def init_tracker(frame, contour):
    x, y, w, h = cv2.boundingRect(contour)
    tracker = cv2.TrackerCSRT_create()
    tracker.init(frame, (x, y, w, h))
    return tracker


def key_action():
    key = cv2.waitKey(1) & 0xff
    if key == 27:
        return True
    elif key == ord('r'):
        return 'r'
    return False

def process_frame(frame, trackers):
    for tracker in trackers:
        success, box = tracker.update(frame)
        if success:
            p1 = (int(box[0]), int(box[1]))
            p2 = (int(box[0] + box[2]), int(box[1] + box[3]))
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)
        else:
            trackers.remove(tracker)  # 移除失效的追踪器
    return frame

def main():
    cap = cv2.VideoCapture('chlamy.avi')
    if not cap.isOpened():
        print('Cannot open camera')
        return

    ret, frame = cap.read()
    frame = cv2.resize(frame, (int(600*1.5), 600))

    trackers = []
    initial_contours = detect_circular_contours(frame)[1]
    for contour in initial_contours:
        tracker = init_tracker(frame, contour)
        trackers.append(tracker)

    prev_contours = initial_contours

    while True:
        ret, frame = cap.read()
        if not ret:
            print('Cannot read image')
            break

        frame = cv2.resize(frame, (int(600*1.5), 600))
        frame,prev_contours= detect_circular_contours(frame, prev_contours)

        print(len(prev_contours))
        thread = threading.Thread(target=process_frame, args=(frame, trackers))
        thread.start()
        thread.join()

        cv2.imshow('frame', frame)
        action = key_action()
        if action == True:
            break
        elif action == 'r':
            trackers = []
            for contour in prev_contours:
                tracker = init_tracker(frame, contour)
                trackers.append(tracker)

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()