import cv2 as cv
import numpy as np


def empty():
    pass


def getContours(img, fig, col_on_frames, frame_count, light_on=False):
    new_frame = True    # flag for the new frame
    frame_count += 1    # count of frames for the frames elapsed
    contours, hierarchy = cv.findContours(img, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    if not contours and light_on == True: # if the light is off and the flag is on
        light_on = False # flag for the light on

    for cnt in contours:
        area = cv.contourArea(cnt)
        areaThresh = cv.getTrackbarPos("Area", "Parameters")
        if area > areaThresh:
            light_on = True # flag for the light on
            perimeter = cv.arcLength(cnt, True)
            approxVertices = cv.approxPolyDP(cnt, 0.05 * perimeter, True)
            x, y, w, h = cv.boundingRect(approxVertices)
            cv.rectangle(fig, (x, y), (x + w, y + h), (0, 0, 255), 2)
            if new_frame: # count the frame only once in the "for" loop
                col_on_frames += 1
                new_frame = False

    return col_on_frames, frame_count, light_on


video = cv.VideoCapture("./Module_4_Data/testing.mp4")
fps = video.get(cv.CAP_PROP_FPS)
total_frames = int(video.get(cv.CAP_PROP_FRAME_COUNT))
duration = total_frames / fps
cur_frame = 0 # elapsed frames count
blue_on_frames = 0 # number of FRAMES with blue light on
blue_count = 0  # number of TIMES blue light was turned on
blue_is_on = False # flag for the blue light on


if video.isOpened() == False:
    print("Error opening video")

cv.namedWindow("Parameters")
cv.resizeWindow("Parameters", 500, 400)
cv.createTrackbar("Hue min", "Parameters", 90, 255, empty)
cv.createTrackbar("Hue max", "Parameters", 130, 255, empty)
cv.createTrackbar("Saturation min", "Parameters", 125, 255, empty)
cv.createTrackbar("Saturation max", "Parameters", 255, 255, empty)
cv.createTrackbar("Value min", "Parameters", 200, 255, empty)
cv.createTrackbar("Value max", "Parameters", 255, 255, empty)
cv.createTrackbar("Area", "Parameters", 50, 200, empty)

while video.isOpened():
    ret, frame = video.read()
    if ret == True:
        frame = cv.resize(frame, (960, 540))
        hsvFr = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

        hue_min = cv.getTrackbarPos("Hue min", "Parameters")
        hue_max = cv.getTrackbarPos("Hue max", "Parameters")
        sat_min = cv.getTrackbarPos("Saturation min", "Parameters")
        sat_max = cv.getTrackbarPos("Saturation max", "Parameters")
        val_min = cv.getTrackbarPos("Value min", "Parameters")
        val_max = cv.getTrackbarPos("Value max", "Parameters")


        lbound = np.array([hue_min, sat_min, val_min])
        upbound = np.array([hue_max, sat_max, val_max])

        mask = cv.inRange(hsvFr, lbound, upbound)
        result = cv.bitwise_and(frame, frame, mask=mask)

        dummy = blue_is_on  # dummy variable to compare new light_on flag with previous frame
        blue_on_frames, cur_frame, blue_is_on = getContours(mask, frame, blue_on_frames, cur_frame)
        if (blue_is_on != dummy) & (blue_is_on):    # check if the light_on flag changed and if it has turned to blue
            blue_count += 1

        # calculation of elapsed time
        elapsed_time = cur_frame / fps
        minutes = int(elapsed_time / 60)
        seconds = elapsed_time % 60

        # display the time
        x = f"Elapsed time: {str(minutes)}:{str(int(seconds))}/{int(duration/60)}:{int(duration) % 60}"
        cv.putText(frame, x, (50,50), cv.FONT_HERSHEY_SIMPLEX,1, (0, 0, 255), 2, cv.LINE_AA)

        cv.imshow('Original', frame)
        # cv.imshow('HSV', hsvFr)
        cv.imshow('Mask', mask)
        cv.imshow('Filtered', result)

        if cv.waitKey(25) & 0xFF == ord('q'):
            break
    else:
        break
print(f"Total frames = {cur_frame}")
print(f"Blue light is on {blue_on_frames} frames or {round(blue_on_frames/fps,2)} seconds")
print(f"Blue appeared {blue_count} times")

video.release()
cv.destroyAllWindows()
