#! -*- coding=utf-8 -*-
import time
from machines.StateMachine import Machine
from appium4droid import webdriver
from appium4droid.common.exceptions import *
from appium4droid.support.ui import WebDriverWait
import requests
import re

try:
    from util import reset_wifi, alert
except ImportError:
    reset_wifi = lambda: 1
    alert = lambda: 1


class MachineVPN(Machine):
    def __init__(self, driver):
        super(MachineVPN, self).__init__(self.enter_setting)
        self.driver = driver
        self.reconnect_times = 0

    def enter_setting(self):
        dr = self.driver
        dr.press_keycode(3)  # back to Home
        time.sleep(1)
        dr.press_keycode(3)  # back to Home
        time.sleep(1)
        dr.find_element_by_name("设置").click()
        time.sleep(1)

        return self.enter_vpn

    def enter_vpn(self):
        dr = self.driver
        dr.find_element_by_name("其他连接方式").click()
        time.sleep(1)
        dr.find_element_by_name("VPN").click()
        time.sleep(1)
        return self.close_connection

    def close_connection(self):
        dr = self.driver
        try:
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("已连接")).click()
            time.sleep(1)
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("断开连接")).click()
            time.sleep(1)
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("PPTP VPN")).click()
            time.sleep(1)
            print("thats ok")
        except TimeoutException as e:
            print("in else")
            # vpn = dr.find_element_by_name("PPTP VPN")
            dr.find_element_by_class_name("android.widget.RadioButton").click()
            # dr.tap(300, 425)
        return self.reconnect

    def reconnect(self):
        CONNECT_WAIT_TIME = 30

        dr = self.driver
        # time.sleep(2)
        # dr.find_element_by_name("连接").click()
        ## maybe should try and except here
        try:
            WebDriverWait(dr, CONNECT_WAIT_TIME).until(lambda d: d.find_element_by_name("已连接"))
        except TimeoutException:
            return self.onConnectTimeout
        if self.log_ip("浙江"):
            return self.close_connection()
        if self.log_ip("江苏"):
            return self.close_connection()
        self.reconnect_times = 0
        dr.press_keycode(3)
        return self.exit

    def onConnectTimeout(self):
        print("connect failed!!")
        self.reconnect_times = 1 + self.reconnect_times
        if self.reconnect_times > 3:
            alert()
            reset_wifi()
            self.reconnect_times = 0
        return self.close_connection

    # def Exit(self):
    #     self.running = False
    #     print("going to Exit")
    #     dr = self.driver
    #     dr.press_keycode(3)
    #     return None

    def ExceptinOccur(self):
        self.running = False
        print("ExceptinOccur!!!")
        self.driver.press_keycode(3)
        return None

    def log_ip(self, notlotation):
        WEB_URL = 'http://ip.chinaz.com/getip.aspx'
        r = requests.get(WEB_URL)
        print(r.text)
        match = re.search(r'ip:\'(.+)\'\,address:\'(.+)\'', r.text)
        if match:
            addr = match.group(2)
            match_addr = re.findall(notlotation, addr)
            if match_addr:
                return True


if __name__ == "__main__":
    dr = webdriver.Remote()
    time.sleep(2)
    dr.press_keycode(3)

    MachineVPN(dr).run()
