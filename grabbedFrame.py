import numpy as np
import imutils
import cv2
import math 

def grabbedFrame(im,ret,cropping,getROI,x_start, y_start, x_end, y_end) :
    # cv2.imshow('image', im)
    frame = im.copy()
    if not ret:
        print('dont have frame')
        return 0

    # frame=cv2.flip(frame,1)       
    if not cropping and not getROI:
        return im , 0, 0 , 0

    elif cropping and not getROI:
        cv2.rectangle(im, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
        return im , 0, 0 , 0

    elif not cropping and getROI:
        cv2.rectangle(im, (x_start, y_start), (x_end, y_end), (0, 255, 0), 2)
        if x_start > x_end :
            temp = x_end
            x_end = x_start
            x_start = temp
        if y_start > y_end :
            temp = y_end
            y_end = y_start
            y_start = temp
        lower,upper = selectColor(frame,x_start, y_start, x_end, y_end)
        return im , lower, upper , 2

def selectColor(frame,x_start, y_start, x_end, y_end) :
    refPt = [(x_start, y_start), (x_end, y_end)]

    roi = frame[refPt[0][1]:refPt[1][1], refPt[0][0]:refPt[1][0]]
        #cv2.imshow("ROI", roi)

    hsvRoi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
    print('min H = {}, min S = {}, min V = {}; max H = {}, max S = {}, max V = {}'.format(hsvRoi[:,:,0].min(), hsvRoi[:,:,1].min(), hsvRoi[:,:,2].min(), hsvRoi[:,:,0].max(), hsvRoi[:,:,1].max(), hsvRoi[:,:,2].max()))
     
    lower = np.array([hsvRoi[:,:,0].min(), hsvRoi[:,:,1].min(), hsvRoi[:,:,2].min()])
    upper = np.array([hsvRoi[:,:,0].max(), hsvRoi[:,:,1].max(), hsvRoi[:,:,2].max()])
    return lower, upper