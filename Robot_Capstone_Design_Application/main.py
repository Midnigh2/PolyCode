from ultralytics import YOLO
import cv2
import cvzone
import math
import os
import datetime
import imutils


#record
# file_path = './video/record.mp4'
base_path = os.path.dirname(os.path.abspath("__file__"))
base_path = base_path + "\\video"
if not os.path.exists(base_path):
    os.makedirs(base_path)

fourcc = cv2.VideoWriter_fourcc(*'XVID')
record = False

#camera
cam = cv2.VideoCapture('rtsp://yourID:yourPW@camIP')  # For Webcam
video = -1
#yolo
model = YOLO("fall.pt")
classNames = ['fall', 'half', 'nofall']
myColor = (0, 0, 255)

while (cam.isOpened()):
    success, img = cam.read()
    img = imutils.resize(img, height=1280, width=720) # resize frame
    key = cv2.waitKey(1)
    results = model(img, stream=True)

    now = datetime.datetime.now().strftime("%d_%H-%M-%S")

    for r in results:
        boxes = r.boxes
        for box in boxes:
            # Bounding Box
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            # cv2.rectangle(img,(x1,y1),(x2,y2),(255,0,255),3)
            w, h = x2 - x1, y2 - y1
            # cvzone.cornerRect(img, (x1, y1, w, h))

            # Confidence
            conf = math.ceil((box.conf[0] * 100)) / 100
            # Class Name
            cls = int(box.cls[0])
            currentClass = classNames[cls]
            print(currentClass)
            if conf>0.5:
                if currentClass =='fall' or currentClass =='half':
                    myColor = (0, 0, 255)
                elif currentClass =='nofall':
                    myColor =(0,255,0)
                else:
                    myColor = (255, 0, 0)

                cvzone.putTextRect(img, f'{classNames[cls]} {conf}',
                                   (max(0, x1), max(35, y1)), scale=1, thickness=1,colorB=myColor,
                                   colorT=(255,255,255),colorR=myColor, offset=5)
                cv2.rectangle(img, (x1, y1), (x2, y2), myColor, 3)

    if (record == True and video == -1):
        video = cv2.VideoWriter(os.path.join(base_path, "Image" +"_"+str(now) + ".mp4"), fourcc, 30.0, (img.shape[1], img.shape[0]))

    if (record == False and video != -1):
        video.release()
        video = -1

    elif key == 114:  # r
        print("Start Record")
        record = True

    elif key == 101:  # e
        print("End Record")
        record = False

    if key == 27: # esc
        break

    if record == True:
        print("Recording...")
        if video != -1:
            video.write(img)

    cv2.imshow("Image", img)

video.release()
cam.release()

