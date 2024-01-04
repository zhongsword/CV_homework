import cv2 as cv
import numpy as np

## Shi-Tomasi
def shi(img, pic, mask=None):
    corners = cv.goodFeaturesToTrack(pic, 2, 0.5, 20, blockSize=9, mask=mask)
    corners = np.int0(corners)
    for corner in corners:
        x, y = corner.ravel()
        cv.circle(img, (x, y), 3, (0, 0, 255), -1)
    return img, corners

## canny
def edge(pic):
    gray = cv.cvtColor(pic, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (5, 5), sigmaX=0, sigmaY=0)
    edges = cv.Canny(image=gray, threshold1=100, threshold2=200)

    return edges
