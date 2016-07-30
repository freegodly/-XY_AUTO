# -*- coding: utf-8 -*- 

import cv2
from cv2 import cv 
import numpy as np
from matplotlib import pyplot as plt



def comparehits_bin_min(image_bin,featureimage_bin,max_sum=255,startx = 0 ,endx = 0,move_px = 1):
    """
    查找特征图像出现的位置
    要求传入二值化图像
    返回 出现位置的起始位置 和 差异
    """
    find_list = []

    h, w = image_bin.shape[:2]
    h_f, w_f = featureimage_bin.shape[:2]

    # featureimage_gray = cv2.cvtColor(featureimage,cv2.COLOR_BGR2GRAY) 
    # ret , featureimage_bin = cv2.threshold(featureimage_gray, 200,255, cv2.THRESH_BINARY)

    # image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) 
    # ret , image_bin = cv2.threshold(image_gray, 200,255, cv2.THRESH_BINARY)

    image1M = cv.fromarray(image_bin)
    image1Ip = cv.GetImage(image1M)
    bc_min = max_sum
    start_px = -1 

    if endx==0 : endx = w
    for i in xrange(int(endx-startx-w_f)/move_px):
        start_px = i*move_px+startx
        rc = (start_px, 0, w_f, h_f)
        cv.SetImageROI(image1Ip,rc)  
        imageCopy = cv.CreateImage((rc[2], rc[3]),cv2.IPL_DEPTH_8U,1)  
        cv.Copy(image1Ip,imageCopy)  
        cv.ResetImageROI(image1Ip) 
        simg_bin = np.asarray(cv.GetMat(imageCopy))
       
        inter = sum(sum(abs(featureimage_bin - simg_bin)))
        if( inter < bc_min):
            find_list.append([start_px,inter])
    find_list.sort(cmp = lambda x ,y : cmp(x[1],y[1]))
    return find_list



def img_gray_and_bin(image,min_color = 200,max_color = 255):
    """
    将图像二值化
    """
    image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) 
    ret , image_bin = cv2.threshold(image_gray, min_color,max_color, cv2.THRESH_BINARY)
    return image_bin



def read_feature_file(filename):
    """
    读取特征描述文件
    """
    feature_info = []

    file_object = open(filename,'r')
    try:
        for line in file_object:
            line = line.strip('\n')
            sl = line.split(" ")
            feature_info.append((sl[0],sl[1]))
    finally:
        file_object.close()

    return feature_info