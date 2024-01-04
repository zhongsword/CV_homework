import cv2 as cv
import numpy as np
import os
pts = []


def draw_polygon(event, x, y, flags, param):
    global pts
    if event == cv.EVENT_LBUTTONDOWN:
        pts.append([x, y])
    elif event == cv.EVENT_RBUTTONDOWN:
        pts = []


def mask_drawer(video_path: str, output_path: str):
    global pts
    video_path = os.path.join(os.getcwd(), video_path)
    out_path = os.path.join(os.getcwd(), "features_mask", video_path)
    cam = cv.VideoCapture(video_path)
    ret, frame = cam.read()
    frame_raw = frame
    cam.release()
    cv.namedWindow('frame')
    mask = np.zeros_like(frame[..., 0])
    cv.setMouseCallback("frame", draw_polygon)

    while True:
        cv.imshow('frame', frame)
        key = cv.waitKey(1)
        if key == ord('c'):
            frame = frame_raw
        elif key == ord('q'):
            break
        elif key == 13:
            pts = np.array(pts, np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv.polylines(frame, [pts], True, (0, 255, 255), 3)
            mask = cv.fillPoly(mask, [pts], (255))
            cv.imwrite(out_path, mask)
            pts = []

    cv.destroyAllWindows()


if __name__ == '__main__':
    videopath = 'data_vision.MTS'
    output_path = 'F4_mask.png'
    mask_drawer(videopath, output_path)
