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

def comparehits_bin_min(image_bin,featureimage_bin,max_sum=10,startx = 0 ,endx = 0,move_px = 1):
    """
    查找特征图像出现的位置
    要求传入二值化图像
    返回 出现位置的起始位置 和 差异
    """
    find_list = []

    h, w = image_bin.shape[:2]
    h_f, w_f = featureimage_bin.shape[:2]

    bc_min = max_sum
    start_px = -1

    if endx==0 : endx = w
    for i in xrange(int(endx-startx-w_f)/move_px):
        start_px = i*move_px+startx
        rc = (start_px, 0, w_f, h_f)
        simg_bin = image_bin[rc[1]:rc[1]+rc[3],rc[0]:rc[0]+rc[2]]

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
            simg_bin = image_bin[rc[1]:rc[1]+rc[3],rc[0]:rc[0]+rc[2]]
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
            simg_bin = trainImage[rc[1]:rc[1]+rc[3],rc[0]:rc[0]+rc[2],:]
            simg_b, simg_g, simg_r = cv2.split(simg_bin)
            simg_b_hist = cv2.calcHist([simg_b], [0], None, [bins],[0,256])
            simg_b_hist = cv2.normalize(simg_b_hist).flatten()
            simg_g_hist = cv2.calcHist([simg_g], [0], None, [bins],[0,256])
            simg_g_hist = cv2.normalize(simg_g_hist).flatten()
            simg_r_hist = cv2.calcHist([simg_r], [0], None, [bins],[0,256])
            simg_r_hist = cv2.normalize(simg_r_hist).flatten()

            #cv2.compareHist
            #CV_CONTOURS_MATCH_I1, CV_CONTOURS_MATCH_I2, CV_CONTOURS_MATCH_I3
            # inter = 0.33*cv2.compareHist(queryImage_b_hist,simg_b_hist,cv2.cv.CV_CONTOURS_MATCH_I1) + 0.33*cv2.compareHist(queryImage_g_hist,simg_g_hist,cv2.cv.CV_CONTOURS_MATCH_I1 )+0.33*cv2.compareHist(queryImage_r_hist,simg_r_hist,cv2.cv.CV_CONTOURS_MATCH_I1 )
            inter = 0.5 *calc_chimerge(queryImage_b_hist, simg_b_hist)+0.5 *calc_chimerge(queryImage_g_hist, simg_g_hist)+0.5 *calc_chimerge(queryImage_r_hist, simg_r_hist)
            if( inter < bc_min):
                find_list.append([(start_px,start_py),inter])
    find_list.sort(cmp = lambda x ,y : cmp(x[1],y[1]))
    return find_list



def find_obj_hist_mask(trainImage,queryImage,max_sum=255, bins = 30,startx = 0 ,endx = 0,starty = 0 ,endy = 0,move_px = 1,move_py = 1,mask = None):
    find_list = []
    h, w = trainImage.shape[:2]
    h_f, w_f = queryImage.shape[:2]

    queryImage_b, queryImage_g, queryImage_r = cv2.split(queryImage)
    queryImage_b_hist = cv2.calcHist([queryImage_b], [0], mask, [bins],[0,256])
    queryImage_b_hist = cv2.normalize(queryImage_b_hist).flatten()
    queryImage_g_hist = cv2.calcHist([queryImage_g], [0], mask, [bins],[0,256])
    queryImage_g_hist = cv2.normalize(queryImage_g_hist).flatten()
    queryImage_r_hist = cv2.calcHist([queryImage_r], [0], mask, [bins],[0,256])
    queryImage_r_hist = cv2.normalize(queryImage_r_hist).flatten()

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

            simg_bin = trainImage[rc[1]:rc[1]+rc[3],rc[0]:rc[0]+rc[2],:]
            simg_b, simg_g, simg_r = cv2.split(simg_bin)
            simg_b_hist = cv2.calcHist([simg_b], [0], mask, [bins],[0,256])
            simg_b_hist = cv2.normalize(simg_b_hist).flatten()
            simg_g_hist = cv2.calcHist([simg_g], [0], mask, [bins],[0,256])
            simg_g_hist = cv2.normalize(simg_g_hist).flatten()
            simg_r_hist = cv2.calcHist([simg_r], [0], mask, [bins],[0,256])
            simg_r_hist = cv2.normalize(simg_r_hist).flatten()

            #CV_COMP_BHATTACHARYYA   CV_COMP_CHISQR  CV_COMP_INTERSECT
            inter = 0.33*cv2.compareHist(queryImage_b_hist,simg_b_hist,cv2.cv.CV_COMP_CHISQR) + 0.33*cv2.compareHist(queryImage_g_hist,simg_g_hist,cv2.cv.CV_COMP_CHISQR )+0.33*cv2.compareHist(queryImage_r_hist,simg_r_hist,cv2.cv.CV_COMP_CHISQR )

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


def find_obj_rect(image,minLineLength = 10,extend_length = 10,color_min = 200,color_max = 255):
    """
    查找图像中最大的矩形
    """
    result_rect = None

    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #cv2.imwrite("img_gray.png",img_gray)

    _,img_bin = cv2.threshold(img_gray, color_min,color_max, cv2.THRESH_BINARY)

    #cv2.imshow("img_bin",img_bin)

    maxLineGap = 15
    lines = cv2.HoughLinesP(img_bin,1,np.pi/2,minLineLength,0,maxLineGap)

    if len(lines[0]) < 4 :
        print "len_lines:",len(lines[0])
        return result_rect

    find_lines = []
    for x1,y1,x2,y2 in lines[0]:
        #垂直的
        if x1==x2:
            find_lines.append((x1,y1+extend_length,x2,y2-extend_length))
        #水平的
        if y1==y2:
            find_lines.append((x1-extend_length,y1,x2+extend_length,y2))

    rect_img = np.zeros(image.shape, np.uint8)
    for x1,y1,x2,y2 in find_lines:
        cv2.line(rect_img,(x1,y1),(x2,y2),(0,255,0),3)

    rect_img_gray =  cv2.cvtColor(rect_img, cv2.COLOR_BGR2GRAY)
    _,rect_img_bin = cv2.threshold(rect_img_gray, 100,255, cv2.THRESH_BINARY)

    #cv2.imshow("rect_img_bin",rect_img_bin)


    (cnts, _) = cv2.findContours(rect_img_bin.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]

    rect = cv2.minAreaRect(c)

    box = np.int0(cv2.cv.BoxPoints(rect))
    # cv2.drawContours(image, [box], -1, (0, 255, 0), 2)
    # cv2.imshow("img",image)

    x_s = []
    y_s = []
    for b in box:
        x_s.append(b[0])
        y_s.append(b[1])

    result_rect=[min(x_s),min(y_s),max(x_s)-min(x_s),max(y_s)-min(y_s)]

    return result_rect



def get_image_sub(image,rect,channels = 3):

    #判断是否出接
    h, w = image.shape[:2]


    if rect[0] < 0 :
        rect[0] = 0
    if rect[1] < 0 :
        rect[1] = 0
    if rect[0]+rect[2] > w:
        rect[2] = w - rect[0]
    if rect[1]+rect[3] > h:
        rect[3] = h - rect[1]


    rc = (rect[0], rect[1], rect[2], rect[3])
    sub_image = image[rc[1]:rc[1]+rc[3],rc[0]:rc[0]+rc[2],:]
    sub_image = sub_image
    return sub_image

def get_window_hwnd(classname):
    hwnd = win32gui.FindWindow(classname, None)
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    win32gui.SetForegroundWindow(hwnd)
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






def find_contours(img):
    """
    cv2.RETR_EXTERNAL 表示只检测外轮廓
    cv2.RETR_LIST 检测的轮廓不建立等级关系
    cv2.RETR_CCOMP 建立两个等级的轮廓，上面的一层为外边界，里面的一层为内孔的边界信息。如果内孔内还有一个连通物体，这个物体的边界也在顶层。
    cv2.RETR_TREE 建立一个等级树结构的轮廓。

    第三个参数method为轮廓的近似办法
    cv2.CHAIN_APPROX_NONE 存储所有的轮廓点，相邻的两个点的像素位置差不超过1，即max（abs（x1-x2），abs（y2-y1））==1
    cv2.CHAIN_APPROX_SIMPLE 压缩水平方向，垂直方向，对角线方向的元素，只保留该方向的终点坐标，例如一个矩形轮廓只需4个点来保存轮廓信息
    cv2.CHAIN_APPROX_TC89_L1 ， CV_CHAIN_APPROX_TC89_KCOS 使用teh-Chinl chain 近似算法
    """
    img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #常量定义椭圆 MORPH_ELLIPSE 和十字形结构 MORPH_CROSS  定义矩形 MORPH_RECT
    #kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (10, 10))
    #opened = cv2.morphologyEx(img_gray, cv2.MORPH_OPEN, kernel)
    #img_gray = cv2.dilate(img_gray, None, iterations = 5)
    #img_gray = cv2.erode(img_gray, None, iterations = 2)


    #_,img_bin = cv2.threshold(img_gray, 0,100, cv2.THRESH_BINARY_INV)


    # kernel  = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    # dilate  = cv2.dilate(img_gray, kernel, iterations = 1)
    # erode   = cv2.erode(img_gray, kernel, iterations = 1)
    # result = cv2.absdiff(dilate,erode);
    _,img_bin = cv2.threshold(img_gray, 200,255, cv2.THRESH_BINARY)
    minLineLength = 200
    maxLineGap = 15
    lines = cv2.HoughLinesP(img_bin,1,np.pi/4,200,minLineLength,maxLineGap)
    for x1,y1,x2,y2 in lines[0]:
        cv2.line(img,(x1,y1),(x2,y2),(0,255,0),2)

    cv2.imshow("img_bin",img_bin)
    cv2.imshow("result",img)

    # gradX = cv2.Sobel(img_bin, ddepth = cv2.cv.CV_32F, dx = 1, dy = 0, ksize = 3)
    # gradY = cv2.Sobel(img_bin, ddepth = cv2.cv.CV_32F, dx = 0, dy = 1, ksize = 3)

    # gradient = cv2.subtract(gradX, gradY)
    # gradient = cv2.convertScaleAbs(gradient)

    # blurred = cv2.blur(img_bin, (10, 10))
    # (_, thresh) = cv2.threshold(blurred, 100, 255, cv2.THRESH_BINARY)



    # kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (5, 5))
    # closed = cv2.morphologyEx(img_bin, cv2.MORPH_CLOSE, kernel)


    #
    #closed = cv2.dilate(img_bin, None, iterations = 10)
    #closed = cv2.erode(img_bin, None, iterations = 1)

    # _,img_bin = cv2.threshold(closed, 0,80, cv2.THRESH_BINARY_INV)

    # cv2.imshow("img_bin",img_bin)

    # (cnts, _) = cv2.findContours(img_bin.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

    # c = sorted(cnts, key = cv2.contourArea, reverse = True)[0]

    # rect = cv2.minAreaRect(c)

    # box = np.int0(cv2.cv.BoxPoints(rect))

    # cv2.drawContours(img, [box], -1, (0, 255, 0), 3)

    # cv2.imshow("img",img)
    return img



def pil_to_cv2(image):
    open_cv_image = np.array(image)
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
