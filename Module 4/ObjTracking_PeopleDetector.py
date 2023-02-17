import cv2
import numpy as np
import pandas as pnd

def empty():
    pass


def getPar(x):
    if x == 0:
        x = (4, 4)
    elif x == 1:
        x = (8, 8)
    elif x == 2:
        x = (16, 16)
    elif x == 3:
        x = (32, 32)
    return x


hog = cv2.HOGDescriptor()
hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
# df = pnd.DataFrame()


areaThresh = 20000
sc = 1 + 2 / 100
wS = getPar(0)
pd = getPar(3)

cap = cv2.VideoCapture("Module_4_Data/WIN_20210403_13_38_18_Pro.mp4")
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
new_frame = True

resizedImg = np.zeros((128, 64, 3), np.uint8)

_, img1 = cap.read()
_, img2 = cap.read()
width = int(cap.get(3))  # float `width`
height = int(cap.get(4))  # float `height`
crop = (int(img1.shape[1] / 2), int(img1.shape[0] / 2))
img1 = cv2.resize(img1, crop)
img2 = cv2.resize(img2, crop)

ppl_on_frames = 0
while True:

    diff = cv2.absdiff(img1, img2)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 1)
    _, thresh = cv2.threshold(blur, 15, 255, cv2.THRESH_BINARY)

    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    for cnt in contours:
        (x, y, w, h) = cv2.boundingRect(cnt)

        area = cv2.contourArea(cnt)
        if area > areaThresh:
            cv2.rectangle(img1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            # cv2.putText(img1, "Status:{}".format('Movement'), (10,20), cv2.FONT_HERSHEY_COMPLEX, 1, (0,0,255), 3)

            person = img1[y:y + h, x:x + w]
            factor = 2
            sizeParams = (int(img1.shape[0] / factor), int(img1.shape[1] / factor))
            resizedImg = cv2.resize(person, sizeParams)
            cv2.imshow("Res", resizedImg)

            (rects, weights) = hog.detectMultiScale(resizedImg, winStride=wS, padding=pd, scale=sc)

            for i in rects:
                cv2.rectangle(img1, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(img1, "Status:{}".format('Person Detected'), (10, 20), cv2.FONT_HERSHEY_COMPLEX, 1,
                            (0, 0, 255), 3)
                if new_frame:  # count the frame only once in the "for" loop
                    ppl_on_frames += 1
                    new_frame = False

    # imgcnt = cv2.drawContours(img1, contours, -1, (0,255,0), 2)
    cv2.imshow('Analysis', img1)
    # cv2.imshow('ddAnalysis', diff)

    img1 = img2
    ret, img2 = cap.read()
    if ret == True:
        img2 = cv2.resize(img2, crop)
        new_frame = True
    else:
        print('Area = ', areaThresh,', winstride = ', wS, ', padding = ', pd, ', scale = ', sc)
        print("# of frames with people " + str(ppl_on_frames))
        # df = df.append([[areaThresh, wS, pd, sc, ppl_on_frames]])
        break

    if cv2.waitKey(2) & 0xFF == ord('q'):
        print('Area = ', areaThresh,', winstride = ', wS, ', padding = ', pd, ', scale = ', sc)
        # print("Total frames " +str(total_frames))
        print("# of frames with people " + str(ppl_on_frames))
        # df = df.append([[areaThresh,wS,pd,sc,ppl_on_frames]])
        break
# df.to_excel('Person.xlsx')