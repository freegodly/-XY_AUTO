# -*- coding: utf-8 -*-
import sys
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

from FindGameBasicInfo import *






if __name__ == '__main__':

    gbi =GameBasicInfo()

    gbi.start()

    while 1:
        cmd=raw_input('mhxy:')

        if cmd=="exit":
            gbi.stop()
            exit()
        elif cmd == "gbi":
            print gbi.game_rect
            print gbi.client_rect
            print gbi.map_name
            print gbi.hero_location_info
            print gbi.minimap_location
        elif cmd == "go":
            point=raw_input('input point:')
            p = point.split(',')
            gbi.go_point(int(p[0]),int(p[1]))
