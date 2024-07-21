import cv2
import numpy as np
import threading


def end():
    cv2.destroyAllWindows()
    quit()


def read_video(video_path):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print('Cannot open camera')
        end()
    return cap


def read_image(cap):
    ret, frame = cap.read()
    if not ret:
        print('Cannot read image')
        cap.release()
        end()
    frame = cv2.resize(frame, (int(600 * 1.5), 600))
    return frame


def detect_init(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (3, 3), 1)
    fan = cv2.bitwise_not(blurred)
    edges = cv2.Canny(fan, 40, 60)
    kernel = np.ones((3, 3), np.uint8)
    edges = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel, iterations=1)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def detect_circular_contours(image, prev_contours=None):
    contours = detect_init(image)
    valid_contours = []
    for contour in contours:
        area = cv2.contourArea(contour)
        if area < 30:
            continue
        perimeter = cv2.arcLength(contour, True)
        if perimeter == 0:
            continue
        circularity = 4 * np.pi * (area / (perimeter * perimeter))
        if 0.5 < circularity < 1.2:
            valid_contours.append(contour)

    if prev_contours is not None:
        final_contours = []
        for contour in valid_contours:
            if any(cv2.matchShapes(contour, prev, cv2.CONTOURS_MATCH_I2, 0) < 0.1 for prev in prev_contours):
                final_contours.append(contour)
        valid_contours = final_contours if final_contours else valid_contours

    for contour in valid_contours:
        cv2.drawContours(image, [contour], -1, (255, 0, 0), 2)

    return image, valid_contours


def init_tracker(frame, contour):
    x, y, w, h = cv2.boundingRect(contour)
    tracker = cv2.legacy.TrackerCSRT_create()
    success = tracker.init(frame, (x, y, w, h))
    if success:
        print(f'Tracker initialized at position: {(x, y, w, h)}')
    else:
        print(f'Failed to initialize tracker at position: {(x, y, w, h)}')
    return tracker if success else None


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
            trackers.remove(tracker)
    return frame


def main():
    cap = read_video('video/chlamy.avi')
    frame = read_image(cap)
    trackers = []
    initial_contours = detect_circular_contours(frame)[1]
    for contour in initial_contours:
        tracker = init_tracker(frame, contour)
        if tracker:
            trackers.append(tracker)

    prev_contours = initial_contours

    while True:
        frame = read_image(cap)
        frame, current_contours = detect_circular_contours(frame, prev_contours)

        new_contours = [contour for contour in current_contours if not any(
            cv2.matchShapes(contour, prev, cv2.CONTOURS_MATCH_I2, 0) < 0.1 for prev in prev_contours)]

        for contour in new_contours:
            tracker = init_tracker(frame, contour)
            if tracker:
                trackers.append(tracker)

        prev_contours = current_contours

        thread = threading.Thread(target=process_frame, args=(frame, trackers))
        thread.start()
        thread.join()

        cv2.imshow('frame', frame)
        action = key_action()
        if action==True:
            break
        elif action == 'r':
            trackers = []
            for contour in prev_contours:
                tracker = init_tracker(frame, contour)
                if tracker:
                    trackers.append(tracker)

    cap.release()
    end()


if __name__ == "__main__":
    main()
