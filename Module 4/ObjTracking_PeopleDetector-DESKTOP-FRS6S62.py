import cv2
import numpy as np
from skimage.feature import hog

cap = cv2.VideoCapture(
    r'E:\STARLY\NCSU_Data\Teaching\ISE789_Smart_Mfg\Lecture_Video\Lecture Content\SmartManufacturing\Part_4_4_TrackObjects\test.mp4')

ret, img1 = cap.read()
ret, img2 = cap.read()
width = int(cap.get(3))  # float `width`
height = int(cap.get(4))  # float `height`

jj = hog.
hog.setSVMDetector(cv2.)

resizedImg = np.zeros((128, 64, 3), np.uint8)
while True:

    diff = cv2.absdiff(img1, img2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 1)
    _, thresh = cv2.threshold(blur, 15, 255, cv2.THRESH_BINARY)

    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)
        # area based box.
        area = cv2.contourArea(cnt)
        if area > 30000:
            cv2.rectangle(img1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # cv2.putText(img1, "Status:{}".format('Movement'), (10,20), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 3)

            person = img1[y:y + h, x:x + w]
            factor = 2
            sizeParams = (int(img1.shape[0] / factor), int(img1.shape[1] / factor))
            resizedImg = cv2.resize(person, sizeParams)

            (rects, weights) = hog.detectMultiScale(resizedImg, winStride=(8, 8), padding=(8, 8), scale=1.04)
            for (xs, ys, ws, hs) in rects:
                cv2.rectangle(img1, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(img1, "Status:{}".format('Person Detected'), (10, 20), cv2.FONT_HERSHEY_COMPLEX, 1,
                            (0, 0, 255), 3)

    # imgcnt = cv2.drawContours(img1, contours, -1, (0,255,0), 2)
    cv2.imshow('Analysis', img1)
    cv2.imshow('ddAnalysis', diff)

    img1 = img2
    ret, img2 = cap.read()

    if cv2.waitKey(2) & 0xFF == ord('q'):
        break