#! -*- coding=utf-8 -*-
import time
from machines.StateMachine import Machine
from appium4droid import webdriver
from appium4droid.common.exceptions import *
from appium4droid.support.ui import WebDriverWait

try:
    from util import reset_wifi, alert
except ImportError:
    reset_wifi = lambda: 1
    alert = lambda: 1


class MachineVPN(Machine):
    def __init__(self, driver):
        super(MachineVPN, self).__init__(self.enter_vpn)
        self.driver = driver
        self.reconnect_times = 0

    def enter_vpn(self):
        dr = self.driver
        dr.press_keycode(3)  # back to Home
        time.sleep(1)
        dr.press_keycode(3)  # back to Home
        time.sleep(1)
        dr.find_element_by_name("无极VPN").click()
        time.sleep(1)
        #检测是否已登录
        try:
            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("org.wuji:id/loginbutton")).click()
        except TimeoutException:
            pass
        return self.reconnect

    def reconnect(self):
        dr = self.driver
        time.sleep(2)
        #切换VPN
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("org.wuji:id/exit_vpn")).click()
        time.sleep(1)
        try:
            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("正在初始化数据")).click()
        except TimeoutException:
            pass
        #检测连接成功
        try:
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.miui.home:id/cell_layout"))
        except TimeoutException:
            return self.onConnectTimeout
        self.reconnect_times = 0
        dr.press_keycode(3)
        return self.exit

    def onConnectTimeout(self):
        print("connect failed!!")
        self.reconnect_times = 1 + self.reconnect_times
        if self.reconnect_times > 5:
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("org.wuji:id/exit_button")).click()
            time.sleep(5)
            # alert()
            reset_wifi()
            self.reconnect_times = 0
            return self.enter_vpn
        return self.reconnect


if __name__ == "__main__":
    dr = webdriver.Remote()
    time.sleep(2)
    dr.press_keycode(3)

    MachineVPN(dr).run()
