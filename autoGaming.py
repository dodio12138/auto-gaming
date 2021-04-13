# -*- coding: UTF-8 -*-
"""
@author:dodio
@description:基于OpenCv的自动玩Google小恐龙游戏的程序
@file:autoGaming.py
@time:2021/04/12
"""
from selenium import webdriver
import cv2 as cv
import pyautogui as pg
import numpy as np


def trackObj(trackScr, obj, conf=0.14):
    """
    追踪指定的目标位置
    :param trackScr:需要追踪的场景
    :param obj: 需要最终的目标图片（模板）
    :param conf: 相似度系数
    :return:返回目标框的左上和右下角坐标
    """
    result = cv.matchTemplate(trackScr, obj, cv.TM_SQDIFF_NORMED)  # 模板匹配
    minVal, maxVal, minLoc, maxLoc = cv.minMaxLoc(result)  # 获取相似度数组
    obj_w, obj_h, _ = obj.shape  # 获取模板宽高
    topLeft = minLoc  # 目标框的左上角坐标
    bottomRight = (topLeft[0] + int(obj_w), topLeft[1] + int(obj_h))  # 目标框的右下角坐标
    # print(minVal)
    if minVal < conf:  # 判断相似度系数
        return topLeft, bottomRight
    else:
        return False, False


def detectObstacles(area):
    """
    检测区域内的障碍物
    :param area:检测区域
    :return:区分值
    """
    cv.cvtColor(area, cv.COLOR_BGR2HSV)  # 色彩空间转换
    ave_brightness = 1  # 平均亮度
    color_w, color_h, _ = area.shape  # 获取区域的宽高
    for i in range(color_w):
        for j in range(color_h):
            if area[i][j][2] < 150:
                ave_brightness += 1
            else:
                ave_brightness += 0
            # print(track[i][j][2])
    ave_brightness = (color_h * color_h) / ave_brightness
    # print(sum)
    return ave_brightness


driver = webdriver.Chrome()  # 声明一个浏览器驱动
driver.maximize_window()  # 最大化窗口
driver.get('https://dino.zone/zh-cn/')  # 打开对应的游戏网页

sW, sH = pg.size()  # 获取电脑屏幕大小
dinosaur = cv.imread('templatePic/dinosaur1.jpg')  # 载入目标物体模板

while 1:
    screen = pg.screenshot()  # 获取当前屏幕画面
    screen = cv.cvtColor(np.asarray(screen), cv.COLOR_RGB2BGR)  # 转换为OpenCv格式图像
    trackPic = cv.resize(screen, (int(sW / 2), int(sH / 2)))  # 待追踪的画面
    a1, b1 = trackObj(trackPic, dinosaur)
    a2, b2 = 0, 0  # 区域碰撞检测的左上和右下角坐标
    # print(a1, b1)
    if a1:
        a2 = (int((a1[0] + 300) / 2), int((a1[1] + 220) / 2))
        b2 = (int((a1[0] + 410) / 2), int((a1[1] + 220 + 80) / 2))
        cv.rectangle(trackPic, a1, b1, (255, 0, 255), thickness=1)  # 画出目标物体框
    else:
        a2 = (int((125 + 300) / 2), int((272 + 220) / 2))
        b2 = (int((125 + 400) / 2), int((272 + 220 + 80) / 2))
    detect_area = trackPic[a2[1]:b2[1], a2[0]: b2[0]]  # 划定碰撞检测区域
    space = detectObstacles(detect_area)  # 判断
    if 100 > space > 5:  # 判断亮度阈值
        pg.press(' ')  # 有障碍则按下空格键
    if space < 3:  # 游戏失败则重新开始游戏
        pg.moveTo(1222, 696, duration=1, tween=pg.easeInOutSine)
        pg.click()
        pg.moveTo(522, 496, duration=1, tween=pg.easeInOutSine)
    cv.rectangle(trackPic, a2, b2, (0, 255, 255), thickness=1)  # 画出检测区域
    cv.imshow('trackPic', trackPic)

    if cv.waitKey(5) & 0XFF == 27:
        break

