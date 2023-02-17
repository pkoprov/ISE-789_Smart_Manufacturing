import numpy as np
import cv2

im = cv2.imread('dori.jpeg')
imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)



ret,thresh = cv2.threshold(imgray,10,255,0)
contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

cv2.imshow('image color', imgray)
im2 = cv2.drawContours(im, contours, -1, (0, 255, 0), 3)
cv2.waitKey(0)
cv2.imshow('image color2', im2)
cv2.waitKey(0)