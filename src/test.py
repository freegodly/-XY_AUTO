# -*- coding: utf-8 -*- 

import cv2
import numpy as np
from matplotlib import pyplot as plt


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


def find_obj():     
    img1 = cv2.imread('title.png',0)          # queryImage
    img2 = cv2.imread('xy0030.jpg',0) # trainImage


    #detector = cv2.ORB(400)#400
    detector = cv2.SIFT()

    FLANN_INDEX_LSH    = 6
    flann_params= dict(algorithm = FLANN_INDEX_LSH,
                       table_number = 6, # 12
                       key_size = 12,     # 20
                       multi_probe_level = 1) #2
    #matcher = cv2.FlannBasedMatcher(flann_params, {}) 
    matcher = cv2.BFMatcher()


    kp1, des1 = detector.detectAndCompute(img1,None)
    kp2, des2 = detector.detectAndCompute(img2,None)


    raw_matches = matcher.knnMatch(des1, trainDescriptors = des2, k = 2) #2


    h1, w1 = img2.shape[:2]
    vis = np.zeros((h1, w1), np.uint8)
    vis = img2
    vis = cv2.cvtColor(vis, cv2.COLOR_GRAY2BGR)


    p1, p2, kp_pairs = filter_matches(kp1, kp2, raw_matches,0.70)

    x1,y1,x2,y2 = find_rect(p2,img2)

    color = (0, 255, 0)
    cv2.rectangle(vis, (x1, y1), (x2, y2), color, 2)

    #return vis
    plt.imshow(vis)
    plt.show()

def find_contours():
    img = cv2.imread('xy0030.jpg',0)
    #img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    h, w = img.shape[:2]

    contours0, hierarchy = cv2.findContours( img.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = [cv2.approxPolyDP(cnt, 3, True) for cnt in contours0]

    vis = np.zeros((h, w, 3), np.uint8)
    levels = 3
    cv2.drawContours( vis, contours, (-1, 3)[levels <= 0], (128,255,255),
            3, cv2.CV_AA, hierarchy, abs(levels) )
    cv2.imshow('contours', vis)

import win32gui
from PIL import ImageGrab
import win32con
import pythoncom, pyHook
def get_window(classname):
    hwnd = win32gui.FindWindow(classname, None)
    win32gui.ShowWindow(hwnd, win32con.SW_RESTORE) 
    #win32gui.SetForegroundWindow(hwnd)
    return hwnd

def get_window_image(hwnd):
    game_rect = win32gui.GetWindowRect(hwnd)
    src_image = ImageGrab.grab(game_rect)
    #src_image.show()
    open_cv_image = np.array(src_image)
    open_cv_image = cv2.cvtColor(open_cv_image, cv2.cv.CV_BGR2RGB)
    #plt.imshow(open_cv_image)
    #plt.show()
    return open_cv_image

def KeyStroke(event): 
    if str(event.Key)=='F12':
        exit()
   
    return True     

def find_title(img2):
    img1 = cv2.imread('wq.png',0)          # queryImage
    
    detector = cv2.ORB(400)#400
    #detector = cv2.SIFT()

    FLANN_INDEX_LSH    = 6
    flann_params= dict(algorithm = FLANN_INDEX_LSH,
                       table_number = 6, # 12
                       key_size = 12,     # 20
                       multi_probe_level = 1) #2
    matcher = cv2.FlannBasedMatcher(flann_params, {}) 

    kp1, des1 = detector.detectAndCompute(img1,None)
    kp2, des2 = detector.detectAndCompute(img2,None)
    raw_matches = matcher.knnMatch(des1, trainDescriptors = des2, k = 2) #2


    h1, w1 = img2.shape[:2]
    vis = np.zeros((h1, w1), np.uint8)
    vis = img2
    #vis = cv2.cvtColor(vis, cv2.COLOR_GRAY2BGR)

    p1, p2, kp_pairs = filter_matches(kp1, kp2, raw_matches,0.9)

    x1,y1,x2,y2 = find_rect(p2,img2)

    color = (0, 255, 0)
    cv2.rectangle(vis, (x1, y1), (x2, y2), color, 2)
    return vis

if __name__ == '__main__':

    hm = pyHook.HookManager()
    hm.KeyDown = KeyStroke
    hm.HookKeyboard()

    hwnd = get_window("WSGAME")
    while(True):
        open_cv_image = get_window_image(hwnd)
        show_img = find_title(open_cv_image)
        cv2.imshow('frame',show_img)
        pythoncom.PumpWaitingMessages()

    cv2.destroyAllWindows()