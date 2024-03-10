import cv2
import pandas as pd
import numpy as np
from ultralytics import YOLO
import time
import socketio


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

sio.connect("http://localhost:5000", auth={"token": authToken})


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
camera_address1 = 'http://192.168.8.100:8080/video'  # Camera 1 for slots 1-3
camera_address2 = 'http://192.168.8.100:8080/video'  # Camera 2 for slots 4-6

#Open video capture and read frames
cap1 = cv2.VideoCapture(camera_address1)
cap2 = cv2.VideoCapture(camera_address2)

# Check if both cameras opened successfully
if not (cap1.isOpened() or cap2.isOpened()):
    print("Error opening video streams or invalid camera addresses.")
    exit(1)

#Load class names:
my_file = open("clz.txt", "r")
data = my_file.read()
class_list = data.split("\n")

#Define polygonal areas for each parking space. Each area is represented as a list of coordinates.

# Camera 1 (slots 1-3)
area1_1 = [(36,537),(28,629),(77,635),(84,534)]
area1_2 = [(79,534), (77,635), (123, 632), (124, 531)]
area1_3 = [(117, 531), (117, 630), (169,627), (166,528)]

# Camera 2 (slots 4-6)
area2_4 = [(1118,493),(1162,581),(1209,569),(1168,481)]
area2_5 = [(1168,481),(1209,569),(1256,554), (1210,475)]
area2_6 = [(1210,475),(1256,554),(1294,541),(1242,466)]

#Start an infinite loop to process frames from the video stream. Resize each frame to (1020, 500) pixels.
while True:
    ret1, frame1 = cap1.read()
    ret2, frame2 = cap2.read()

    if not (ret1 and ret2):
        break
    # Resize frame1 for consistency 
    frame1 = cv2.resize(frame1, (750,700))  # Adjust dimensions if necessary
    frame2 = cv2.resize(frame2, (750,700))
    
    # Perform object detection using YOLO for frame1
    results1 = model.predict(frame1)
    boxes1 = results1[0].boxes.data

    # Perform object detection using YOLO for frame2
    results2 = model.predict(frame2)
    boxes2 = results2[0].boxes.data

    # Combine the frames
    combined_frame = cv2.hconcat([frame1, frame2])
    
# Define 12 parking areas as lists of coordinates
    list1=[]
    list2=[]
    list3=[]
    list4=[]
    list5=[]
    list6=[]
    
# Process detections and check for cars in parking areas for frame1
    for index, row in pd.DataFrame(boxes1).astype("float").iterrows():
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5])  # Extract bounding box coordinates and class index
        c = class_list[d]  # Get class name       

        if 'car' in c:  # Check if detected object is a car
            cx = int((x1 + x2) // 2)
            cy = int((y1 + y2) // 2)

            # Check if car's center falls within any of camera 1's parking areas
            results11 = cv2.pointPolygonTest(np.array(area1_1, np.int32), ((cx, cy)), False)
            results12 = cv2.pointPolygonTest(np.array(area1_2, np.int32), ((cx, cy)), False)
            results13 = cv2.pointPolygonTest(np.array(area1_3, np.int32), ((cx, cy)), False)

        # If car is detected in a slot, draw rectangles and circles directly on the combined_frame
            if results11 >= 0:  # Car detected in slot 1
                cv2.rectangle(combined_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(combined_frame, (cx, cy), 3, (0, 0, 255), -1)
                list1.append(c)
            elif results12 >= 0:  # Car detected in slot 2
                cv2.rectangle(combined_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(combined_frame, (cx, cy), 3, (0, 0, 255), -1)
                list2.append(c)
            elif results13 >= 0:  # Car detected in slot 3
                cv2.rectangle(combined_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(combined_frame, (cx, cy), 3, (0, 0, 255), -1)
                list3.append(c)
      
    
# Process detections and check for cars in parking areas for frame2
    for index, row in pd.DataFrame(boxes2).astype("float").iterrows():
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5])  # Extract bounding box coordinates and class index
        c = class_list[d]  # Get class name 

        if 'car' in c:  # Check if detected object is a car
            cx = int((x1 + x2) // 2)
            cy = int((y1 + y2) // 2)

            results24 = cv2.pointPolygonTest(np.array(area2_4, np.int32), ((cx, cy)), False)
            results25 = cv2.pointPolygonTest(np.array(area2_5, np.int32), ((cx, cy)), False)
            results26 = cv2.pointPolygonTest(np.array(area2_6, np.int32), ((cx, cy)), False)

            if results24 >= 0:  # Car detected in slot 4
                cv2.rectangle(combined_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(combined_frame, (cx, cy), 3, (0, 0, 255), -1)
                list4.append(c)
            elif results25 >= 0:  # Car detected in slot 5
                cv2.rectangle(combined_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(combined_frame, (cx, cy), 3, (0, 0, 255), -1)
                list5.append(c)
            elif results26 >= 0:  # Car detected in slot 6
                cv2.rectangle(combined_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(combined_frame, (cx, cy), 3, (0, 0, 255), -1)
                list6.append(c)

# Perform object detection using YOLO for the combined frame
    results_combined = model.predict(combined_frame)
    boxes_combined = results_combined[0].boxes.data

# Process detections and check for cars in parking areas for the combined frame
    for index, row in pd.DataFrame(boxes_combined).astype("float").iterrows():   
        x1 = int(row[0])
        y1 = int(row[1])
        x2 = int(row[2])
        y2 = int(row[3])
        d = int(row[5])  # Extract bounding box coordinates and class index
        c = class_list[d]  # Get class name

        if 'car' in c:  # Check if detected object is a car
            cx = int((x1 + x2) // 2)
            cy = int((y1 + y2) // 2)

            # Check if car's center falls within any of camera 1's parking areas
            results11 = cv2.pointPolygonTest(np.array(area1_1, np.int32), ((cx, cy)), False)
            results12 = cv2.pointPolygonTest(np.array(area1_2, np.int32), ((cx, cy)), False)
            results13 = cv2.pointPolygonTest(np.array(area1_3, np.int32), ((cx, cy)), False)
            results24 = cv2.pointPolygonTest(np.array(area2_4, np.int32), ((cx, cy)), False)
            results25 = cv2.pointPolygonTest(np.array(area2_5, np.int32), ((cx, cy)), False)
            results26 = cv2.pointPolygonTest(np.array(area2_6, np.int32), ((cx, cy)), False)

        # If car is detected in a slot, draw rectangles and circles directly on the combined_frame
            if results11 >= 0:  # Car detected in slot 1
                cv2.rectangle(combined_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(combined_frame, (cx, cy), 3, (0, 0, 255), -1)
                list1.append(c)
            elif results12 >= 0:  # Car detected in slot 2
                cv2.rectangle(combined_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(combined_frame, (cx, cy), 3, (0, 0, 255), -1)
                list2.append(c)
            elif results13 >= 0:  # Car detected in slot 3
                cv2.rectangle(combined_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(combined_frame, (cx, cy), 3, (0, 0, 255), -1)
                list3.append(c)
            elif results24 >= 0:  # Car detected in slot 4
                cv2.rectangle(combined_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(combined_frame, (cx, cy), 3, (0, 0, 255), -1)
                list4.append(c)
            elif results25 >= 0:  # Car detected in slot 5
                cv2.rectangle(combined_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(combined_frame, (cx, cy), 3, (0, 0, 255), -1)
                list5.append(c)
            elif results26 >= 0:  # Car detected in slot 6
                cv2.rectangle(combined_frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.circle(combined_frame, (cx, cy), 3, (0, 0, 255), -1)
                list6.append(c)    


    # Count cars in each slot
    slotID = a11 = len(list1)
    slotID = a12 = len(list2)
    slotID = a13 = len(list3)
    slotID = a24 = len(list4)
    slotID = a25 = len(list5)
    slotID = a26 = len(list6) 

    # Calculate available spaces for camera 1
    o1 = a11 + a12 + a13 + a24 +a25 +a26  # Total occupied spaces
    space1 = 6 - o1  # Available spaces                                
    print(space1)

    isAvailable1 = (len(list1) == 0)
    isAvailable2 = (len(list2) == 0)
    isAvailable3 = (len(list3) == 0)
    isAvailable4 = (len(list4) == 0)
    isAvailable5 = (len(list5) == 0)
    isAvailable6 = (len(list6) == 0)

    print(f"Slot 1 = {isAvailable1}")
    print(f"Slot 2 = {isAvailable2}")
    print(f"Slot 3 = {isAvailable3}")
    print(f"Slot 4 = {isAvailable4}")
    print(f"Slot 5 = {isAvailable5}")
    print(f"Slot 6 = {isAvailable6}")

    
    update_slots("S1",isAvailable1)
    update_slots("S2",isAvailable2)
    update_slots("S3",isAvailable3)
    update_slots("S4",isAvailable4)
    update_slots("S5",isAvailable5)
    update_slots("S6",isAvailable6)
    

# Draw parking areas with different colors based on occupancy    
    if a11==1:
        cv2.polylines(combined_frame,[np.array(area1_1,np.int32)],True,(0,0,255),2)
        cv2.putText(combined_frame,str('1'),(44,653),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)       
    else:
        cv2.polylines(combined_frame,[np.array(area1_1,np.int32)],True,(0,255,0),2)
        cv2.putText(combined_frame,str('1'),(44,653),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
    if a12==1:
        cv2.polylines(combined_frame,[np.array(area1_2,np.int32)],True,(0,0,255),2)
        cv2.putText(combined_frame,str('2'),(94,654),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
    else:
        cv2.polylines(combined_frame,[np.array(area1_2,np.int32)],True,(0,255,0),2)
        cv2.putText(combined_frame,str('2'),(94,654),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
    if a13==1:
        cv2.polylines(combined_frame,[np.array(area1_3,np.int32)],True,(0,0,255),2)
        cv2.putText(combined_frame,str('3'),(149,647),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
    else:
        cv2.polylines(combined_frame,[np.array(area1_3,np.int32)],True,(0,255,0),2)
        cv2.putText(combined_frame,str('3'),(149,647),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
    if a24==1:
        cv2.polylines(combined_frame,[np.array(area2_4,np.int32)],True,(0,0,255),2)
        cv2.putText(combined_frame,str('4'),(1192,600),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
    else:
        cv2.polylines(combined_frame,[np.array(area2_4,np.int32)],True,(0,255,0),2)
        cv2.putText(combined_frame,str('4'),(1192,600),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
    if a25==1:
        cv2.polylines(combined_frame,[np.array(area2_5,np.int32)],True,(0,0,255),2)
        cv2.putText(combined_frame,str('5'),(1232,587),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
    else:
        cv2.polylines(combined_frame,[np.array(area2_5,np.int32)],True,(0,255,0),2)
        cv2.putText(combined_frame,str('5'),(1232,587),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)
    if a26==1:
        cv2.polylines(combined_frame,[np.array(area2_6,np.int32)],True,(0,0,255),2)
        cv2.putText(combined_frame,str('6'),(1280,573),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
    else:
        cv2.polylines(combined_frame,[np.array(area2_6,np.int32)],True,(0,255,0),2)
        cv2.putText(combined_frame,str('6'),(1280,573),cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),1)

   
    # Display available spaces
    cv2.putText(combined_frame, str(space1), (23, 30), cv2.FONT_HERSHEY_PLAIN, 3, (255, 255, 255), 2)

    # Show the separate frames with detections and parking areas
    #cv2.imshow("Camera 1", frame1)
    #cv2.imshow("Camera 2", frame2)

    # Show the combined_frame with detections and parking areas
    cv2.imshow("RGB", combined_frame)

    #time.sleep(3)
    if cv2.waitKey(0) & 0xFF == 27:
        break      # Exit if 'ESC' key is

url = 'http://localhost:3000/parkingSpaces'    
#url = 'http://localhost:5000/parkingSpaces'

cap1.release()
cap2.release()
cv2.destroyAllWindows()