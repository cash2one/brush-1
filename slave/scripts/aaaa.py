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
from machines.machineVPN import MachineVPN
# from machines.machineVPN_4c import MachineVPN
# from machines.machineWujiVPN import MachineVPN
# from machines.machine008 import Machine008
from machines.machineXposeHook import MachineXHook as Machine008
from appium4droid import webdriver
from bootstrap import setup_boostrap
from TotalMachine import WorkMachine
from appium4droid.support.ui import WebDriverWait
from machines.StateMachine import Machine
from random import choice
from appium4droid.common.exceptions import *



class TotalMachine(WorkMachine):
    def load_task_info(self):
        return []

    def setup_machine(self):
        dr = self.driver
        self.runnum = 0
        self.machine008 = Machine008(dr)
        self.machine008.task_schedule = ["record_file", "clear_data", "uninstall_apk", "modify_data_suiji"]    # 007 task list

    def main_loop(self):
        dr = self.driver
        m008 = self.machine008
        #切换脚本输入法
        dr.press_keycode(63)
        time.sleep(1)
        dr.find_element_by_name("Appium Android Input Manager for Unicode").click()
        time.sleep(1)
        while True:
            try:
                dr.press_keycode(3)
                time.sleep(1)
                dr.press_keycode(3)
                time.sleep(1)
                dr.press_keycode(66)
                time.sleep(1)
                dr.press_keycode(66)
                time.sleep(1)
                #清后台
                # dr.press_keycode(82)
                # time.sleep(1)
                # WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.android.systemui:id/clearButton")).click()
                # time.sleep(1)
                #计数器清0
                if time.localtime().tm_hour == 0 and self.runnum > 12:
                    self.runnum = 0
                MachineVPN(dr).run()
                m008.run()
                dr.press_keycode(3)
                time.sleep(1)
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("文件管理")).click()
                time.sleep(1)
                try:
                    WebDriverWait(dr, 10).until(lambda d: d.find_element_by_name("安装包")).click()
                    time.sleep(1)
                except TimeoutException:
                    dr.press_keycode(4)
                    time.sleep(1)
                    WebDriverWait(dr, 10).until(lambda d: d.find_element_by_name("安装包")).click()
                    time.sleep(1)
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("htscCFTApp110.apk")).click()
                time.sleep(1)
                try:
                    WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("安装")).click()
                    time.sleep(1)
                except TimeoutException:
                    WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("替换")).click()
                    time.sleep(1)
                    WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("安装")).click()
                    time.sleep(1)
                WebDriverWait(dr, 180).until(lambda d: d.find_element_by_name("打开")).click()
                time.sleep(5)
                WebDriverWait(dr, 180).until(lambda d: d.find_element_by_id("com.lphtsccft:id/introduceRadioGroup"))
                self.begintime = "开始:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
                for _ in range(2):
                    dr.swipe(300, 600, 300, 200)
                    time.sleep(1)
                WebDriverWait(dr, 180).until(lambda d: d.find_element_by_id("com.lphtsccft:id/introducePageViewPager")).click()
                time.sleep(5)
                for _ in range(3):
                    dr.press_keycode(4)
                    time.sleep(1)
                    try:
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("确定")).click()
                        time.sleep(1)
                        break
                    except TimeoutException:
                        pass
                dr.press_keycode(4)
                time.sleep(1)
                dr.press_keycode(4)
                time.sleep(1)
                #记录时间
                self.endstime = "结束:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
                print(self.begintime)
                print(self.endstime)
                try:
                    with open('/sdcard/1/timeaaaaa.log', 'a') as f:
                        f.write('\n激活 %s.%s, %s, %s, count:%s' % (time.localtime().tm_mon, time.localtime().tm_mday, self.begintime, self.endstime, self.runnum))
                except:
                    pass
                time.sleep(1)
            except Exception as e:
                print("somting wrong")
                print(e)
            finally:
                pass
            print("Again\n")
        return self.exit


    #控制激活量
    def ctrl_new(self, filename, num=100, sleep_time=1800):
        with open("/sdcard/1/%s.log" % filename, 'r', encoding='utf-8') as f:
            a = f.read()
        match = re.findall(r'激活 %s.%s' % (time.localtime().tm_mon, time.localtime().tm_mday), a)
        if match.__len__() >= num:
            print("激活数已达%s,暂停30分钟" % match.__len__())
            time.sleep(sleep_time)
            return True
        else:
            return False



if __name__ == "__main__":
    TM = TotalMachine()
    TM.run()
