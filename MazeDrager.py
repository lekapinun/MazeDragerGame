import numpy as np
import imutils
import cv2
import math  
from grabbedFrame import grabbedFrame
from tracking import tracking
from play import play
from selectMap import selectMap

cap = cv2.VideoCapture(0)
x_start, y_start, x_end, y_end = 0, 0, 0, 0
x_point, y_point = 0, 0
cropping, getROI = False, False
refPt = []
lower, upper = np.array([]), np.array([])
option = 0
center, center_old = [0,0], [0,0]
count = 0
fast_control=640
userCam = []
keep = [0,0,20]
mapGame = []
startPoint = []
startedgame=False
stratScence = cv2.imread('IMG//main.jpg')
stratScence2 = cv2.imread('IMG//main2.jpg')
mapMenu = cv2.imread('IMG//save.jpg')
sad = cv2.imread('IMG//tryagain.jpg')
keep_fram = []
flag = 0
listMap = []
selectMap = 99

def click_and_crop(event, x, y, flags, param):
    global x_start, y_start, x_end, y_end, cropping, getROI, x_point, y_point

    if event == cv2.EVENT_LBUTTONDOWN:
        x_start, y_start, x_end, y_end = x, y, x, y
        cropping = True
        x_point, y_point = x, y
        print(x_point, y_point)

    elif event == cv2.EVENT_MOUSEMOVE:
        if cropping == True:
            x_end, y_end = x, y

    elif event == cv2.EVENT_LBUTTONUP:
        x_end, y_end = x, y
        cropping = False
        if x_start != x_end and y_start != y_end:
            getROI = True

cv2.namedWindow("image")
cv2.setMouseCallback("image", click_and_crop)

while 1:
    # Menu
    while option == 0:
        if lower != np.array([]) and upper != np.array([]) and selectMap != 99 :
            if x_point > 488 and x_point < 607 and y_point > 155 and y_point < 202 :
                x_point, y_point = 0, 0
                [str_img,str_x,str_y]=listMap[selectMap]
                startPoint=[int(str_x),int(str_y)]
                print(str_img,str_x,str_y)
                mapGame=cv2.imread("Map//"+str_img)
                # startPoint = [x_point, y_point]

                flag = 2
                keep = [startPoint[0],startPoint[1],20]
                option = 1 #start
            cv2.imshow("image",stratScence)
        else :
            cv2.imshow("image",stratScence2)

        
        if x_point > 415 and x_point < 607 and y_point > 225 and y_point < 284 :
            x_point, y_point = 0, 0
            print("selectMap")
            option = 2 #selectMap
        if x_point > 294 and x_point < 607 and y_point > 312 and y_point < 372 :
            x_point, y_point = 0, 0
            cropping = False
            getROI = False
            option = 3 #selectColor
        if x_point > 519 and x_point < 607 and y_point > 391 and y_point < 433 :
            x_point, y_point = 0, 0
            option = 999 #exit

        if cv2.waitKey(1) & 0xFF == ord('q'):
            option = 999

    # Create Map
    while option == 5:
        # ret, img = cap.read()
        # # img = cv2.flip(img,1)
        # img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        # img = cv2.inRange(img,0,125)
        # img = 255-img
        # img = cv2.medianBlur(img,5)
        # img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
        # cv2.imshow("image",img)
        ret, img = cap.read()
        # img = cv2.flip(img,1)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        img = cv2.inRange(img,0,75)
        # img = 255-img
        img = cv2.medianBlur(img,5)
        TampmapGame = img.copy()
        # TampmapGame=255-TampmapGame
        # img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
        newtest=np.zeros(TampmapGame.shape)    
        contourmask = temp,contours,hierarchy = cv2.findContours(TampmapGame, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            x,y,w,h = cv2.boundingRect(cnt)
            if(x==0 or y==0 or x+w==TampmapGame.shape[0] or y+h==TampmapGame.shape[1] or x==TampmapGame.shape[0] or y==TampmapGame.shape[1]):
                print("1")# cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
            else:
                # cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
                if(w*h>1000):
                    newtest[y:y+h,x:x+w]=TampmapGame[y:y+h,x:w+x]
            
        cv2.drawContours(img,contours,-1,(0,0,255),2)
        newtest=255-newtest
        cv2.imshow('image',newtest)
        k = cv2.waitKey(1)
        if k & 0xFF == ord('d'):
            option = 4
            mapGame = newtest.copy()
        elif  k & 0xFF == ord('q'):
            option = 0

    # Select Map
    while option == 2 :

        with open("Map//listMap.txt") as f:
            listMap = [x.strip().split(',') for x in f.readlines()]

        scence = mapMenu.copy()
        sx, sy = 58, 100
        for i in range(0,len(listMap)) :
            if x_point > 58 and x_point < 140 and y_point < sy + 5 and y_point > sy - 20 :
                x_point, y_point = 0, 0
                selectMap = i
                # cv2.circle(scence, (50, sy-5), 2, (212, 114, 255), 2)
            cv2.putText(scence,listMap[i][0],(58,100+(35*i)),cv2.FONT_HERSHEY_PLAIN, 1,(255,255,255),2)
            sy = sy + 35
        cv2.circle(scence, (50, 100+(35*selectMap)-5), 2, (212, 114, 255), 2)

        if selectMap != 99 :
            [str_img,str_x,str_y]=listMap[selectMap]
            startPoint=[int(str_x),int(str_y)]
            PreviewSelectMapGame=cv2.imread("Map//"+str_img)
            cv2.circle(PreviewSelectMapGame, (int(str_x), int(str_y)), 20, (212, 114, 255), 2)
            PreviewSelectMapGame = cv2.resize(PreviewSelectMapGame,(0,0),fx=0.5,fy=0.5)
            PreviewSizeY, PreviewSizeX = PreviewSelectMapGame.shape[0] , PreviewSelectMapGame.shape[1]
            scence[65:65+int(PreviewSizeY),575-int(PreviewSizeX):575] = PreviewSelectMapGame

        cv2.imshow("image",scence)

        if x_point > 301 and x_point < 440 and y_point > 383 and y_point < 438 :
            x_point, y_point = 0, 0
            print("selectMap")
            option = 5
        if x_point > 460 and x_point < 602 and y_point > 383 and y_point < 438 :
            x_point, y_point = 0, 0
            option = 0

        k = cv2.waitKey(1)
        if k & 0xFF == ord('q'):
            x_point, y_point = 0, 0
            option = 0


    # Select Start Point          
    while option == 4:
        temp = mapGame.copy()
        cv2.circle(temp, (x_point, y_point), 20, (0, 255, 0),2)
        cv2.imshow("image",temp)
        k = cv2.waitKey(1)
        if k & 0xFF == ord('d'):
            if len(listMap)  >= 10 :
                # startPoint = [x_point, y_point]
                listMap.remove(listMap[0])
            listMap.append(["img" + str(len(listMap)+1) + ".jpg" , str(x_point) , str(y_point)])
            cv2.imwrite("Map//img" + str(len(listMap)) + ".jpg",mapGame)
            file = open("Map//listMap.txt","w")
            for Map in listMap :
                file.write(Map[0] + ',' + Map[1] + ',' + Map[2] + '\n')
            file.close()

            option = 2 
        elif  k & 0xFF == ord('q'):
            option = 0

    # Selecct Color
    while option == 3:
        ret, img = cap.read()
        img = cv2.flip(img,1)
        img, lower, upper, check = grabbedFrame(img,ret,cropping,getROI,x_start, y_start, x_end, y_end)
        cv2.imshow("image",img)
        if check != 0 :
            cropping = False
            getROI = False
            option = 0
        if cv2.waitKey(1) & 0xFF == ord('q'):
            option = 0

    # Play
    while option == 1 :
        ret, img = cap.read()
        img = cv2.flip(img,1)
        fast_control = 20
        userCam,center,center_old,flag,keep =  tracking(img,lower,upper,center_old,flag,keep,fast_control)

        TempMap = mapGame.copy()

        if center != None and flag == 1:
            TempMap, option = play(mapGame.copy(),center,option)

        TempMap[0:userCam.shape[0],0:userCam.shape[1]] = userCam

        if center != None :
            cv2.circle(TempMap, (int(center[0]), int(center[1])), 2, (0, 255, 0), 2)
        if flag==2 :
            cv2.circle(TempMap, (int(keep[0]), int(keep[1])), 20, (0, 0, 255), 2)

        cv2.imshow("image",TempMap)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            option = 0

    # Dead 69
    while option == 69 :
        ret, img = cap.read()
        img = cv2.flip(img,1)
        fast_control=1000
        userCam,center,center_old,flag,keep =  tracking(img,lower,upper,center_old,flag,keep,fast_control)
        endScene = sad.copy()
        endScene[0:userCam.shape[0],0:userCam.shape[1]] = userCam
        img = endScene.copy()
        print(center)
        if center != None :
            cv2.circle(img, (int(center[0]), int(center[1])), 2, (0, 255, 0), 2)
        if flag==2 :
            cv2.circle(img, (int(keep[0]), int(keep[1])), 20, (0, 0, 255), 2)
        
        cv2.imshow("image",img)

        if center == None :
            center = [ int(keep[0]), int(keep[1]) ]
        if center[0] > 72 and center[0] < 300 and center[1] > 358 and center[1] < 429 :
            count = count + 1
            print(count)
            print("TryAgain")
            if count >= 100:
                x_point, y_point = 0, 0
                flag = 2
                keep = [startPoint[0],startPoint[1],20]
                option = 1
        elif center[0] > 340 and center[0] < 568 and center[1] > 358 and center[1] < 429 :
            count = count + 1
            print(count)
            print("Menu")
            if count >= 100:
                option = 0
        else :
            count = 0
        if cv2.waitKey(1) & 0xFF == ord('q'):
            option = 0
   
    # Exit
    if option == 999:
        break

cap.release()
cv2.destroyAllWindows()