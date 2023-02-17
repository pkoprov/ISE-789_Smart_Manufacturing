import cv2
import numpy as np


def empty():
    pass


cap = cv2.VideoCapture(0)
frameWidth = 640
frameHeight = 480

cap.set(3, frameWidth)
cap.set(4, frameHeight)

# Setup our parameters trackers
cv2.namedWindow("Parameters")
cv2.resizeWindow("Parameters", 500, 400)
cv2.createTrackbar("Threshold1", "Parameters", 36, 255, empty)
cv2.createTrackbar("Threshold2", "Parameters", 181, 255, empty)
cv2.createTrackbar("Area", "Parameters", 0, 10000, empty)


def getContours(img, contours):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        area = cv2.contourArea(cnt)
        areaThresh = cv2.getTrackbarPos("Area", "Parameters")

        if area > areaThresh:
            perimeter = cv2.arcLength(cnt, True)
            approxVertices = cv2.approxPolyDP(cnt, 0.02 * perimeter, True)
            # print(area, len(approxVertices))
            if len(approxVertices) == 4:
                cv2.drawContours(imgContour, cnt, -1, (0, 0, 255), 5)
                x, y, w, h = cv2.boundingRect(approxVertices)
                cv2.rectangle(imgContour, (x, y), (x + w, y + h), (0, 255, 0), 5)
                cv2.putText(imgContour, "Points: " + str(len(approxVertices)), (x + w + 20, y + 20),
                            cv2.FONT_HERSHEY_COMPLEX, 0.7, (0, 255, 0), 2)
                cv2.putText(imgContour, "Area: " + str(int(area)), (x + w + 20, y + 45), cv2.FONT_HERSHEY_COMPLEX, 0.7,
                            (0, 255, 0), 2)


while True:
    ret, img = cap.read()

    imgContour = img.copy()

    imgBlur = cv2.GaussianBlur(img, (7, 1), 1)
    imgGray = cv2.cvtColor(imgBlur, cv2.COLOR_BGR2GRAY)

    threshold1 = cv2.getTrackbarPos("Threshold1", "Parameters")
    threshold2 = cv2.getTrackbarPos("Threshold2", "Parameters")
    imgCanny = cv2.Canny(imgGray, threshold1, threshold2)

    kernel = np.ones((3, 3))
    imgDil = cv2.dilate(imgCanny, kernel, iterations=1)

    getContours(imgDil, imgContour)

    # cv2.imshow("Canny Edges", imgCanny)
    # cv2.imshow("Dilated Edges", imgDil)
    cv2.imshow("Contour Edges", imgContour)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break