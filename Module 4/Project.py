import cv2
import matplotlib.pyplot as plt

vFrames1 = cv2.VideoCapture("http://10.154.61.143:8080/video?dummy=param.mjpg")

def imShow(frame):
  height, width = frame.shape[:2]
  resized_image = cv2.resize(frame,(3*width, 3*height), interpolation = cv2.INTER_CUBIC)

  fig = plt.gcf()
  fig.set_size_inches(18, 10)
  plt.axis("off")
  plt.imshow(cv2.cvtColor(resized_image, cv2.COLOR_BGR2RGB))
  plt.show()

while True:
  ret, frame = vFrames1.read()

  cv2.imshow('frame1', frame)
  # imShow(frame)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break
vFrames1.release()
cv2.destroyAllWindows()