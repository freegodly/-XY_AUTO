# -*- coding: utf-8 -*-

import cv2
from cv2 import cv
import numpy as np
from matplotlib import pyplot as plt
from Tools import *
import win32gui
from PIL import ImageGrab
from PIL import Image
import win32con,win32api
import pythoncom, pyHook
import time
from DD import DD



def KeyStroke(event):
    if str(event.Key)=='F12':
        exit()
    return True



def image_despose(image):
    start=clock()
    #识别坐标
    mapname,hero_location_info = get_coordinates(image)
    print mapname
    print "hero_location_info:",hero_location_info

    ################### 查找光标位置
    image_mouse = cv2.imread("feature/other/mouse.png")
    image_mouse_mask = cv2.imread("feature/other/mouse_mask.png",0)
    find_list = find_obj_hist_mask(image,image_mouse,mask=image_mouse_mask,max_sum=2.5,move_px = 5,move_py = 5)
    if len(find_list) > 0:
        #print find_list[0]
        start_point = find_list[0][0]
        cv2.rectangle(image, (start_point[0], start_point[1]), (start_point[0]+10, start_point[1]+10), (0, 0, 255), 4)

        ##查找小地图区域范围
        rect_location = [ find_list[0][0][0] - 34 , find_list[0][0][1] - 26-5 ,68,26]
        #cv2.rectangle(image, (rect_location[0], rect_location[1]), (rect_location[0]+rect_location[2], rect_location[1]+rect_location[3]), (0, 255, 0), 2)
        image_sub = get_image_sub(image,rect_location)
        minimap_location = get_minimap_location(image_sub)
        print "minimap_location:",minimap_location
    print "find_obj_hist:",(clock()-start)
    return image



def find_point(image):
    mach_list = []
    match_info = []

    feature_names = read_feature_file("feature/coordinates/names.txt")
    feature_numbers = read_feature_file("feature/coordinates/numbers.txt")


    image_bin = img_gray_and_bin(image,200,255)
    #cv2.imwrite("image_bin.png",image_bin)

    #先查找数字和汉字的分隔符
    img_left = cv2.imread("feature/coordinates/left.png")
    img_left_bin = img_gray_and_bin(img_left,200,255)
    find_list = comparehits_bin_min(image_bin,img_left_bin,255)
    if len(find_list) < 1 : return match_info
    left_x = find_list[0][0]

    img_right = cv2.imread("feature/coordinates/right.png")
    img_right_bin = img_gray_and_bin(img_right,200,255)
    find_list = comparehits_bin_min(image_bin,img_right_bin,255)
    right_x = find_list[0][0]
    if len(find_list) < 1 : return match_info

    #print "left:",left_x," right:",right_x

    #匹配地图名字
    for i in xrange(len(feature_names)):
        feature_img = cv2.imread("feature/coordinates/"+feature_names[i][0])
        feature_img_bin = img_gray_and_bin(feature_img,200,255)
        find_list = comparehits_bin_min(image_bin,feature_img_bin,2,0,left_x)
        for m in find_list:
           mach_list.append((m[0],feature_names[i][1]))
           #print m[0],":",feature_names[i][1].decode('utf-8')," bc_min:",m[1]

    mach_list.sort(cmp = lambda x ,y : cmp(x[0],y[0]))
    for m in mach_list:
       match_info.append(m[1])

    #匹配坐标
    mach_list =[]
    for i in xrange(len(feature_numbers)):
        feature_img = cv2.imread("feature/coordinates/"+feature_numbers[i][0])
        feature_img_bin = img_gray_and_bin(feature_img,200,255)
        find_list = comparehits_bin_min(image_bin,feature_img_bin,1,left_x,0)
        for m in find_list:
           mach_list.append((m[0],feature_numbers[i][1]))
           #print m[0],":",feature_numbers[i][1].decode('utf-8')," bc_min:",m[1]

    mach_list.sort(cmp = lambda x ,y : cmp(x[0],y[0]))
    for m in mach_list:
       match_info.append(m[1])

    return match_info

def split_point(title_image):
    #get_screen_sub_pilimage()
    #pil_to_cv2
    #title_image = get_screen_sub_pilimage(20, 20,110,18)
    #title_image = Image.open('point.jpg')
    cv_title_image = pil_to_cv2(title_image)
    cv_title_image_bin = img_gray_and_bin(cv_title_image,200,255)

    h, w = cv_title_image.shape[:2]

    img_left = cv2.imread("feature/coordinates/left.png")
    img_left_bin = img_gray_and_bin(img_left,200,255)
    find_list = comparehits_bin_min(cv_title_image_bin,img_left_bin)
    left_x = find_list[0][0]
    img_right = cv2.imread("feature/coordinates/right.png")
    img_right_bin = img_gray_and_bin(img_right,200,255)
    find_list = comparehits_bin_min(cv_title_image_bin,img_right_bin)
    right_x = find_list[0][0]

    print "left:",left_x," right:",right_x

    #切割汉字11个像素 H=12
    endx = left_x - 1
    while endx > 12:
        bounds = (endx-11,0,endx,h)
        sub_img = title_image.crop(bounds)
        sub_img.save("point/"+str(endx)+".png")
        print endx
        endx = endx -11 -1

    #切割数字5个像素
    endx = right_x - 1
    while endx-left_x > 6:
        bounds = (endx-5,0,endx,h)
        sub_img = title_image.crop(bounds)
        sub_img.save("point/s_"+str(endx)+".png")
        print endx
        endx = endx -5 -1

def get_coordinates(image):
    mapname = u"未知"
    hero_location = [-1,-1]
    img = get_image_sub(image,(20, 24,110,12))
    #cv2.imwrite("img.png",img)
    mach_list = find_point(img)
    info = ""
    for m in mach_list:
        info+=m
    hero_location_info = info.decode('utf-8')
    try:
        h = hero_location_info.split('[')
        mapname = h[0]
        h = h[1].split(']')
        h = h[0].split(',')
        hero_location[0] = int(h[0])
        hero_location[1] = int(h[1])
    except Exception,e:
        pass
    return (mapname,hero_location)


def get_minimap_location(image):

    minimap_location = [-1,-1]

    mach_list = []
    match_info = []
    feature_numbers = read_feature_file("feature/minimaplocation/numbers.txt")
    image_bin = img_gray_and_bin(image,200,255)
    #cv2.imwrite("image_bin.png",image_bin)
    #匹配坐标
    for i in xrange(len(feature_numbers)):
        feature_img = cv2.imread("feature/minimaplocation/"+feature_numbers[i][0])
        feature_img_bin = img_gray_and_bin(feature_img,200,255)
        find_list = comparehits_bin_min_x(image_bin,feature_img_bin,0.1,move_px=1)
        for m in find_list:
           mach_list.append((m[0],feature_numbers[i][1]))

    mach_list.sort(cmp = lambda x ,y : cmp(x[0],y[0]))
    for m in mach_list:
       match_info.append(m[1])


    info = ""
    for m in match_info:
        info+=m
    if len(info)>0:
        try:
            x = info.split(",")
            minimap_location = [int(x[0]),int(x[-1])]
        except Exception,e:
            pass
    return minimap_location


def test():
    t = clock()
    print "RunTime:",clock()-t
    cv2.waitKey()
    exit()

if __name__ == '__main__':
    hm = pyHook.HookManager()
    hm.KeyDown = KeyStroke
    hm.HookKeyboard()

    hwnd = get_window_hwnd("WSGAME")

    #test()
    while(True):
        open_cv_image = get_window_rect_image(hwnd)
        open_cv_image = image_despose(open_cv_image)
        cv2.imshow('frame',open_cv_image)
        pythoncom.PumpWaitingMessages()

    cv2.destroyAllWindows()
