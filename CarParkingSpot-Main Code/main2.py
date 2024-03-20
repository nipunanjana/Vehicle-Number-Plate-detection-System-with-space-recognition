'''
Import necessary libraries: 
cv2: OpenCV library for image and video processing
pandas: Data manipulation library
numpy: Numerical computing library
ultralytics.YOLO: YOLOv8 object detection model
time: Time-related functions
'''
import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
import time
import socketio

'''
authToken = "your_secret_token"  # Replace with your actual token
sio = socketio.Client()

@sio.event
def connect():
    print("Connected to server")

@sio.event
def disconnect():
    print("Disconnected from server")

@sio.event
def parkingStatus(data):
    # Handle parking status updates (replace with your logic)
    print("Parking space ID:", data["spaceId"], "Availability:", data["availability"])    

# Function to simulate form submission (since Python doesn't have browser events)
def update_slots(spaceId, availability ):
    sio.emit("parkingStatus", {"spaceId": spaceId, "availability": availability})

sio.connect("http://localhost:3000", auth={"token": authToken})

'''

#Load YOLO model
model=YOLO('yolov8s.pt')

#Define a function for mouse events
def RGB(event, x, y, flags, param):
    if event == cv2.EVENT_MOUSEMOVE :  
        colorsBGR = [x, y]
        print(colorsBGR)

cv2.namedWindow('RGB')
cv2.setMouseCallback('RGB', RGB)

# set ip camera addresses.

#ip_camera_address = 'rtsp://http://[2402:4000:b282:fb9:69bb:3b7:a089:349f]:8080/'
camera_address = 'http://192.168.8.100:8080/video'
#camera_address = 'http://[2402:4000:2081:308d:9e6c:5069:8755:ee6e]:8080/video'


#Open video capture and read frames

#cap=cv2.VideoCapture('parking1.mp4')
#cap=cv2.VideoCapture(ip_camera_address)
cap = cv2.VideoCapture(camera_address)

#Load class names:
my_file = open("clz.txt", "r")
data = my_file.read()
class_list = data.split("\n")

#Define polygonal areas for each parking space. Each area is represented as a list of coordinates.
area1=[(50,368),(29,423),(67,421),(85,365)]
area2=[(105,353),(86,428),(137,427),(146,358)]
area3=[(159,354),(150,427),(204,425),(203,353)]
area4=[(217,352),(219,422),(273,418),(261,347)]
area5=[(274,345),(286,417),(338,415),(321,345)]
area6=[(336,343),(357,410),(409,408),(382,340)]
area7=[(396,338),(426,404),(479,399),(439,334)]
area8=[(458,333),(494,397),(543,390),(495,330)]
area9=[(511,327),(557,388),(603,383),(549,324)]
area10=[(559,328),(615,381),(654,372),(600,324)]
area11=[(615,328),(666,369),(703,363),(647,319)]
area12=[(663,319),(711,358),(754,354),(691,313)]

#Start an infinite loop to process frames from the video stream. Resize each frame to (1020, 500) pixels.
while True:    
    ret,frame = cap.read()
    if not ret:
        break
    #time.sleep(1)
    frame=cv2.resize(frame,(1020,500))

#Perform object detection using YOLO
    results=model.predict(frame)
    a=results[0].boxes.data
    px=pd.DataFrame(a).astype("float")      # Convert bounding box data to DataFrame

# Define 12 parking areas as lists of coordinates
    list1=[]
    list2=[]
    list3=[]
    list4=[]
    list5=[]
    list6=[]
    list7=[]
    list8=[]
    list9=[]
    list10=[]
    list11=[]
    list12=[]
    
#Process detections and check for cars in parking areas
    for index,row in px.iterrows():
 
        x1=int(row[0])
        y1=int(row[1])
        x2=int(row[2])
        y2=int(row[3])      
        d=int(row[5])       # Extract bounding box coordinates and class index.
        c=class_list[d]     # Get class name
        if 'car' in c:      # Check if the detected object is a car
            cx=int(x1+x2)//2
            cy=int(y1+y2)//2
            #Check if the car's center falls within any parking area.        
            results1=cv2.pointPolygonTest(np.array(area1,np.int32),((cx,cy)),False)
                #If a car is found in a parking area, mark it with a rectangle, circle, and text.(results1-->results12)
            if results1>=0:
               cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
               cv2.circle(frame,(cx,cy),3,(0,0,255),-1)
               list1.append(c)
               cv2.putText(frame,str(c),(x1,y1),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
            
            results2=cv2.pointPolygonTest(np.array(area2,np.int32),((cx,cy)),False)
            if results2>=0:
               cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
               cv2.circle(frame,(cx,cy),3,(0,0,255),-1)
               list2.append(c)
            
            results3=cv2.pointPolygonTest(np.array(area3,np.int32),((cx,cy)),False)
            if results3>=0:
               cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
               cv2.circle(frame,(cx,cy),3,(0,0,255),-1)
               list3.append(c)   
            results4=cv2.pointPolygonTest(np.array(area4,np.int32),((cx,cy)),False)
            if results4>=0:
               cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
               cv2.circle(frame,(cx,cy),3,(0,0,255),-1)
               list4.append(c)  
            results5=cv2.pointPolygonTest(np.array(area5,np.int32),((cx,cy)),False)
            if results5>=0:
               cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
               cv2.circle(frame,(cx,cy),3,(0,0,255),-1)
               list5.append(c)  
            results6=cv2.pointPolygonTest(np.array(area6,np.int32),((cx,cy)),False)
            if results6>=0:
               cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
               cv2.circle(frame,(cx,cy),3,(0,0,255),-1)
               list6.append(c)  
            results7=cv2.pointPolygonTest(np.array(area7,np.int32),((cx,cy)),False)
            if results7>=0:
               cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
               cv2.circle(frame,(cx,cy),3,(0,0,255),-1)
               list7.append(c)   
            results8=cv2.pointPolygonTest(np.array(area8,np.int32),((cx,cy)),False)
            if results8>=0:
               cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
               cv2.circle(frame,(cx,cy),3,(0,0,255),-1)
               list8.append(c)  
            results9=cv2.pointPolygonTest(np.array(area9,np.int32),((cx,cy)),False)
            if results9>=0:
               cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
               cv2.circle(frame,(cx,cy),3,(0,0,255),-1)
               list9.append(c)  
            results10=cv2.pointPolygonTest(np.array(area10,np.int32),((cx,cy)),False)
            if results10>=0:
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.circle(frame,(cx,cy),3,(0,0,255),-1)
                list10.append(c)     
            results11=cv2.pointPolygonTest(np.array(area11,np.int32),((cx,cy)),False)
            if results11>=0:
               cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
               cv2.circle(frame,(cx,cy),3,(0,0,255),-1)
               list11.append(c)    
            results12=cv2.pointPolygonTest(np.array(area12,np.int32),((cx,cy)),False)
            if results12>=0:
               cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
               cv2.circle(frame,(cx,cy),3,(0,0,255),-1)
               list12.append(c)
              
# Count cars in each area    
    slotID = a1=(len(list1))
    slotID = a2=(len(list2))       
    slotID = a3=(len(list3))    
    slotID = a4=(len(list4))
    slotID = a5=(len(list5))
    slotID = a6=(len(list6)) 
    slotID = a7=(len(list7))
    slotID = a8=(len(list8)) 
    slotID = a9=(len(list9))
    slotID = a10=(len(list10))
    slotID = a11=(len(list11))
    slotID = a12=(len(list12))

    o=(a1+a2+a3+a4+a5+a6+a7+a8+a9+a10+a11+a12)      # Total number of occupied spaces
    space=(12-o)                                    # Number of available spaces
    print(space)

    isAvailable1 = (len(list1) == 0)
    isAvailable2 = (len(list2) == 0)
    isAvailable3 = (len(list3) == 0)
    isAvailable4 = (len(list4) == 0)
    isAvailable5 = (len(list5) == 0)
    isAvailable6 = (len(list6) == 0)
    isAvailable7 = (len(list7) == 0)
    isAvailable8 = (len(list8) == 0)
    isAvailable9 = (len(list9) == 0)
    isAvailable10 = (len(list10) == 0)
    isAvailable11 = (len(list11) == 0)
    isAvailable12 = (len(list12) == 0)
      
    print(f"Slot 1 = {isAvailable1}")
    print(f"Slot 2 = {isAvailable2}")
    print(f"Slot 3 = {isAvailable3}")
    print(f"Slot 4 = {isAvailable4}")
    print(f"Slot 5 = {isAvailable5}")
    print(f"Slot 6 = {isAvailable6}")
    print(f"Slot 7 = {isAvailable7}")
    print(f"Slot 8 = {isAvailable8}")
    print(f"Slot 9 = {isAvailable9}")
    print(f"Slot 10 = {isAvailable10}")
    print(f"Slot 11 = {isAvailable11}")
    print(f"Slot 12 = {isAvailable12}")
    
    '''
    update_slots("S1",isAvailable1)
    update_slots("S2",isAvailable2)
    update_slots("S3",isAvailable3)
    update_slots("S4",isAvailable4)
    update_slots("S5",isAvailable5)
    update_slots("S6",isAvailable6)
    update_slots("S7",isAvailable7)
    update_slots("S8",isAvailable8)
    update_slots("S9",isAvailable9)
    update_slots("S10",isAvailable10)
    update_slots("S11",isAvailable11)
    update_slots("S12",isAvailable12)
    '''

# Draw parking areas with different colors based on occupancy    
    if a1==1:
        cv2.polylines(frame,[np.array(area1,np.int32)],True,(0,0,255),2)
        cv2.putText(frame,str('1'),(50,441),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)       
    else:
        cv2.polylines(frame,[np.array(area1,np.int32)],True,(0,255,0),2)
        cv2.putText(frame,str('1'),(50,441),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
    if a2==1:
        cv2.polylines(frame,[np.array(area2,np.int32)],True,(0,0,255),2)
        cv2.putText(frame,str('2'),(106,440),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
    else:
        cv2.polylines(frame,[np.array(area2,np.int32)],True,(0,255,0),2)
        cv2.putText(frame,str('2'),(106,440),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
    if a3==1:
        cv2.polylines(frame,[np.array(area3,np.int32)],True,(0,0,255),2)
        cv2.putText(frame,str('3'),(175,436),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
    else:
        cv2.polylines(frame,[np.array(area3,np.int32)],True,(0,255,0),2)
        cv2.putText(frame,str('3'),(175,436),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
    if a4==1:
        cv2.polylines(frame,[np.array(area4,np.int32)],True,(0,0,255),2)
        cv2.putText(frame,str('4'),(250,436),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
    else:
        cv2.polylines(frame,[np.array(area4,np.int32)],True,(0,255,0),2)
        cv2.putText(frame,str('4'),(250,436),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
    if a5==1:
        cv2.polylines(frame,[np.array(area5,np.int32)],True,(0,0,255),2)
        cv2.putText(frame,str('5'),(315,429),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
    else:
        cv2.polylines(frame,[np.array(area5,np.int32)],True,(0,255,0),2)
        cv2.putText(frame,str('5'),(315,429),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
    if a6==1:
        cv2.polylines(frame,[np.array(area6,np.int32)],True,(0,0,255),2)
        cv2.putText(frame,str('6'),(386,421),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
    else:
        cv2.polylines(frame,[np.array(area6,np.int32)],True,(0,255,0),2)
        cv2.putText(frame,str('6'),(386,421),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
    if a7==1:
        cv2.polylines(frame,[np.array(area7,np.int32)],True,(0,0,255),2)
        cv2.putText(frame,str('7'),(456,414),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
    else:
        cv2.polylines(frame,[np.array(area7,np.int32)],True,(0,255,0),2)
        cv2.putText(frame,str('7'),(456,414),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
    if a8==1:
        cv2.polylines(frame,[np.array(area8,np.int32)],True,(0,0,255),2)
        cv2.putText(frame,str('8'),(527,406),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
    else:
        cv2.polylines(frame,[np.array(area8,np.int32)],True,(0,255,0),2)
        cv2.putText(frame,str('8'),(527,406),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
    if a9==1:
        cv2.polylines(frame,[np.array(area9,np.int32)],True,(0,0,255),2)
        cv2.putText(frame,str('9'),(591,398),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
    else:
        cv2.polylines(frame,[np.array(area9,np.int32)],True,(0,255,0),2)
        cv2.putText(frame,str('9'),(591,398),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
    if a10==1:
        cv2.polylines(frame,[np.array(area10,np.int32)],True,(0,0,255),2)
        cv2.putText(frame,str('10'),(649,384),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
    else:
        cv2.polylines(frame,[np.array(area10,np.int32)],True,(0,255,0),2)
        cv2.putText(frame,str('10'),(649,384),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
    if a11==1:
        cv2.polylines(frame,[np.array(area11,np.int32)],True,(0,0,255),2)
        cv2.putText(frame,str('11'),(697,377),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
    else:
        cv2.polylines(frame,[np.array(area11,np.int32)],True,(0,255,0),2)
        cv2.putText(frame,str('11'),(697,377),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
    if a12==1:
        cv2.polylines(frame,[np.array(area12,np.int32)],True,(0,0,255),2)
        cv2.putText(frame,str('12'),(752,371),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
    else:
        cv2.polylines(frame,[np.array(area12,np.int32)],True,(0,255,0),2)
        cv2.putText(frame,str('12'),(752,371),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)

    # Display available spaces
    cv2.putText(frame,str(space),(23,30),cv2.FONT_HERSHEY_PLAIN,3,(255,255,255),2)    

    # Show the frame with detections and parking areas
    cv2.imshow("RGB", frame)

    #time.sleep(3)
    if cv2.waitKey(1)&0xFF==27:
        break       # Exit if 'ESC' key is

#url = 'http://localhost:3000/parkingSpaces'

cap.release()
cv2.destroyAllWindows()