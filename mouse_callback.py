import cv2 as cv 
import numpy as np

# ix, iy, drawing, over

def get_shi_mask(event, x, y, flags, param):
    global ix, iy, drawing, over
    
    drawing = False
    over = False
    
    if event == cv.EVENT_LBUTTONDOWN:
        drawing = True
        ix, iy = x, y

    elif event == cv.EVENT_MOUSEMOVE:
        mode = 1
        # if drawing == True:
            # cv.rectangle(param[0], (ix, iy), (x, y), (0, 255, 0), -1)

    elif event == cv.EVENT_LBUTTONUP:
        over = True
        ex, ey = x, y
        # drawing = False
        # cv.rectangle(param[0], (ix, iy), (x, y), (0, 255, 0), -1)
    
    if over == True:
        param[1][iy:y, ix:x] = 255
        over == False
        # 

    

