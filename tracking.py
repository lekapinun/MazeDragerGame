import numpy as np
import imutils
import cv2
import math 

def tracking(frame,lower,upper,center_old,flag,keep,control_fast) :
    
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)

    kernel = np.ones((9,9),np.uint8)
    mask = cv2.inRange(hsv, lower, upper)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)

    cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE)[-2]
    center = None

    if len(cnts) > 0:
        # find the largest contour in the mask, then use
        # it to compute the minimum enclosing circle and
        # centroid
        c = max(cnts, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        M = cv2.moments(c)
        center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
            
        # only proceed if the radius meets a minimum size. Correct this value for your obect's size
        if radius < 60 and radius > 10:
            print(radius)       
            print(flag)     
            if(flag==1):
                if math.sqrt(math.pow(center[0]-center_old[0],2)+math.pow(center[1]-center_old[1],2))<control_fast:
            # draw the circle and centroid on the frame,
            # then update the list of tracked points
                    cv2.circle(frame, (int(x), int(y)), int(radius), (255, 0, 0),5)
                    cv2.putText(frame, 'center: {}, {}'.format(int(x), int(y)), (int(x-radius),int(y-radius)), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,0,255), 2)
                    flag=0
                else:
                    keep=[center_old[0],center_old[1],control_fast]
                    # keep[2]=control_fast
                    flag=2
            if(flag==0):
                center_old=center
                flag=1
            if(flag==2):
                cv2.circle(frame,(int(keep[0]),int(keep[1])),int(keep[2]),(0,0,255),5)
                if math.sqrt(math.pow(center[0]-keep[0],2)+math.pow(center[1]-keep[1],2))<keep[2]:
                    center_old=center
                    flag=1
            # print(center,center_old)
    else :
        if (flag == 1) :
            keep=[center_old[0],center_old[1],control_fast]
            # keep[2]=control_fast
            flag=2
    # if(flag==2):
    #     cv2.circle(frame,(int(keep[0]),int(keep[1])),int(keep[2]),(0,0,255),5)
    frame = cv2.resize(frame,(0,0),fx=0.2,fy=0.2)
    return frame,center,center_old,flag,keep