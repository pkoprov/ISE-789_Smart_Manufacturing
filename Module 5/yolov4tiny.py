# download coco.names YoloV3 config and weights file and place it in the YOLOv3 sub-directory
# Download YOLOV3.cfg from https://github.com/pjreddie/darknet/tree/master/cfg
# Download coco.names from https://github.com/pjreddie/darknet/tree/master/data
# Download weights from https://pjreddie.com/media/files/yolov3.weights

import cv2
import numpy as np
import sys
import numpy as np
import os.path
import argparse
import time

# Initialize the parameters
confThreshold = 0.5  # Confidence threshold
nmsThreshold = 0.4  # Non-maximum suppression threshold - changing this value will adjust how many overlapping boxes

parser = argparse.ArgumentParser(description='Object Detection using YOLO in OPENCV')
parser.add_argument('--image', help='Path to image file.')
parser.add_argument('--video', help='Path to video file.')
args = parser.parse_args()

# Load names of classes from coco

classes = open('YOLOv3/coco.names').read().strip().split('\n')

net = cv2.dnn.readNetFromDarknet("YOLOv3/yolov4-tiny.cfg", "YOLOv3/yolov4-tiny.weights")
net.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
net.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)  # set to CUDA if you have it on your machine


# Get the names of the output layers
def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]


# Draw the predicted bounding box
def drawBbox(classId, conf, left, top, right, bottom):
    # Draw a bounding box.
    cv2.rectangle(frame, (left, top), (right, bottom), (255, 178, 50), 3)

    label = '%.2f' % conf

    # Get the label for the class name and its confidence
    if classes:
        assert (classId < len(classes))
        label = '%s:%s' % (classes[classId], label)

    # Display the label at the top of the bounding box
    labelSize, baseLine = cv2.getTextSize(label, cv2.FONT_HERSHEY_COMPLEX, 1.0, 1)
    bottom = max(bottom, labelSize[1])
    cv2.rectangle(frame, (left, bottom - round(0.75 * labelSize[1])),
                  (left + round(0.75 * labelSize[0]), bottom + baseLine), (255, 255, 255), cv2.FILLED)
    cv2.putText(frame, label, (left, bottom), cv2.FONT_HERSHEY_COMPLEX, 0.75, (255, 0, 0), 1)


# Remove the bounding boxes with low confidence using non-maxima suppression
def process(frame, outclasses):
    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    # Scan through all the bounding boxes output from the network and keep only the
    # ones with high confidence scores. Assign the box's class label as the class with the highest score.
    classIds = []
    confidences = []
    boxes = []
    for out in outclasses:
        for detection in out:
            probScores = detection[5:]
            classId = np.argmax(probScores)
            confidence = probScores[classId]
            if confidence > confThreshold:
                centerX = int(detection[0] * frameWidth)
                centerY = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(centerX - width / 2)
                top = int(centerY - height / 2)
                classIds.append(classId)
                confidences.append(float(confidence))
                boxes.append([left, top, width, height])

    # Perform non-maximum suppression to eliminate redundant
    # overlapping boxes with lower confidences
    indices = cv2.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)
    for ind in indices:
        idx = ind[0]
        box = boxes[idx]

        # dimensions of bbox
        left = box[0]
        top = box[1]
        width = box[2]
        height = box[3]
        drawBbox(classIds[idx], confidences[idx], left, top, left + width, top + height)


def rescaleFrame(frame, factor=100):
    width = int(frame.shape[1] * factor / 100)
    height = int(frame.shape[0] * factor / 100)
    dim = (width, height)
    return cv2.resize(frame, dim, interpolation=cv2.INTER_AREA)


# MAIN START
if (args.image):
    # Open the image file
    if not os.path.isfile(args.image):
        print("Image file ", args.image, " missing")
        sys.exit(1)
    outFile = args.image[:-4] + '_YOLOv4tiny.jpg'
else:
    # Open the video file
    if not os.path.isfile(args.video):
        print("Video file ", args.video, " missing")
        sys.exit(1)
    cap = cv2.VideoCapture(args.video)
    outFile = args.video[:-4] + '_YOLOv4tiny.avi'

# Get the video writer initialized to save the output video
if (not args.image):
    fourcc = cv2.VideoWriter_fourcc('M', 'J', 'P', 'G')
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    size = (frame_width, frame_height)
    vid_writer = cv2.VideoWriter(outFile, fourcc, 10, size)

# throttle time limit to speed up calculation, but you will loose boxes, so stay within 0.5 to 1.0s
fpsLimit = 2.0
startTime = time.time()

while cv2.waitKey(1) < 0:

    ret, frame = cap.read()

    # Stop if end of the video and release properly
    if not ret:
        print("YOLOv4tiny output location :  ", outFile)
        cv2.waitKey(6000)
        cap.release()
        break

    # reduce size of image from 25-75% - this controls speed of calculation
    frame = rescaleFrame(frame, factor=100)

    nowTime = time.time()
    if (int(nowTime - startTime)) > fpsLimit:

        # Create a 4D blob from the frame
        blob = cv2.dnn.blobFromImage(frame, 1 / 255, (416, 416), [0, 0, 0], 1, crop=False)

        # Sets the input to the network
        net.setInput(blob)

        # Runs the forward pass to get output of the output layers
        outc = net.forward(getOutputsNames(net))

        # Remove the bounding boxes with low confidence
        process(frame, outc)

        # Write the frame with the detection boxes - you can comment this sectino if you do not want to save the model to you disk
        if (args.image):
            cv2.imwrite(outFile, frame.astype(np.uint8))
        else:
            vid_writer.write(frame.astype(np.uint8))

        # reset time
        nowTime = time.time()

    # cv2.imshow('Image', frame)