import cv2
import numpy as np

img = cv2.imread(r'C:\Users\pkoprov\OneDrive - North Carolina State University\ISE 789 Smart Manufacturing\Module 4\Module_4_Data\bolt2.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2. Canny(gray, 10, 200)

lines = cv2.HoughLines(edges, 1, np.pi/180,190)
cv2.imshow('houghlines1',edges)
for line in lines:
   for rho, theta in line:
       a = np.cos(theta)
       b = np.sin(theta)

       x0 = a*rho
       y0 = b*rho

       pt1 = (int(x0 + 1000 * (-b)), int(y0 + 1000 * (a)))
       pt2 = (int(x0 - 1000 * (-b)), int(y0 - 1000 * (a)))
       cv2.line(img, pt1, pt2, (0, 255,0), 2)

cv2.imshow('houghlines',img)
cv2.waitKey(0)
# if cv2.waitKey(1) & 0xFF == ord('w'):
#     cv2.destroyWindow('houghlines')