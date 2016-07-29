# -*- coding: utf-8 -*- 

import cv2
from cv2 import cv 
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
        print "X = %d,Y = %d" %(p[0],p[1])
        if p[0] < x1 : x1 = int(p[0])
        if p[0] > x2 : x2 = int(p[0])
        if p[1] < y1 : y1 = int(p[1])
        if p[1] > y2 : y2 = int(p[1])
    return x1,y1,x2,y2

def togray(src,des):
    image = cv2.imread(src)          # queryImage
    h, w = image.shape[:2]
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) 
    cv2.imwrite(des, gray)

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

def find_contours(img):
    #img = cv2.imread('xy0030.jpg',0)
    #img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    h, w = img.shape[:2]

    contours0, hierarchy = cv2.findContours( img.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours = [cv2.approxPolyDP(cnt, 3, True) for cnt in contours0]

    vis = np.zeros((h, w, 3), np.uint8)
    levels = 3
    cv2.drawContours( vis, contours, (-1, 3)[levels <= 0], (128,255,255),
            3, cv2.CV_AA, hierarchy, abs(levels) )
    #cv2.imshow('contours', vis)
    return vis

import win32gui
from PIL import ImageGrab
from PIL import Image
import win32con
import pythoncom, pyHook


screen_image = None

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
        exit()
   
    return True     

def find_title(img2):
    img1 = cv2.imread('title_f.png',0)          # queryImage
    
    detector = cv2.ORB(800)#400
    #detector = cv2.SIFT()
    FLANN_INDEX_LSH    = 6
    flann_params = dict(algorithm = FLANN_INDEX_LSH,
                       table_number = 15, # 12
                       key_size = 1,     # 20
                       multi_probe_level = 3) #2
    matcher = cv2.FlannBasedMatcher(flann_params, {}) 
    #matcher = cv2.BFMatcher()

    kp1, des1 = detector.detectAndCompute(img1,None)
    kp2, des2 = detector.detectAndCompute(img2,None)
    
    raw_matches = matcher.knnMatch(des1,des2, k = 2) #2
    
    print len(raw_matches)
    h1, w1 = img2.shape[:2]
    vis = np.zeros((h1, w1), np.uint8)
    vis = img2
    #vis = cv2.cvtColor(vis, cv2.COLOR_GRAY2BGR)

    p1, p2, kp_pairs = filter_matches(kp1, kp2, raw_matches,0.99)

    x1,y1,x2,y2 = find_rect(p2,img2)

    color = (0, 255, 0)
    cv2.rectangle(vis, (x1, y1), (x2, y2), color, 2)
    return vis

def get_ROI_image(image,rc):
    image1M = cv.fromarray(image)  
    image1Ip = cv.GetImage(image1M)  
    cv.SetImageROI(image1Ip,rc)  
    imageCopy = cv.CreateImage((rc[2], rc[3]),cv2.IPL_DEPTH_8U, 3)  
    cv.Copy(image1Ip,imageCopy)  
    cv.ResetImageROI(image1Ip)  
    cv2image = np.asarray(cv.GetMat(imageCopy)) 
    return  cv2image

def image_despose(image):
    # 坐标

    rol_image = get_screen_sub_pilimage(20, 20,110,18)
    title_image = pil_to_cv2(rol_image)
    cv2.imwrite("point.jpg", title_image)
    color = (0, 255, 0)
    cv2.rectangle(image, (20, 20), (130, 38), color, 1)

    return image


    image=cv2.imread('point.png')
    image=cv2.resize(image,(800,200),interpolation=cv2.INTER_AREA)
    h, w = image.shape[:2]
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) 

    ret , bin = cv2.threshold(gray, 200,255, cv2.THRESH_BINARY)

    #膨胀后腐蚀  
    dilated = cv2.dilate(bin, cv2.getStructuringElement(cv2.MORPH_RECT,(2, 2)))  
    eroded = cv2.erode(dilated, cv2.getStructuringElement(cv2.MORPH_RECT,(2, 2)))  
    #腐蚀后膨胀  
    eroded = cv2.erode(eroded, cv2.getStructuringElement(cv2.MORPH_RECT,(2, 2)))  
    dilated = cv2.dilate(eroded, cv2.getStructuringElement(cv2.MORPH_RECT,(2, 2)))  
    #细化  
    median = cv2.medianBlur(bin, 3)  
    median1 = cv2.medianBlur(bin, 3)  
    #return bin
    #轮廓查找,查找前必须转换成黑底白字  
    #contours, heirs  = cv2.findContours(median1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE) 
   
    return  bin


    

    i = 0  
    pic = []  
    dictPic = {}  
    for tours in contours:   
        rc = cv2.boundingRect(tours)  
        #rc[0] 表示图像左上角的纵坐标，rc[1] 表示图像左上角的横坐标，rc[2] 表示图像的宽度，rc[3] 表示图像的高度，  
        #cv2.rectangle(bin, (rc[0],rc[1]),(rc[0]+rc[2],rc[1]+rc[3]),(255,0,255))  
        image1M = cv.fromarray(median)  
        image1Ip = cv.GetImage(image1M)  
        cv.SetImageROI(image1Ip,rc)  
        imageCopy = cv.CreateImage((rc[2], rc[3]),cv2.IPL_DEPTH_8U, 1)  
        cv.Copy(image1Ip,imageCopy)  
        cv.ResetImageROI(image1Ip)  
        #print np.asarray(cv.GetMat(imageCopy))  
        #把图像左上角的纵坐标和图像的数组元素放到字典里  
        dictPic[rc[0]] = np.asarray(cv.GetMat(imageCopy))  
        pic.append(np.asarray(cv.GetMat(imageCopy)))  
        #cv.ShowImage(str(i), imageCopy)  
        #cv.Not(imageCopy, imageCopy)    #函数cvNot(const CvArr* src,CvArr* dst)会将src中的每一个元素的每一位取反，然后把结果赋给dst  
        #cv.SaveImage(str(i)+ '.jpg',imageCopy)  
        i = i+1  
    sortedNum = sorted(dictPic.keys())  
    for i in range(len(sortedNum)):  
        pic[i] = dictPic[sortedNum[i]]  
    #cv2.waitKey(0) 
    print len(pic) 
    return pic[27] 


def image_match(img1,img2):
    #detector = cv2.ORB(800)#400
    detector = cv2.SIFT()
    FLANN_INDEX_LSH    = 6
    flann_params = dict(algorithm = FLANN_INDEX_LSH,
                       table_number = 15, # 12
                       key_size = 1,     # 20
                       multi_probe_level = 3) #2
    #matcher = cv2.FlannBasedMatcher(flann_params, {}) 
    matcher = cv2.BFMatcher()

    kp1, des1 = detector.detectAndCompute(img1,None)
    kp2, des2 = detector.detectAndCompute(img2,None)
    raw_matches =  matcher.match(des1,des2)
    #raw_matches = matcher.knnMatch(des1,des2, k = 2) #2
    
    return len(raw_matches)



    print len(raw_matches)
    h1, w1 = img2.shape[:2]
    vis = np.zeros((h1, w1), np.uint8)
    vis = img2
    #vis = cv2.cvtColor(vis, cv2.COLOR_GRAY2BGR)

    p1, p2, kp_pairs = filter_matches(kp1, kp2, raw_matches,0.99)

    x1,y1,x2,y2 = find_rect(p2,img2)

    color = (0, 255, 0)
    cv2.rectangle(vis, (x1, y1), (x2, y2), color, 2)
    return vis


def read_feature_file(filename):

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


def comparehits_min(image,featureimage):
    h, w = image.shape[:2]
    h_f, w_f = featureimage.shape[:2]

    bins = w_f

    # image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    # fer_gray = cv2.cvtColor(featureimage, cv2.COLOR_BGR2HSV)

    fer_gray = cv2.cvtColor(featureimage,cv2.COLOR_BGR2GRAY) 
    image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) 


    hist_fer = cv2.calcHist([fer_gray],[0],None,[bins],[0,255.0]) 
    #hist_fer = cv2.normalize(hist_fer).flatten()


    image1M = cv.fromarray(image_gray)
    image1Ip = cv.GetImage(image1M)
    
    bc_min = 1
    start_px = -1 
    for i in xrange(int(w-w_f)):
        rc = (i, 0, w_f, h_f)
        #rc = (0, 0, w_f, h_f)
        cv.SetImageROI(image1Ip,rc)  
        imageCopy = cv.CreateImage((rc[2], rc[3]),cv2.IPL_DEPTH_8U,1)  
        cv.Copy(image1Ip,imageCopy)  
        cv.ResetImageROI(image1Ip) 
        simg = np.asarray(cv.GetMat(imageCopy))
       
        cv2.imwrite("tmp.jpg", simg)
        sub_img = cv2.imread("tmp.jpg")
        hist_sub = cv2.calcHist([sub_img],[0],None,[bins],[0,255.0]) 
        #hist_sub = cv2.normalize(hist_sub).flatten()
       
        #相关：CV_COMP_CORREL    
        #卡方：CV_COMP_CHISQR
        #直方图相交：CV_COMP_INTERSECT
        # Bhattacharyya距离：CV_COMP_BHATTACHARYYA
        inter = cv2.compareHist(hist_fer, hist_sub, cv2.cv.CV_COMP_BHATTACHARYYA)
        if( inter < bc_min):
            bc_min = inter
            start_px = i
       
    return start_px

def comparehits(image,featureimage,startx = 0,endx=0):
    h, w = image.shape[:2]
    h_f, w_f = featureimage.shape[:2]

    fer_gray = cv2.cvtColor(featureimage,cv2.COLOR_BGR2GRAY) 
    image_gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY) 

    hist_fer = cv2.calcHist([fer_gray],[0],None,[w_f],[0,255.0]) 
   


    image1M = cv.fromarray(image_gray)
    image1Ip = cv.GetImage(image1M)
    
    bc_min = 0.04
    start_px = -1 
    for i in xrange(int(w-w_f-endx+startx)):
        rc = (i+startx, 0, w_f, h_f)
        cv.SetImageROI(image1Ip,rc)  
        imageCopy = cv.CreateImage((rc[2], rc[3]),cv2.IPL_DEPTH_8U, 1)  
        cv.Copy(image1Ip,imageCopy)  
        cv.ResetImageROI(image1Ip) 
        simg = np.asarray(cv.GetMat(imageCopy))
       
        cv2.imwrite("tmp.jpg", simg)
        sub_img = cv2.imread("tmp.jpg")
        hist_sub = cv2.calcHist([sub_img],[0],None,[w_f],[0,255.0]) 

        #相关：CV_COMP_CORREL    
        #卡方：CV_COMP_CHISQR
        #直方图相交：CV_COMP_INTERSECT
        # Bhattacharyya距离：CV_COMP_BHATTACHARYYA
        inter = cv2.compareHist(hist_fer, hist_sub, cv2.cv.CV_COMP_BHATTACHARYYA)
        if( inter < bc_min):
            start_px = i+startx
            print inter
            break
       
    return start_px



def find_point(image):
    mach_list = []
    match_info = []

    feature_point = read_feature_file("point.txt")
    feature_map = read_feature_file("mapname.txt")

    #先查找数字和汉字的分隔符
    img_left = cv2.imread("left.png")
    left_x = comparehits_min(image,img_left)
    left_x =left_x-1
    img_right = cv2.imread("right.png")
    right_x = comparehits_min(image,img_right)

    print "left:",left_x," right:",right_x

    #匹配地图名字
    for i in xrange(len(feature_map)):
        img = cv2.imread(feature_map[i][0])
        start_px = comparehits(image,img,0,left_x)
        if start_px > -1 :
           mach_list.append((start_px,feature_map[i][1]))
           print start_px,":",feature_map[i][1].decode('utf-8')

    mach_list.sort(cmp = lambda x ,y : cmp(x[0],y[0]))        
    for m in mach_list:
       match_info.append(m[1])

    #匹配坐标
    mach_list =[]
    for i in xrange(len(feature_point)):
        img = cv2.imread(feature_point[i][0])
        start_px = comparehits(image,img,left_x+6,right_x)
        if start_px > -1 :
           mach_list.append((start_px,feature_point[i][1]))
           print start_px,":",feature_point[i][1].decode('utf-8')
    
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

    h, w = cv_title_image.shape[:2]

    img_left = cv2.imread("left.png")
    left_x = comparehits_min(cv_title_image,img_left)
    img_right = cv2.imread("right.png")
    right_x = comparehits_min(cv_title_image,img_right) 

    print "left:",left_x," right:",right_x

    #切割汉字11个像素
    endx = left_x - 2
    while endx > 12:
        bounds = (endx-11,0,endx,h)
        sub_img = title_image.crop(bounds) 
        sub_img.save("point/"+str(endx)+".png") 
        print endx
        endx = endx -11 -1

    #切割数字5个像素
    endx = right_x - 2
    while endx-left_x > 6:
        bounds = (endx-5,0,endx,h)
        sub_img = title_image.crop(bounds) 
        sub_img.save("point/s_"+str(endx)+".png") 
        print endx
        endx = endx -5 -1    

if __name__ == '__main__':


    hm = pyHook.HookManager()
    hm.KeyDown = KeyStroke
    hm.HookKeyboard()
    #RCImageViewerFrame
    #WSGAME
    #hwnd = get_window("RCImageViewerFrame")
    hwnd = get_window("WSGAME")


    #open_cv_image = get_window_image(hwnd)
    #img = image_despose(open_cv_image)
    title_image1 = Image.open('point.jpg')
    title_image2 = Image.open('point1.png')
    split_point(title_image1)
    split_point(title_image2)
    exit()
    
    img = cv2.imread('point.jpg')
    fer_gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY) 

    hist_fer = cv2.calcHist([fer_gray],[0],None,[1100],[0,255]) 
    plt.figure()
    plt.plot(range(len(hist_fer)),hist_fer)
    plt.show()
    exit()
    #comparehits(img)
    mach_list = find_point(img)
    info = ""
    for m in mach_list:
        info+=m
    #print x.decode('utf-8')
    print info.decode('utf-8')
    cv2.imshow('frame',img)
    cv2.waitKey(0) 
    exit()


    while(True):
        open_cv_image = get_window_image(hwnd)
        img = image_despose(open_cv_image) 
        cv2.imshow('frame',img)
        # show_img = find_title(open_cv_image)
        # cv2.imshow('frame',show_img)
        

        pythoncom.PumpWaitingMessages()

    cv2.destroyAllWindows()