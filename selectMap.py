import numpy as np
import imutils
import cv2
import math  

def selectMap(img,x_point, y_point,cropping) :
    img = cv2.flip(img,1)

    img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    img = cv2.inRange(img,0,100)
    img = 255-img
    img = cv2.medianBlur(img,5)
    img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)


    if cv2.waitKey(1) & 0xFF == ord('d'):
        keep_fram = img.copy()
        # while 1 :
        print(cropping)
        if cropping :
            startx, starty = x_point, y_point
            # break
        # return keep_fram, 1,img, [startx, starty,20]
    return None, 2,img,[0,0,1000]