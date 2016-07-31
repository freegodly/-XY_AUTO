# -*- coding: utf-8 -*-

import win32gui
from PIL import ImageGrab
from PIL import Image
import win32con
import cv2
from cv2 import cv
import numpy as np
from matplotlib import pyplot as plt
from time import clock
import threading
from MyThread import *

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




def comparehits_bin_min_x(image_bin,featureimage_bin,max_sum=255,startx = 0 ,endx = 0,starty = 0 ,endy = 0,move_px = 1,move_py = 1):
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
    start_py = -1
    if endx==0 : endx = w
    if endy==0 : endy = h
    for j in xrange(int(endy-starty-h_f)/move_py):
        start_py = j*move_py+starty
        for i in xrange(int(endx-startx-w_f)/move_px):
            start_px = i*move_px+startx
            rc = (start_px, start_py, w_f, h_f)
            cv.SetImageROI(image1Ip,rc)
            imageCopy = cv.CreateImage((rc[2], rc[3]),cv2.IPL_DEPTH_8U,1)
            cv.Copy(image1Ip,imageCopy)
            cv.ResetImageROI(image1Ip)
            simg_bin = np.asarray(cv.GetMat(imageCopy))

            inter = sum(sum(abs(featureimage_bin - simg_bin)))
            #print "X:",start_px," Y:",start_py," M:",inter
            if( inter < bc_min):
                find_list.append([(start_px,start_py),inter])
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


def togray(src,des):
    image = cv2.imread(src)          # queryImage
    h, w = image.shape[:2]
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    cv2.imwrite(des, gray)

def find_obj(trainImage,queryImage,ratio=0.75,is2bin = False , bin_min = 170, bin_max=255 ,trees = 5 , checks = 50):
    """
    查找目标图像出现的位置
    返回RECT
    """
    # img1 = cv2.cvtColor(queryImage,cv2.COLOR_BGR2GRAY)  # queryImage
    # img2 = cv2.cvtColor(trainImage,cv2.COLOR_BGR2GRAY)  # trainImage
    # if is2bin :
    #     ret, img1 = cv2.threshold(img1,bin_min,bin_max,cv2.THRESH_BINARY) #将灰度图像转成二值图像
    #     ret, img2 = cv2.threshold(img2,bin_min,bin_max,cv2.THRESH_BINARY) #将灰度图像转成二值图像
    # #cv2.imwrite("img1.png",img1)
    # #cv2.imwrite("img2.png",img2)

    detector = cv2.SIFT()
    #detector = cv2.ORB(400)#400

    kp1, des1 = detector.detectAndCompute(queryImage,None)
    kp2, des2 = detector.detectAndCompute(trainImage,None)
    #print len(kp1)

    # img1_k = cv2.drawKeypoints(img1,kp1,color=(0,255,0), flags=0)
    # plt.imshow(img1_k)
    # plt.show()

    # img2_k = cv2.drawKeypoints(img2,kp2,color=(0,255,0), flags=0)
    # plt.imshow(img2_k)
    # plt.show()

    ## 1
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = trees)
    search_params = dict(checks=checks)   # or pass empty dictionary
    flann = cv2.FlannBasedMatcher(index_params,search_params)
    raw_matches = flann.knnMatch(des1,des2,k=2)


    ## 2
    # FLANN_INDEX_LSH    = 6
    # flann_params= dict(algorithm = FLANN_INDEX_LSH,
    #                table_number = 6, # 12
    #                key_size = 12,     # 20
    #                multi_probe_level = 1) #2
    # matcher = cv2.FlannBasedMatcher(flann_params, {})
    # raw_matches = matcher.knnMatch(des1, trainDescriptors = des2, k = 2) #2


    #print "raw_matches:",len(raw_matches)

    p1, p2, kp_pairs = filter_matches(kp1, kp2, raw_matches,ratio)

    x1,y1,x2,y2 = find_rect(p2,trainImage)

    ## show rect
    # h1, w1 = img2.shape[:2]
    # vis = np.zeros((h1, w1), np.uint8)
    # vis = img2
    # vis = cv2.cvtColor(vis, cv2.COLOR_GRAY2BGR)
    # color = (0, 255, 0)
    # cv2.rectangle(vis, (x1, y1), (x2, y2), color, 2)
    # plt.imshow(vis)
    # plt.show()

    return (x1,y1,x2,y2)


def find_obj_hist(trainImage,queryImage,max_sum=255, bins = 30,startx = 0 ,endx = 0,starty = 0 ,endy = 0,move_px = 1,move_py = 1):
    find_list = []
    h, w = trainImage.shape[:2]
    h_f, w_f = queryImage.shape[:2]
    queryImage_b, queryImage_g, queryImage_r = cv2.split(queryImage)
    queryImage_b_hist = cv2.calcHist([queryImage_b], [0], None, [bins],[0,256])
    queryImage_b_hist = cv2.normalize(queryImage_b_hist).flatten()
    queryImage_g_hist = cv2.calcHist([queryImage_g], [0], None, [bins],[0,256])
    queryImage_g_hist = cv2.normalize(queryImage_g_hist).flatten()
    queryImage_r_hist = cv2.calcHist([queryImage_r], [0], None, [bins],[0,256])
    queryImage_r_hist = cv2.normalize(queryImage_r_hist).flatten()
    image1M = cv.fromarray(trainImage)
    image1Ip = cv.GetImage(image1M)
    bc_min = max_sum
    start_px = -1
    start_py = -1
    if endx==0 : endx = w
    if endy==0 : endy = h
    for j in xrange(int(endy-starty-h_f)/move_py):
        start_py = j*move_py+starty
        for i in xrange(int(endx-startx-w_f)/move_px):
            start_px = i*move_px+startx
            rc = (start_px, start_py, w_f, h_f)
            cv.SetImageROI(image1Ip,rc)
            imageCopy = cv.CreateImage((rc[2], rc[3]),cv2.IPL_DEPTH_8U,3)
            cv.Copy(image1Ip,imageCopy)
            cv.ResetImageROI(image1Ip)
            simg_bin = np.asarray(cv.GetMat(imageCopy))
            simg_b, simg_g, simg_r = cv2.split(simg_bin)
            simg_b_hist = cv2.calcHist([simg_b], [0], None, [bins],[0,256])
            simg_b_hist = cv2.normalize(simg_b_hist).flatten()
            simg_g_hist = cv2.calcHist([simg_g], [0], None, [bins],[0,256])
            simg_g_hist = cv2.normalize(simg_g_hist).flatten()
            simg_r_hist = cv2.calcHist([simg_r], [0], None, [bins],[0,256])
            simg_r_hist = cv2.normalize(simg_r_hist).flatten()
            inter = 0.5 *calc_chimerge(queryImage_b_hist, simg_b_hist)+0.5 *calc_chimerge(queryImage_g_hist, simg_g_hist)+0.5 *calc_chimerge(queryImage_r_hist, simg_r_hist)
            if( inter < bc_min):
                find_list.append([(start_px,start_py),inter])
    find_list.sort(cmp = lambda x ,y : cmp(x[1],y[1]))
    return find_list

def find_obj_hist_multithreading(trainImage,queryImage,max_sum=255, bins = 30,startx = 0 ,endx = 0,starty = 0 ,endy = 0,move_px = 1,move_py = 1,theardnum=10):
    mt = MyThread()
    g_func_list = []


    h, w = trainImage.shape[:2]
    h_f, w_f = queryImage.shape[:2]
    subw = int(w/theardnum)
    for i in xrange(theardnum):
        sub_startx = i*subw
        sub_endx = i*subw+subw
        # if i>0:
        #     sub_startx = sub_startx-w_f
        #     sub_endx = sub_endx-w_f
        if sub_endx>w : sub_endx = w

        g_func_list.append({"func":find_obj_hist,"args":(trainImage,queryImage,max_sum, bins,sub_startx ,sub_endx,starty ,endy ,move_px,move_py)})

    mt.set_thread_func_list(g_func_list)
    mt.start()

    find_list = []
    for l in mt.ret_value():
        find_list.extend(l)

    find_list.sort(cmp = lambda x ,y : cmp(x[1],y[1]))

    return find_list



def get_window_hwnd(classname):
    hwnd = win32gui.FindWindow(classname, None)
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    #win32gui.SetForegroundWindow(hwnd)
    return hwnd

def get_window_rect_image(hwnd):
    game_rect = win32gui.GetWindowRect(hwnd)
    client_rect = win32gui.GetClientRect(hwnd)
    title_h =  game_rect[3] - game_rect[1] - client_rect[3]
    game_rect = (game_rect[0],game_rect[1]+title_h,game_rect[2],game_rect[3])
    src_image = ImageGrab.grab(game_rect)
    open_cv_image = np.array(src_image)
    open_cv_image = cv2.cvtColor(open_cv_image, cv2.cv.CV_BGR2RGB)
    return open_cv_image

#############    local   ##############


def calc_chimerge(a,b):
    a = a
    c = b-a
    c = c*c
    d = c / (a + b +1e-10)
    return (sum(d))

def filter_matches(kp1, kp2, matches, ratio = 0.75):
    mkp1, mkp2 = [], []
    for m in matches:
        if len(m) == 2 and m[0].distance < m[1].distance * ratio:
            m = m[0]
            mkp1.append( kp1[m.queryIdx] )
            mkp2.append( kp2[m.trainIdx] )
    p1 = np.float32([kp.pt for kp in mkp1])
    p2 = np.float32([kp.pt for kp in mkp2])
    kp_pairs = zip(mkp1, mkp2)
    return p1, p2, kp_pairs

def find_rect(p2,img2):
    shape = img2.shape
    x1 = shape[1]
    y1 = shape[0]
    x2 = 0
    y2 = 0

    for p in p2:
        #print "X = %d,Y = %d" %(p[0],p[1])
        if p[0] < x1 : x1 = int(p[0])
        if p[0] > x2 : x2 = int(p[0])
        if p[1] < y1 : y1 = int(p[1])
        if p[1] > y2 : y2 = int(p[1])
    return x1,y1,x2,y2
