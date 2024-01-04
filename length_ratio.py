import cv2 as cv
import os
import math

floor_length = 240
cont = 0
cor_list = []


def getpoint(event, x, y, flags, param):
    global cont
    global floor_length
    global cor_list
    if event == cv.EVENT_LBUTTONDOWN:
        cor_list.append(x)
        cor_list.append(y)
        cont += 1

    if cont == 2:
        length_r = floor_length / math.sqrt((cor_list[1] - cor_list[3]) ** 2 + (cor_list[0] - cor_list[2]) ** 2)
        print(f"length_ratio = {length_r}")
        cont = 0
        cor_list = []


def length_ratio(video_path: str):
    video_path = os.path.join(os.getcwd(), video_path)
    out_path = os.path.join(os.getcwd(), "features_mask", video_path)
    cam = cv.VideoCapture(video_path)
    ret, frame = cam.read()
    frame_raw = frame
    cam.release()
    cv.namedWindow('frame')
    cv.setMouseCallback('frame', getpoint)

    while True:
        cv.imshow('frame', frame)
        key = cv.waitKey(1)
        if key == ord('c'):
            frame_raw = frame
        elif key == ord('q'):
            break


if __name__ == '__main__':
    video_path = './data_vision.MTS'
    length_ratio(video_path)


# 使用层宽的到的数据
# length_ratio = 4.965839411399964
# length_ratio = 4.696492255306906
# length_ratio = 4.468696382511016
# length_ratio = 4.348565981543342

# 使用柱宽得到的数据
# length_ratio = 9.086404552310174
# length_ratio = 8.441900168164679
# length_ratio = 7.410864584109404
# length_ratio = 7.352941176470588

# 使用板厚得到的数据
# length_ratio = 9.223949304289054
# length_ratio = 7.982281262852871
# length_ratio = 6.8320913077148635
# length_ratio = 5.851918189130049

