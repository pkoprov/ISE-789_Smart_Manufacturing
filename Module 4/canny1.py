import cv2


img = cv2.imread("./dori.jpeg")
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
edges = cv2.Canny(img, 100, 150)


cv2.imshow("Image", img)
cv2.imshow("Canny", edges)
cv2.waitKey(0)
cv2.destroyAllWindows()