CV大作业
------------
## 项目结构
```md
+-features_mask     检测时使用的掩码
| |-F1_mask.png     
| |-F2_mask.png     
| |-F3_mask.png     
| |-F4_mask.png
|
+-numpy_rawdata     没有处理过的像素位移结果
| |-f1.npy
| |-f2.npy
| |-f3.npy
| |-f4.npy
|
|-data_vision.MTS   原始视频图像
|-display.ipynb     最终用来展示结果的jupyter文件
|-Ground_Truth.xlsx 提供的一层位移真值
|-length_ration.py  计算像素 位移比例的脚本
|-mask_drawer.py    绘制特征检测掩膜的脚本
|-README.md         
|-result.mat        最终的结果
|-utils.py          各种特征检测和其他的辅助脚本
|-WorkFlow.py       用来计算像素位移的主要脚本
```
## 1. WorkFlow.py
> 这是提取特征的主要脚本，实现了读取视频，调用特征提取算法，根据特征点匹配结果并计算位移平均值最终将结果储存为npy文件的流程

### Class WorkFlow
|方法|__init__(self, video_path)|
|---|---|
|video_path|读取视频的路径|

|方法|__call__(self, img_transform)|
|---|---|
|imgtransform|特征点检测的回调函数，来自utils.py|
|mask_path|特征点检测时使用的掩码的路径|

## 2. mask_drawer.py
> 读取视频的第一帧并显示，然后可以使用鼠标在图像上绘制多边形，绘制的过程中不会显示，按下回车会显示绘制的图形然后按下q键可以退出窗口。之后绘制的掩码会保存在features_mask文件夹中。
### funtion draw_poygondraw_polygon
> 鼠标回调函数，会保存多边形的点

### funtion mask_drawer
| 参数          | 描述        |
|-------------|-----------|
| video_path  | 视频的路径     |
| output-path | 保存掩码文件的路径 |

## 3.utiles.py
> 这里是各种特征检测算法，用于workfolw中。输入绘图图像，特征提取图像，mask。
> 本项目最终使用了ORB算法，提取50个特征点。
> 提取的特征点最终和第100帧进行匹配，选用匹配最好的前10个点计算位移的平均值。

### funtion orb
#### input

| 参数   | 描述                          |
|------|-----------------------------|
| img  | 绘图的图像，最终得到的特征点会绘制在这张图上并显示   |
| pic  | 提取特征的图像，默认和img相同，也可以是强化后的图像 |
| mask | 掩膜，二值图像，只会在非0区域进行特征检测       |
#### return
|参数| 描述                                           |
|---|----------------------------------------------|
|img| 已经绘制了特征点的图像                                  |
|kp| 一个元组，元组内元素为cv.keypoint，详细请阅读[cv::KeyPoint](https://docs.opencv.org/5.x/d2/d29/classcv_1_1KeyPoint.html)|
|des| 一个元组，元组内为kp中下标相同点的对应描述符，详细请阅读[cv::BOWTrainer](https://docs.opencv.org/5.x/d5/d14/classcv_1_1BOWTrainer.html#a2a447f969feed258bd3cdfc521bc9502)|                

### match_movingCaculate
#### input 
| 参数      | 描述            |
|---------|---------------|
| kp1,kp2 | 两张图像中提取的特征点   |
| des1,des2 | kp1,kp2对应的描述符 |

#### return
|参数|描述|
|---|---|
|最终的位移结果|

# 4. lenth_ratio.py
> 通过在屏幕上点击得到像素到位移的比例关系。

# 5. display.ipynb
> 文件中有详细的描述
> 1. 读取groundtruth并下采样到和视频帧率一样
> 2. 和f1叠合绘制，调整f1的取样访问和GT对准
> 3. 把f1，f2，f3，f4都换算成位移，最后输出成一个result.mat

