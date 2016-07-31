# -*- coding: utf-8 -*-

import ctypes
import time

dll = ctypes.windll.LoadLibrary( 'dd/DD64.dll' )

def DD_btn(mode):
    """
    功能： 模拟鼠标点击
    参数： 1 =左键按下 ，2 =左键放开
    4 =右键按下 ，8 =右键放开
    16 =中键按下 ，32 =中键放开
    64 =4键按下 ，128 =4键放开
    256 =5键按下 ，512 =5键放开
    """
    dll.DD_btn(mode)

def DD_btn_click(mode=1,dealy = 0.05):
    if mode == 1:
        dll.DD_btn(1)
        time.sleep(dealy)
        dll.DD_btn(2)
    else:
        dll.DD_btn(4)
        time.sleep(dealy)
        dll.DD_btn(8)

def DD_mov(x,y):
    """
    功能： 模拟鼠标结对移动
    参数： 参数x , 参数y 以屏幕左上角为原点。
    """
    dll.DD_mov(x,y)


def DD_movR(x,y):
    """
    功能： 模拟鼠标相对移动
    参数： 参数dx , 参数dy 以当前坐标为原点。
    """
    dll.DD_movR(x,y)

def DD_key(key,mode):
    """
    功能： 模拟键盘按键
    参数： 参数1 ，请查看[DD虚拟键盘码表]。
    参数2，1=按下，2=放开
    """
    dll.DD_key(key,mode)

def DD_key_click(key,dealy = 0.05):
    dll.DD_key(key,1)
    time.sleep(dealy)
    dll.DD_key(key,2)

def DD_todc(key):
    """
    功能： 转换Windows虚拟键码到 DD 专用键码.
    参数： Windows虚拟键码
    """
    return dll.DD_todc(key)

def DD_str(str_value):
    """
    功能： 直接输入键盘上可见字符和空格
    参数： 字符串, (注意，这个参数不是int32 类型)
    """
    dll.DD_str(str_value)
