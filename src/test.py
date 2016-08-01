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
from FindImageProcess import *
import time
#from DD import DD

screen_image = None
fi_mouse = FindImage("feature/other/mouse_s.png","WSGAME",max_sum=2,move_px = 10,move_py = 10,prox_num=1,proy_num=1)



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


def get_window(classname):
    hwnd = win32gui.FindWindow(classname, None)
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
    #win32gui.SetForegroundWindow(hwnd)
    return hwnd

def get_window_image(hwnd):
    global screen_image
    game_rect = win32gui.GetWindowRect(hwnd)
    client_rect = win32gui.GetClientRect(hwnd)
    title_h =  game_rect[3] - game_rect[1] - client_rect[3]
    game_rect = (game_rect[0],game_rect[1]+title_h,game_rect[2],game_rect[3])
    src_image = ImageGrab.grab(game_rect)
    screen_image = src_image
    #src_image.show()
    open_cv_image = np.array(src_image)
    open_cv_image = cv2.cvtColor(open_cv_image, cv2.cv.CV_BGR2RGB)
    #plt.imshow(open_cv_image)
    #plt.show()
    return open_cv_image

def get_screen_sub_pilimage(x,y,w,h):
    global screen_image
    bounds = (x,y,x+w,y+h)
    sub_img = screen_image.crop(bounds)
    return sub_img

def pil_to_cv2(image):
    open_cv_image = np.array(image)
    open_cv_image = cv2.cvtColor(open_cv_image, cv2.cv.CV_BGR2RGB)
    return open_cv_image



def KeyStroke(event):
    if str(event.Key)=='F12':
        fi_mouse.stop()
        exit()

    return True



def image_despose(image):
    start=clock()


    #标记坐标图像位置
    color = (0, 255, 0)
    cv2.rectangle(image, (20, 24), (110+20, 12+24), color, 1)
    #识别坐标
    #print_coordinates()

    ################### 查找光标位置
    # mouseinfo = fi_mouse.get_result()
    # if mouseinfo is not None:
    #     #print mouseinfo
    #     start_point = mouseinfo[0]
    #     cv2.rectangle(image, (start_point[0], start_point[1]), (start_point[0]+10, start_point[1]+10), (0, 0, 255), 4)


    ################### 查找光标位置
    image_mouse = cv2.imread("feature/other/mouse.png")
    image_mouse_mask = cv2.imread("feature/other/mouse_mask.png",0)
    find_list = find_obj_hist_mask(image,image_mouse,mask=image_mouse_mask,max_sum=1,move_px = 5,move_py = 5)
    if len(find_list) > 0:
        print find_list[0]
        start_point = find_list[0]
        cv2.rectangle(image, (start_point[0], start_point[1]), (start_point[0]+10, start_point[1]+10), (0, 0, 255), 4)




    print "find_obj_hist:",(clock()-start)


    window_hwnd = get_window_hwnd("WSGAME")
    #screen_pos = win32gui.ClientToScreen(hwnd,start_point)
    screen_pos = win32gui.ClientToScreen(window_hwnd,(100,100))
    win32api.SetCursorPos(screen_pos)
    win32gui.SetForegroundWindow(window_hwnd)

    time.sleep(1)

    DD.DD_btn_click(1)
    DD.DD_str("122345678")
    DD.DD_key_click(313)

    fi_mouse.stop()
    exit()
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

def print_coordinates():
    rol_image = get_screen_sub_pilimage(20, 24,110,12)
    img = pil_to_cv2(rol_image)
    #print img.shape
    mach_list = find_point(img)
    info = ""
    for m in mach_list:
        info+=m
    print info.decode('utf-8')

def test():
    t = clock()

    

    

    ################### 查找光标位置
    # image = cv2.imread("img/xy0008.jpg")
    # image_mouse = cv2.imread("feature/other/mouse.png")
    # image_mouse_mask = cv2.imread("feature/other/mouse_mask.png",0)
    # find_list = find_obj_hist_mask(image,image_mouse,max_sum=1,move_px = 5,move_py = 5,mask=image_mouse_mask)
    # print len(find_list)
    # if len(find_list) > 0:
    #     print find_list[0]



    ########################  查找小地图
    # #image = cv2.imread("img/xy0004.jpg")
    # image = cv2.imread("img/xy0009.jpg")
    # #image = cv2.imread("img/xy0001.jpg")
    # #image = cv2.imread("img/xy0010.jpg")
    # rect = find_obj_rect(image,minLineLength=200,extend_length=10)
    # if rect is not None:
    #     print rect
    #     cv2.rectangle(image, (rect[0], rect[1]), (rect[0]+rect[2], rect[1]+rect[3]), (0, 0, 255), 4)
        
    #     rect = [rect[0]+10,rect[1]+10,rect[2]-20,rect[3]-20]
    #     sub_image = get_image_sub(image,rect)
    #     #cv2.imshow('sub_image',sub_image)
    #     cv2.imwrite('img/sub_image.png',sub_image)

        
    ####################  查找小地图光标位置  
    image = cv2.imread("feature/other/mouse_for_location.png")
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    _,img_bin = cv2.threshold(img_gray, 240,255, cv2.THRESH_BINARY)


    cv2.imshow('frame',image)
    print "RunTime:",clock()-t
    cv2.waitKey()
    exit()

if __name__ == '__main__':
    multiprocessing.freeze_support()
    #fi_mouse.run()
    hm = pyHook.HookManager()
    hm.KeyDown = KeyStroke
    hm.HookKeyboard()

    #hwnd = get_window("RCImageViewerFrame")
    hwnd = get_window("WSGAME")

    test()
    while(True):
        open_cv_image = get_window_image(hwnd)
        #cv2.imshow('frame',open_cv_image)
        img = image_despose(open_cv_image)
        cv2.imshow('frame',img)
        pythoncom.PumpWaitingMessages()

    cv2.destroyAllWindows()
