# -*- coding: utf-8 -*-

import threading
import multiprocessing
from time import ctime,sleep
from Tools import *
import win32gui
from PIL import ImageGrab
from PIL import Image
import win32con
import cv2
from cv2 import cv
import numpy as np

class FindImage(object):
    def __init__(self,queryImageName,className,max_sum=2, bins = 30,move_px = 1,move_py = 1,prox_num=2,proy_num=2):

        #cv2.imread(queryImageName)
        self.queryImageName = queryImageName
        self.className = className
        self.max_sum = max_sum
        self.bins = bins
        self.move_px = move_px
        self.move_py = move_py
        self.prox_num = prox_num
        self.proy_num = proy_num

        self.lock  = multiprocessing.Lock()
        self.ExitQueue = multiprocessing.Queue(prox_num*proy_num)
        self.ResultQueue = multiprocessing.Queue(prox_num*proy_num)

        self.ProcessList = []

    def p_find_image(self,startx = 0 ,endx = 0,starty = 0 ,endy = 0):
        hwnd =  get_window_hwnd(self.className)
        queryImage = cv2.imread(self.queryImageName)
        self.lock.acquire()
        print "P startx:",startx,"  starty:",starty
        self.lock.release()
        while 1:
            if self.ExitQueue.qsize() > 0:
            	return
            trainImage = get_window_rect_image(hwnd)
            find_list  = find_obj_hist(trainImage,queryImage,max_sum=self.max_sum, bins = self.bins,startx = startx
             ,endx = endx,starty = starty ,endy = endy,move_px = self.move_px,move_py = self.move_py)
            if len(find_list) > 0:
                self.ResultQueue.put(find_list[0])

    def run(self):
        trainImage_rect = self.get_trainImage_rect()
        h, w = trainImage_rect[3]-trainImage_rect[1],trainImage_rect[2]-trainImage_rect[0]
        queryImage = cv2.imread(self.queryImageName)
        h_f, w_f = queryImage.shape[:2]

        subw = int(w/self.prox_num)
        subh = int(h/self.proy_num)
        for j in range(self.proy_num):
            sub_starty = j*subh
            sub_endy = j*subh+subh
            if j>0:
                sub_starty = sub_starty-h_f
                sub_endy = sub_endy-h_f
            if sub_endy>h : sub_endy = h

            for i in range(self.prox_num):
                sub_startx = i*subw
                sub_endx = i*subw+subw
                if i>0:
                    sub_startx = sub_startx-w_f
                    sub_endx = sub_endx-w_f
                if sub_endx>w : sub_endx = w

                #print (sub_startx,sub_endx,sub_starty,sub_endy)
                process = multiprocessing.Process(target=self.p_find_image,args=(sub_startx,sub_endx,sub_starty,sub_endy))
                process.start()
                #self.ProcessList.append(process)

    def get_result(self):
        result = None
        if self.ResultQueue.qsize() > 0:
        	result = self.ResultQueue.get()
        return result


    def stop(self):
		self.ExitQueue.put(1)

		self.ProcessList =[]

    def get_trainImage_rect(self):
		hwnd =  get_window_hwnd(self.className)
		game_rect = win32gui.GetWindowRect(hwnd)
		client_rect = win32gui.GetClientRect(hwnd)
		title_h =  game_rect[3] - game_rect[1] - client_rect[3]
		game_rect = (game_rect[0],game_rect[1]+title_h,game_rect[2],game_rect[3])
		return game_rect
