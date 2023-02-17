import cv2

vFrames1 = cv2.VideoCapture(0)


while True:
    ret, frame1 = vFrames1.read()

    color = cv2.cvtColor(frame1, cv2.COLOR_BGR2BGRA)


    cv2.imshow('frame1', frame1)
    cv2.imshow('frame2', color)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.release()
cv2.destroyAllWindows()