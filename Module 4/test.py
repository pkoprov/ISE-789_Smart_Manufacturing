import cv2

img = cv2.imread('dori.jpeg')
imGray = cv2.imread('dori.jpeg', 0)
thresh, img_BW = cv2.threshold(imGray, 128, 255, cv2.THRESH_BINARY)
thresh, img_BW2 = cv2.threshold(imGray, 128, 255, cv2.THRESH_BINARY|cv2.THRESH_OTSU)
cv2.imshow('image color', img)
cv2.waitKey(0)

cv2.imshow('image Gray', imGray)
cv2.waitKey(0)

cv2.imshow('image black and white', img_BW)
cv2.waitKey(0)
cv2.imshow('image black and white2', img_BW2)
cv2.waitKey(0)


cv2.destroyAllWindows()
