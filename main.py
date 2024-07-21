import cv2
cap = cv2.VideoCapture('chlamy.avi')

if not cap.isOpened():
    print('Cannot open camera')

def init(frame):
    box=cv2.selectROI('1',frame,False)
    cv2.destroyWindow('1')
    trac=cv2.TrackerCSRT_create()
    trac.init(frame,box)
    return trac,box

ret, frame=cap.read()
frame=cv2.resize(frame,(1920,1080))
if not ret:
    print('Cannot read image')

trac,box=init(frame)

while True:
    ret,frame=cap.read()
    if not ret:
        print('Cannot read image')
        break
    frame=cv2.resize(frame,(1920,1080))
    suc,box=trac.update(frame)
    if suc:
        x,y,w,h=[int(i) for i in box]
        print(x,y,w,h)
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2,1)
    else:
        cv2.putText(frame,'R',(100,80),cv2.FONT_HERSHEY_PLAIN,0.75,(0,0,255),2)
    cv2.imshow('frame',frame)
    key = cv2.waitKey(1) & 0xff
    if key == 27:
        break
    elif key == ord('r'):
        trac,box=init(frame)
cap.release()
cv2.destroyAllWindows()
