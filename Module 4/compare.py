from skimage.metrics import structural_similarity as ssim
from skimage.metrics import normalized_root_mse as nrmse

import matplotlib.pyplot as plt
import cv2
import numpy as np


def findmse(refA, test):
    err = np.sum((refA.astype('float') - test.astype('float')) ** 2)
    err /= float(refA.shape[0] * refA.shape[1])

    nerr = nrmse(refA, test, normalization="euclidean")
    return err, nerr

def img_comp(refA, test, title):
    s = ssim(refA, test, win_size=7)
    mse, nrmse =  findmse(refA,test)

    fig = plt.figure(title)
    plt.suptitle("SSIM: %.2f MSE: %.2f Normalized MSE: %.2f" %(s, mse, nrmse), ha="center")

    ax1 = fig.add_subplot(1,2,1)
    ax1.title.set_text("Reference image")
    plt.imshow(refA, cmap=plt.cm.gray)

    ax2 = fig.add_subplot(1,2,2)
    ax2.title.set_text("test image")
    plt.imshow(test, cmap=plt.cm.gray)

    plt.show()


refA = cv2.imread("./Module_4_Data/ansi41sprocket1020.png")
testA = cv2.imread("./Module_4_Data/ansi41sprocket1020_v2.png")
testB= cv2.imread("./Module_4_Data/ansi41sprocket1020_v3.png")

ref2A = cv2.imread("./Module_4_Data/ok_casting.jpeg")
test2A = cv2.imread("./Module_4_Data/defective_casting.jpeg")
test2B= cv2.imread("./Module_4_Data/ok_casting_2.jpeg")

# cv2.imshow("RefA", refA)
# cv2.imshow("Test", testA)

# cv2.waitKey(0)
# cv2.destroyAllWindows()

refA = cv2.cvtColor(refA, cv2.COLOR_BGR2GRAY)
testA = cv2.cvtColor(testA, cv2.COLOR_BGR2GRAY)
testB = cv2.cvtColor(testB, cv2.COLOR_BGR2GRAY)

ref2A = cv2.cvtColor(ref2A, cv2.COLOR_BGR2GRAY)
test2A = cv2.cvtColor(test2A, cv2.COLOR_BGR2GRAY)
test2B = cv2.cvtColor(test2B, cv2.COLOR_BGR2GRAY)


fig = plt.figure("Image Comparison")
images = [("Reference", refA), ("Test A", testA), ("Test B", testB),
          ("Reference", ref2A), ("Test A", test2A), ("Test B", test2B)]

for (i, (name, image)) in enumerate(images):
    a = fig.add_subplot(2,3, i+1)
    a.set_title(name)
    plt.imshow(image, cmap = plt.cm.gray)

plt.show()

img_comp(refA, refA, "RefA VS RefA")
img_comp(refA, testA, "RefA VS TestA")
img_comp(refA, testB, "RefA VS TestB")
img_comp(ref2A, ref2A, "Ref2A VS Ref2A")
img_comp(ref2A, test2A, "Ref2A VS Test2A")
img_comp(ref2A, test2B, "Ref2A VS Test2B")