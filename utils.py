import cv2 as cv
import numpy as np
import math


# 图像锐化
def sharp(img, pic=None, mask=None):
    kernel = np.array([
        [-1, -1, -1],
        [-1, 9, -1],
        [-1, -1, -1]])
    img = cv.filter2D(img, -1, kernel=kernel)
    return img


# Shi-Tomas
def shi(img, pic, mask=None):
    pic = cv.cvtColor(pic, cv.COLOR_BGR2GRAY)
    # pic = cv.GaussianBlur(pic, (3, 3), sigmaX=0, sigmaY=0)
    corners = cv.goodFeaturesToTrack(pic, 2, 0.5, 20, blockSize=9, mask=mask)
    corners = np.int0(corners)
    results = []
    for corner in corners:
        x, y = corner.ravel()
        cv.circle(img, (x, y), 3, (0, 0, 255), -1)
        results.append([int(x), int(y)])
    return img, results


# canny
def edge(pic):
    gray = cv.cvtColor(pic, cv.COLOR_BGR2GRAY)
    gray = cv.GaussianBlur(gray, (5, 5), sigmaX=0, sigmaY=0)
    edges = cv.Canny(image=gray, threshold1=100, threshold2=200)

    return edges


# SIFT
def sift(img, pic, mask=None):

    pic = cv.cvtColor(pic, cv.COLOR_BGR2GRAY)
    detector = cv.SIFT.create()
    kp, des = detector.detectAndCompute(pic, mask)
    img = cv.drawKeypoints(img, kp, img, color=(0, 255, 255))
    return img, kp, des

# mouse call back
# 返回一个矩形
def get_rectangle_mask(event, x, y, flags, param):
    global ix, iy, drawing, over

    drawing = False
    over = False
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y
    elif event == cv.EVENT_MOUSEMOVE:
        mode = 1
    elif event == cv.EVENT_LBUTTONUP:
        over = True
        ex, ey = x, y

    if over:
        param = [[ix, iy], [x, y]]
        over = False


# SURF 专利问题无法使用
def surf(img, pic, mask=None):
    pic = cv.cvtColor(pic, cv.COLOR_BGR2GRAY)
    detector = cv.xfeatures2d.SURF.create(400)
    kp, des = detector.detectAndCompute(pic, mask)
    img = cv.drawKeypoints(img, kp, img, color=(0, 255, 255))
    return img, kp, des


# ORB
def orb(img, pic, mask=None):
    pic = cv.cvtColor(pic, cv.COLOR_BGR2GRAY)
    detector = cv.ORB.create(50)
    kp, des = detector.detectAndCompute(pic, mask)
    img = cv.drawKeypoints(img, kp, img, color=(0, 255, 255))
    return img, kp, des


# 位移计算
def distance(x1, y1, x2, y2):
    moving_x = x2 - x1
    moving_y = y2 - y1
    moving_dist = math.sqrt(moving_x ** 2 + moving_y ** 2)
    if moving_y < 0:
        moving_dist = - moving_dist
    return moving_dist


# 两帧之间的位移计算
def match_movingCaculate(kp1, kp2, des1, des2):
    bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    moving_sum = 0
    for match in matches[:10]:
        x1 = kp1[match.queryIdx].pt[0]
        y1 = kp1[match.queryIdx].pt[1]
        x2 = kp2[match.trainIdx].pt[0]
        y2 = kp2[match.trainIdx].pt[1]
        moving_sum += distance(x1, y1, x2, y2)

    return moving_sum / 10


# 视频的整个处理
def out_put(kps, dess):
    movings = list()
    for i in range(len(kps)):
        movings.append(match_movingCaculate(kps[100], kps[i], dess[100], dess[i]))
    movings = np.array(movings)
    return movings
