#! -*- coding=utf-8 -*-
import os
import sys


filepath = os.path.abspath(__file__)
sys.path.append(os.path.dirname(os.path.dirname(filepath)))

import threading
import time
import re
import random
from datetime import datetime
from multiprocessing import Process
from appium4droid import webdriver
from bootstrap import setup_boostrap
from TotalMachine import WorkMachine
from machines.StateMachine import Machine
from appium4droid.common.exceptions import *
from appium4droid.support.ui import WebDriverWait
from random import choice

try:
    from util import replace_wifi
except ImportError:
    replace_wifi = lambda: 1
try:
    from util import screenshot, run_qpy2_script
except ImportError:
    screenshot = lambda: 1
    run_qpy2_script = lambda x: None

class TotalMachine(WorkMachine):
    def load_task_info(self):
        return []

    def setup_machine(self):
        dr = self.driver
        self.runnum = 0

    def main_loop(self):
        dr = self.driver
        #切换脚本输入法
        dr.press_keycode(63)
        time.sleep(1)
        dr.find_element_by_name("Appium Android Input Manager for Unicode").click()
        time.sleep(1)
        dr.press_keycode(3)
        time.sleep(1)
        dr.find_element_by_name("Chrome").click()
        time.sleep(1)
        while True:
            try:
                WebDriverWait(dr, 10).until(lambda d: d.find_elements_by_xpath("//android.view.View[@content-desc='兑换']"))[13].click()
                time.sleep(1)
                cdk = ""
                WebDriverWait(dr, 60).until(lambda d: d.find_element_by_name("恭喜你！成功领取复活币"))
                time.sleep(1)
                edts = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_class_name("android.widget.EditText"))
                cdk = edts[0].get_attribute("name")
                WebDriverWait(dr, 10).until(lambda d: d.find_element_by_xpath("//android.view.View[@content-desc='× 关闭']")).click()
                time.sleep(1)
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.android.chrome:id/tab_switcher_button")).click()
                time.sleep(1)
                dr.tap(300, 1120)
                time.sleep(1)
                edts = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_class_name("android.widget.EditText"))
                edts[0].click()
                for i in range(20):
                    dr.press_keycode(67)
                time.sleep(1)
                edts[0].send_keys(cdk)
                time.sleep(1)
                WebDriverWait(dr, 10).until(lambda d: d.find_element_by_xpath("//android.view.View[@content-desc='看不清楚，换一张']")).click()
                time.sleep(5)
                edts[1].click()
                for i in range(5):
                    dr.press_keycode(67)
                time.sleep(2)
                for _ in range(10):
                    screenshot("/sdcard/screenshot.png")
                    run_qpy2_script("get_captchaimg_cdk.py")
                    imgcaptcha = self.uuwise()
                    if imgcaptcha is None:
                        print("getimgcaptcha failed")
                        WebDriverWait(dr, 10).until(lambda d: d.find_element_by_xpath("//android.view.View[@content-desc='看不清楚，换一张']")).click()
                        time.sleep(1)
                        edts[1].click()
                        for i in range(5):
                            dr.press_keycode(67)
                        time.sleep(1)
                        continue
                    edts[1].send_keys(imgcaptcha)
                    WebDriverWait(dr, 10).until(lambda d: d.find_element_by_xpath("//android.view.View[@content-desc='确定']")).click()
                    try:
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("对不起，验证码错误，请重新输入!"))
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("确定")).click()
                        time.sleep(1)
                        WebDriverWait(dr, 10).until(lambda d: d.find_element_by_xpath("//android.view.View[@content-desc='看不清楚，换一张']")).click()
                        time.sleep(1)
                        edts[1].click()
                        for i in range(5):
                            dr.press_keycode(67)
                        time.sleep(1)
                    except TimeoutException:
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("确定")).click()
                        time.sleep(1)
                        break
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.android.chrome:id/tab_switcher_button")).click()
                    time.sleep(1)
                    dr.tap(300, 300)
                    time.sleep(1)

            except Exception as e:
                print("somting wrong")
                print(e)
            finally:
                pass
            print("Again\n")
        return self.exit

    def uuwise(self):
        dr = self.driver
        dr.press_keycode(3)
        time.sleep(1)
        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("UUWiseDemo")).click()
        time.sleep(1)
        try:
            dr.find_element_by_name("查分")
            dr.press_keycode(4)
            time.sleep(1)
        except NoSuchElementException:
            pass
        btlogin = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.example.uuwisedemo:id/btn_login"))
        edtsuser = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.example.uuwisedemo:id/et_loginname"))
        edtspwd = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.example.uuwisedemo:id/et_loginpwd"))
        uuuser = 'xiaoxiaozhuan'
        uupwd = 'meiriq2014'
        if edtsuser.text == uuuser and edtspwd.text == uupwd:
            pass
        else:
            edtsuser.send_keys(uuuser)
            time.sleep(1)
            edtspwd.send_keys(uupwd)
            time.sleep(1)
        btlogin.click()
        screenshotpath = dr.find_element_by_id("com.example.uuwisedemo:id/et_path")
        for x in range(10):
            screenshotpath.click()
            time.sleep(0.5)
            dr.press_keycode(123)
            time.sleep(0.5)
            for i in range(40):
                dr.press_keycode(67)
            if screenshotpath.text == "路径":
                break
        screenshotpath.send_keys('/sdcard/captcha.png')
        time.sleep(1)
        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.example.uuwisedemo:id/btn_recognize")).click()
        time.sleep(1)
        captcha = None
        try:
            msg = WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.example.uuwisedemo:id/txt_code"))
            match = re.search(r'验证码：\d+\|([0-9a-zA-Z]+)', msg.text)
            if match:
                captcha = match.group(1)
            else:
                captcha = None
        except:
            pass
        dr.press_keycode(4)
        time.sleep(1)
        dr.press_keycode(82)
        time.sleep(2)
        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("Chrome")).click()
        return captcha



if __name__ == "__main__":
    TM = TotalMachine()
    TM.run()
