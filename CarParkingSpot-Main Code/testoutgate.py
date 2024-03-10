import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
import time
#import requests

model=YOLO('yolov8s.pt')

def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :  
        colorsBGR = [x, y]
        print(colorsBGR)

cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

camera_address = 'rtsp://admin:L22D04E7@192.168.1.6/cam/realmonitor?channel=1&subtype=00&authbasic=YWRtaW46TDIyRDA0RTc='  # in cam
#camera_address = 'rtsp://admin:parknpay123@192.168.1.4/cam/realmonitor?channel=1&subtype=00&authbasic=YWRtaW46TDIyRDA0RTc='  # out cam

#cap=cv2.VideoCapture('parking1.mp4')
cap = cv2.VideoCapture(camera_address)

my_file = open("clz.txt", "r")
data = my_file.read()
class_list = data.split("\n")

area9=[(263,236),(342,435),(714,395),(503,248)]
#area9=[(518,292),(545,337),(589,335),(554,287)]

with open("log.txt", "a") as log_file:
    while True:    
        ret,frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (1020,500))
        results = model.predict(frame)
        a = results[0].boxes.data
        px = pd.DataFrame(a).astype("float")
        list9 = []

        for index,row in px.iterrows():
            x1 = int(row[0])
            y1 = int(row[1])
            x2 = int(row[2])
            y2 = int(row[3])
            d = int(row[5])
            c = class_list[d]
            if 'car' in c:
                cx = int(x1+x2)//2
                cy = int(y1+y2)//2

                results9 = cv2.pointPolygonTest(np.array(area9, np.int32), ((cx,cy)), False)
                if results9 >= 0:
                    cv2.rectangle(frame, (x1,y1), (x2,y2), (0,255,0), 2)
                    cv2.circle(frame, (cx,cy), 3, (0,0,255), -1)
                    list9.append(c)  

        a9 = len(list9)
        log_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')}, Area 9: {a9}\n")  # Writing log entry

        # Extract slotID and availability
        slotID = '9'  # Or any other desired ID format
        isAvailable = True if a9 == 0 else False

        if a9 == 1:
            cv2.polylines(frame, [np.array(area9, np.int32)], True, (0,0,255), 2)
            cv2.putText(frame, str('9'), (591,398), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0,0,255), 1)
        else:
            cv2.polylines(frame, [np.array(area9, np.int32)], True, (0,255,0), 2)
            cv2.putText(frame, str('9'), (591,398), cv2.FONT_HERSHEY_COMPLEX, 0.5, (255,255,255), 1)

        cv2.imshow("RGB", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

cap.release()
cv2.destroyAllWindows()
