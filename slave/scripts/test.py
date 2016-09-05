#! -*- coding=utf-8 -*-
import os
import sys

filepath = os.path.abspath(__file__)
sys.path.append(os.path.dirname(os.path.dirname(filepath)))

import time

from appium4droid import webdriver
# from appium4droid.support.ui import WebDriverWait
from appium.webdriver.common.touch_action import TouchAction

if __name__ == "__main__":
    dr = webdriver.Remote()

    while 1:
        dr.press_keycode(3)
        time.sleep(1)
        # dr.swipe(100, 100, 200, 200)
        # dr.press_keycode(3)
        # time.sleep(1)
        # dr.swipe1(100, 100, 100, 200)
        # time.sleep(10)
        # time.sleep(1)
        action = TouchAction(dr)
        action.press(dr.find_element_by_name("求偶")).move_to(dr.find_element_by_name("斑马")).move_to(dr.find_element_by_name("上海观察")).move_to(dr.find_element_by_name("百大易购")).release().perform()
        time.sleep(5)