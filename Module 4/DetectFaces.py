import numpy as np
import cv2 as cv

img = cv.imread("Module_4_Data/3.JPG")
print(f"Image Height {img.shape[0]}")
print(f"Image Width {img.shape[1]}")
fact = 3
resizedImg = cv.resize(img, (int(img.shape[1]/fact),int(img.shape[0]/fact)))


hog = cv.HOGDescriptor()
hog.setSVMDetector(cv.HOGDescriptor_getDefaultPeopleDetector())
(rects, weights) = hog.detectMultiScale(resizedImg, winStride=(4, 4), padding=(4, 4), scale=1.04)

for (x, y, w, h) in rects:
    cv.rectangle(resizedImg, (x, y), (x + w, y + h), (255, 0, 0), 2)

cv.imshow('img', resizedImg)
cv.waitKey(0)
cv.destroyAllWindows()