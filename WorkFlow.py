from typing import Any
import numpy as np
import cv2 as cv
import os

import utils


class WorkFlow:
    def __init__(self, video_path: str) -> None:
        self.video_path = os.path.join(os.getcwd(), video_path)
        self.frame_cont = 0

    def __call__(self, img_transform, mask_path: str):

        kps = list()
        dess = list()
        cam = cv.VideoCapture(self.video_path)
        mask = cv.cvtColor(cv.imread(os.path.join(os.getcwd(), mask_path)),
                           cv.COLOR_BGR2GRAY)
        
        while cam.isOpened():
            res, frame = cam.read()
            if not res:
                print("Stream is over or anything wrong!")
                break
            result, kp, des = img_transform(frame, mask)
            kps.append(kp)
            dess.append(des)
            cv.imshow('result', result)
            if cv.waitKey(1) == ord('q'):
                break

        cam.release()
        cv.destroyAllWindows()
        return kps, dess


if __name__ == "__main__":
    test = WorkFlow("data_vision.MTS")
    test_kps, test_dess = test(lambda x, y: utils.orb(x, x, y), "./features_mask/F3_mask.png")
    result = utils.out_put(test_kps, test_dess)
    result = np.array(result)
    np.save("./numpy_rawdata/f3.npy", result)
