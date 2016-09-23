#! -*- coding=utf-8 -*-
import os
import sys

filepath = os.path.abspath(__file__)
sys.path.append(os.path.dirname(os.path.dirname(filepath)))

import time

from appium4droid import webdriver
from appium4droid.support.ui import WebDriverWait
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
        # action1 = TouchAction(dr).press(x=100, y=100)
        # action2 = TouchAction(dr).press(x=100, y=200)
        # action3 = TouchAction(dr).press(x=200, y=200)
        # action4 = TouchAction(dr).press(x=200, y=100)
        # muction = MultiAction(dr)
        # muction.add(action1).add(action2).add(action3).add(action4).perform()
        # dr.swipe1(100, 100, 200, 200)
        # from appium.webdriver.common.touch_action import TouchAction
        wd = TouchAction(dr)
        wd.press(x=600, y=600).move_to(x=200, y=600).move_to(x=600, y=600).release().perform()
        # time.sleep(2)
        # els = dr.find_elements_by_class_name('android.view.View')
        # a1 = TouchAction()
        # a1.press(els[0]).move_to(x=10, y=0).move_to(x=10, y=-75).move_to(x=10, y=-600).release()
        #
        # a2 = TouchAction()
        # a2.press(els[1]).move_to(x=10, y=10).move_to(x=10, y=-300).move_to(x=10, y=-600).release()
        #
        # ma = MultiAction(dr, els[0])
        # ma.add(a1, a2)
        # ma.perform()

        # action1 = TouchAction(dr)
        # el = dr.find_element_by_id('XXXXX1')
        # action1.long_press(el).wait(10000).perform()

        # action2 = TouchAction(dr)
        # el = dr.find_element_by_id('XXXXX2')
        # action2.moveTo(el).release().perform()