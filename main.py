import cv2

cap = cv2.VideoCapture('./Desktop/Lane.mp4')
if not cap.isOpened():
    print('Cannot open camera')


def init(frame):
    box = cv2.selectROI('1', frame, False)
    cv2.destroyWindow("1")
    trac = cv2.TrackerCSRT_create()
    trac.init(frame, box)
    return trac, box


ret, frame = cap.read()
if not ret:
    print('Cannot read image')

target_width = 800

# 计算目标窗口高度，保持1.5:1的纵横比
target_height = int(target_width / 1.5)
frame = cv2.resize(frame, (target_width, target_height))
trac, box = init(frame)
while True:
    ret, frame = cap.read()
    frame = cv2.resize(frame, (target_width, target_height))
    if not ret:
        print('Cannot read image')
        break
    suc, box = trac.update(frame)
    if suc:
        x, y, w, h = int(box[0]), int(box[1]), int(box[2]), int(box[3])
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2, 1)
    else:
        cv2.putText(frame, 'R', (100, 80), cv2.FONT_HERSHEY_PLAIN, 0.75, (0, 0, 255), 2)
    cv2.imshow('frame', frame)
    key = cv2.waitKey(1) & 0xff
    if key == 27:
        break
    elif key == ord('r'):
        trac, box = init(frame)
cap.release()
cv2.destroyAllWindows()
