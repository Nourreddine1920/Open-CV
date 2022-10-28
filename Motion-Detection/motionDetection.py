# importing OpenCv , time and pandas library
import cv2  , time , pandas
import os 
import numpy as np


#importing datime class from datetime library 
from datetime import datetime

#Assigning our static_back to None 
static_back = None

#Initializing dataframe , one column is start 
#time and other column is end time 
currentMotion= ["" ,""]
motionList = []
#print(currentMotion)
#Capture Video
video = cv2.VideoCapture(0)
# video.set(3, 640) # set video width
# video.set(4, 480) # set video height

#captureDevice = cv2.VideoCapture(0, cv2.CAP_DSHOW) #captureDevice = camera


#Infinite loop to treat stack of image as video 
while True : 
    print("entred....")
    #Reading frame(image) from video
    check , frame = video.read()
    #print("ddd")
    

    # inializing motion to 0
    motion = 0

    #converting image to gray_scale image 
    gray = cv2.cvtColor(frame , cv2.COLOR_BGR2GRAY)
    #print("aa")

    #converting gray_scale image to GaussianBlur
    #so that can be easily find emotion 
    gray= cv2.GaussianBlur(gray , (21 , 21) , 0)
    #print("eee")
    
    # In first iteration we assign the value 
    # of static_back to our first frame
    if static_back is None : 
        static_back = gray
        continue
    #print("ccc")

    #Difference between static background and current frame (which is GaussianBlur)
    diff_frame = cv2.absdiff(static_back , gray)

    # if change between static background and current frame is greater than 30 
    # it will show white color (255)

    thresh_frame = cv2.threshold(diff_frame , 30 , 255 , cv2.THRESH_BINARY)[1]
    #print("ggg")
    thresh_frame = cv2.dilate(thresh_frame , None , iterations=2)
    
    #Finding countours of moving objects
    cnts ,_ = cv2.findContours(thresh_frame.copy() , cv2.RETR_EXTERNAL   , cv2.CHAIN_APPROX_SIMPLE)
    print(cnts)
    for contour in cnts : 
        #print("yyy")
        if cv2.contourArea(contour) < 10000 : 
            motion = 1
            continue
        if currentMotion[0] == "" and motion ==1  : 
            currentMotion[0] = datetime.now().strftime("%m/%d/%Y : %H:%M:%S")
        (x , y , w , h) = cv2.boundingRect(contour)
        # making green rectangle arround the moving object 
        cv2.rectangle(frame , (x , y) , (x + w , y + h) , (0 , 255 , 0) , 3) 

    # Appending status of motion 
    if motion == 0 and currentMotion[0] != "" : 
        currentMotion[1] = datetime.now().strftime("%m/%d/%Y : %H:%M:%S")
        motionList.append(currentMotion)
        currentMotion = ["" , ""]
    
    #Displaying image in gray_scale
    cv2.imshow("Gray Frame" , gray)
    print("enterd")
    # Displaying the difference in current frame to the static frame 
    cv2.imshow("Difference frame" , diff_frame)
    # Displaying the black and white image in which if intensity greater than 30 it will appear white 
    cv2.imshow("threshold Frame" , thresh_frame)
    #Displaying color frame with contour of motion of object 
    cv2.imshow("Color frame" , frame)
    key = cv2.waitKey(1)
    # if q entered whole process will stop 
    if cv2.waitKey(1) & 0xFF == ord('q')  : 
        # if something is moving then it append the end time of movement 
        if motion ==1 and currentMotion[0] != "" : 
            currentMotion[1] = datetime.now().strftime("%m/%d/%Y : %H:%M:%S")
            motionList.append(currentMotion)
        break
for move in motionList[:30] : 
    print(move)
video.release()
#destroying all windows
cv2.destroyAllWindows()
