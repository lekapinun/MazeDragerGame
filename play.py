import numpy as np
import imutils
import cv2
import math  

def play(mapGame,center,option) :
    TempMap = mapGame.copy()
    TempMap = cv2.inRange(TempMap,(100,100,100),(255,255,255))
    # cv2.putText(mapGame,str(TempMap[center[1],center[0]]),(500,100),cv2.FONT_HERSHEY_PLAIN, 5,(255,0,0))
    if TempMap[center[1],center[0]] != 255 or TempMap[center[1],center[0]+1] != 255 or TempMap[center[1]+1,center[0]] != 255 or TempMap[center[1]+1,center[0]+1] != 255:
        # cv2.putText(mapGame,'DAMN!!!',(500,100),cv2.FONT_HERSHEY_PLAIN, 5,(255,0,0))
        option = 69
    
    return mapGame,option