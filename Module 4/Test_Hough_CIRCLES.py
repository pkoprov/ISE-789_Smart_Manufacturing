import cv2
import numpy as np

def empty():
    pass

img = cv2.imread("./Module_4_Data/bolt.jpg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2. Canny(gray, 80, 200)

cv2.namedWindow("Parameters")
cv2.resizeWindow("parameters", 500,400)
cv2.createTrackbar('dp', "Parameters",1,3,empty)
cv2.createTrackbar('minDist', "Parameters",20,50,empty)
cv2.createTrackbar('param1', "Parameters",1,100,empty)
cv2.createTrackbar('param2', "Parameters",1,100,empty)
cv2.createTrackbar('minRadius', "Parameters",0,100,empty)
cv2.createTrackbar('maxRadius', "Parameters",0,100,empty)
while True:
    dp = cv2.getTrackbarPos('dp', "Parameters")
    minDist = cv2.getTrackbarPos('minDist', "Parameters")
    param1 = cv2.getTrackbarPos('param1', "Parameters")
    param2 = cv2.getTrackbarPos('param2', "Parameters")
    minRadius = cv2.getTrackbarPos('minRadius', "Parameters")
    maxRadius = cv2.getTrackbarPos('maxRadius', "Parameters")


    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT,1,20, param1=50,param2=30,minRadius=minRadius,maxRadius=maxRadius)
    circles = np.uint16(np.around(circles))
    for i in circles[0,:]:
        # draw the outer circle
        cv2.circle(img,(i[0],i[1]),i[2],(0,255,0),2)
        # draw the center of the circle
        cv2.circle(img,(i[0],i[1]),2,(0,0,255),3)


    cv2.imshow('houghlines',img)

    if cv2.waitKey(1) & 0xFF == ord('w'):
        cv2.destroyWindow('houghlines')
    elif cv2.waitKey(1) & 0xFF == ord('q'):
        break