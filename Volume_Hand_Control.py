import cv2 as cv
from cv2 import waitKey
from cv2 import FILLED
import numpy as np
import HandTrackingModule as htm
import time
import math
# Voice libraries
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
        

cap = cv.VideoCapture(0)

# The webcam dimensions are adjusted
#####################
widthC = 640
heightC = 480
cap.set(3,widthC)
cap.set(4,heightC)
#####################
detector = htm.handDetector() # Hand Detector which has been made by me, included

pTime = 0

# Get default audio device using PyCAW
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(
    IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))
       

range =volume.GetVolumeRange() # This object is created in order to learn what the range is
print(range)
minVol = range[0]
maxVol = range[1]




while True:
    success , img = cap.read()
    
    if success:
        # Fps is written on the screen
        #############################
        cTime = time.time()
        color = (255,0,255)
        fps = 1/(cTime-pTime)
        pTime = cTime
        cv.putText(img,str(int(fps)),(40,50),1,cv.FONT_HERSHEY_COMPLEX,(color),2)
        ##############################
        img = detector.findHands(img,True) # Firstly, it must find the hands
        lmList =detector.findPositon(img) # Secondly, The hands which are found, can find locations
        color2 = (255,255,0)
        if len(lmList) !=0:
            
            # print(lmList[4])
            # print(lmList[8])
            
            
            
           
            x = int((lmList[4][1] + lmList[8][1])/2)
            y = int((lmList[4][2]+ lmList[8][2]) /2)
            # print(x,y)
            dis = math.dist((lmList[4][1],lmList[4][2]),(lmList[8][1],lmList[8][2]))
            # print(dis)
            cv.circle(img,(lmList[4][1],lmList[4][2]),1,color,20)
            cv.circle(img,(lmList[8][1],lmList[8][2]),1,color,20)
            cv.line(img,(lmList[4][1],lmList[4][2]),(lmList[8][1],lmList[8][2]),color,4)
            cv.circle(img,(x,y),1,(color2),20)
            
            
            
            
            
            
            # max dis = 200  min dis = 25
            vol = np.interp(dis,[25,200],[minVol,maxVol])  # The ranges is equalled by this function
            # print(vol)
            
            # print(vol) 
            vol1 = np.interp(dis,[minVol,maxVol],[300,100])   
            # print(vol1)      
            volume.SetMasterVolumeLevel(vol,None) # The volume level is adjusted by this function
            
            
            
            cv.rectangle(img,(50,100),(100,300),color2,4)
            cv.rectangle(img,(100,300),(50,int(vol1)),color2,cv.FILLED)
        cv.imshow('img',img)
        
        if cv.waitKey(20) & 0xFF ==ord('a'):
            break
        
cv.destroyAllWindows()
    