import sys
import time
import os
import random
from cv2 import cv2
import numpy as np
from core import adb

adbkit = adb.adbKit()


def standby(template, acc=0.85, special=False):
    # 模擬器截圖
    adbkit.screenshots()
    # 载入图像
    target_img = cv2.imread("screencap.png")
    if special == True:
        cv2.rectangle(target_img, (0, 0), (1280, 420),
                      color=(0, 0, 0), thickness=-1)
        cv2.imwrite("screencap-rect.png", target_img)
    find_img = cv2.imread(str(template))
    find_height, find_width = find_img.shape[:2:]

    # 模板匹配
    result = cv2.matchTemplate(target_img, find_img, cv2.TM_CCOEFF_NORMED)
    # min_val, max__val, min_loc, max_loc = cv2.minMaxLoc(result)
    reslist = cv2.minMaxLoc(result)
    #reslist[1] = max__val; reslist[3] = max_loc;

    cv2.rectangle(target_img, reslist[3], (reslist[3][0]+find_height, reslist[3][1]+find_width),
                  color=(0, 255, 0), thickness=2)
    cv2.imwrite("screencap-rect.png", target_img)

    if reslist[1] > acc:
        print("acc rate:", round(reslist[1], 2))
        return reslist[3], find_height, find_width
    else:
        print("acc rate:", round(reslist[1], 2))
        return False, find_height, find_width


"""
def adbtap(pos):  # nouse 點擊圖像座標(改用固定座標)
    loc, h, w = pos
    pointCentre = (loc[0]+(w/2), loc[1]+(h/2))
    Px = int(pointCentre[0])
    Py = int(pointCentre[1])
    print("ready to tap", Px, ",", Py)
    adbkit.click(Px, Py)
"""


def get_pos(template, acc=0.9):
    pos = standby(template, acc)
    if pos[0]:
        print("get pos", pos[0])
        return pos
    else:
        return False


def tap(Px: int, Py: int):
    adbkit.click(Px, Py)


def list_tap(pos):
    adbkit.click(pos[0], pos[1])


def swipe(x1, y1, x2, y2, delay):
    adbkit.swipe(x1, y1, x2, y2, delay)
