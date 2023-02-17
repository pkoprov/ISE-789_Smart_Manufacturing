import cv2
import numpy as np

vFrames = cv2.VideoCapture(0)

while True:

    ret, frame = vFrames.read()

    hsvFr = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lbound = np.array([12,60,180])
    upbound = np.array([105,115,191])

    mask = cv2.inRange(hsvFr, lbound, upbound)

    result = cv2.bitwise_and(frame, frame, mask=mask)

    cv2.imshow('Original', frame)
    cv2.imshow('HSV', hsvFr)
    cv2.imshow('Mask', mask)
    cv2.imshow('Filtered', result)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()