#! -*- coding=utf-8 -*-
import os
import sys


filepath = os.path.abspath(__file__)
sys.path.append(os.path.dirname(os.path.dirname(filepath)))

import threading
import time

from datetime import datetime
from multiprocessing import Process
from machines.machineVPN import MachineVPN
# from machines.machineWujiVPN import MachineVPN
from machines.machineXposeHook import MachineXHook as Machine008
from appium4droid import webdriver
from bootstrap import setup_boostrap
from TotalMachine import WorkMachine
from appium4droid.support.ui import WebDriverWait
from machines.StateMachine import Machine
import random
import requests
import re


class TotalMachine(WorkMachine):
    def load_task_info(self):
        return []

    def setup_machine(self):
        dr = self.driver
        self.machine008 = Machine008(dr)
        self.machine008.task_schedule = ["record_file", "clear_data", "modify_data_suiji"]  # 007 task list
        self.appname = "testsdk"

    def main_loop(self):
        dr = self.driver
        m008 = self.machine008
        while True:
            try:
                dr.press_keycode(3)
                time.sleep(1)
                dr.press_keycode(3)
                time.sleep(1)
                #清后台
                # dr.press_keycode(82)
                # time.sleep(1)
                # WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.android.systemui:id/clearButton")).click()
                # time.sleep(1)
                MachineVPN(dr).run()
                m008.run()
                # dr.press_keycode(3)
                # time.sleep(1)
                # dr.press_keycode(3)
                # time.sleep(1)
                # WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name(self.appname)).click()
                # time.sleep(5)
                # 开启加速
                # dr.press_keycode(3)
                # time.sleep(1)
                # WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("GMD Speed Time")).click()
                # time.sleep(1)
                # WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.gmd.speedtime:id/buttonStart")).click()
                # time.sleep(2)
                dr.press_keycode(3)
                time.sleep(1)
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name(self.appname)).click()
                time.sleep(15)
                #记录ip
                self.log_ip()
                dr.press_keycode(3)
                time.sleep(5)
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name(self.appname)).click()
                time.sleep(1)
                #关闭加速
                # dr.press_keycode(3)
                # time.sleep(1)
                # WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("嘀嗒拼车")).click()
                # time.sleep(5)
                # WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.gmd.speedtime:id/buttonStop")).click()
                # time.sleep(1)
                # dr.press_keycode(3)
                # time.sleep(1)
            except Exception as e:
                print("somting wrong")
                print(e)
            finally:
                pass
            print("Again\n")
        return self.exit

    def log_ip(self):
        WEB_URL = 'http://ip.chinaz.com/getip.aspx'
        r = requests.get(WEB_URL)
        print(r.text)
        match = re.search(r'ip:\'(.+)\'\,address:\'(.+)\'', r.text)
        if match:
            print(match.group(1))
            print(match.group(2))
            ip = match.group(1)
            addr = match.group(2)
            with open('/sdcard/1/ip.log', 'a') as f:
                f.write('\n%s  %s' % (ip, addr))

if __name__ == "__main__":
        TM = TotalMachine()
        TM.run()