#! -*- coding=utf-8 -*-
import os
import sys

filepath = os.path.abspath(__file__)
sys.path.append(os.path.dirname(os.path.dirname(filepath)))

import time

from appium4droid import webdriver
# from appium4droid.support.ui import WebDriverWait
from appium.webdriver.common.touch_action import TouchAction
from appium.webdriver.common.multi_action import MultiAction
if __name__ == "__main__":
    dr = webdriver.Remote()

    while 1:
        dr.press_keycode(3)
        time.sleep(1)
        dr.swipe(100, 100, 500, 600)
        time.sleep(1)
        # action = TouchAction()
        # a = action.press(dr.find_element_by_name("花椒直播")).move_to(dr.find_element_by_name("斑马")).move_to(dr.find_element_by_name("上海观察")).move_to(dr.find_element_by_name("百大易购")).release()
        # a.perform()
        action1 = TouchAction(dr).press(100, 100).waitAction(1500)
        action2 = TouchAction(dr).press(100, 200).waitAction(1500)
        action3 = TouchAction(dr).press(200, 200).waitAction(1500)
        action4 = TouchAction(dr).press(200, 100).waitAction(1500)
        action5 = TouchAction(dr).press(100, 100).waitAction(1500)
        muction = MultiAction(dr)
        muction.add(action1).add(action2).add(action3).add(action4).add(action5).perform()
        # dr.swipe1(100, 100, 200, 200)
        # from appium.webdriver.common.touch_action import TouchAction
        # wd = TouchAction(dr)
        # wd.press(x=600, y=600).move_to(x=200, y=600).move_to(x=600, y=600).release()
        time.sleep(2)