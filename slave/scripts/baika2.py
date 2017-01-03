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
# from machines.machine008 import Machine008
from machines.machineXposeHook import MachineXHook as Machine008
from appium4droid import webdriver
from bootstrap import setup_boostrap
from TotalMachine import WorkMachine
from appium4droid.support.ui import WebDriverWait
from machines.StateMachine import Machine
from sock.socksend import send_file
from random import choice
try:
    from util import replace_wifi
except ImportError:
    replace_wifi = lambda: 1
from jiema.shenhuaSDK import Shenhua



class TotalMachine(WorkMachine):
    def load_task_info(self):
        return []

    def setup_machine(self):
        dr = self.driver
        self.runnum = 0
        self.machine008 = Machine008(dr)
        self.machine008.task_schedule = ["record_file", "clear_data", "modify_data_suiji"]    # 007 task list


    def main_loop(self):
        dr = self.driver
        m008 = self.machine008
        #切换脚本输入法
        dr.press_keycode(63)
        time.sleep(1)
        dr.find_element_by_name("Appium Android Input Manager for Unicode").click()
        time.sleep(1)
        pwd_li = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                  "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                  "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                  "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                  "u", "v", "w", "x", "y", "z"]
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
                #计数器清0
                if time.localtime().tm_hour == 0 and self.runnum > 12:
                    self.runnum = 0
                MachineVPN(dr).run()
                m008.run()
                ###################################################################################################################
                self.begintime = "开始:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("Chrome")).click()
                time.sleep(1)
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.android.chrome:id/terms_accept")).click()
                time.sleep(1)
                #输入网址
                edts = WebDriverWait(dr, 30).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
                edts.send_keys("http://api.51ygdai.com/act/light-loan?source_tag=&from=singlemessage&isappinstalled=0")
                time.sleep(1)
                dr.press_keycode(66)
                time.sleep(1)
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@content-desc='获取验证码']"))
                code = Shenhua("xiaoxiaozhuan", "meiriq2014", 95685)
                for i in range(5):
                    #登录接码平台
                    try:
                        code.login()
                        break
                    except Exception as e:
                        print("error in login")
                    if i == 4:
                        print("接码平台登录失败")
                        time.sleep(60)
                        raise Exception("接码平台登录失败")
                for i in range(5):
                    phone_num = code.getPhone()
                    edts = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_class_name("android.widget.EditText"))
                    #输入手机号码
                    edts[0].send_keys(phone_num)
                    time.sleep(1)
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@content-desc='获取验证码']")).click()
                    time.sleep(1)
                    #选择接码平台获取验证码
                    #【现金卡】您的验证码为:299038 (此验证码有效期为30分钟)
                    regrex = r'验证码为:(\d+)'
                    captcha = code.waitForMessage(regrex, phone_num)
                    if captcha is None:
                        #释放号码
                        code.releasePhone(phone_num)
                        edts[0].click()
                        dr.press_keycode(123)
                        time.sleep(0.5)
                        for _ in range(15):
                            dr.press_keycode(67)
                    else:
                        break
                    if i == 4:
                        print("获取验证码失败")
                        time.sleep(60)
                        raise Exception("获取验证码失败")
                #输入验证码
                edts[2].send_keys(captcha)
                time.sleep(1)
                pwd = ""
                for _ in range(random.randint(6, 8)):
                    pwd += choice(pwd_li)
                edts[1].send_keys(pwd)
                time.sleep(1)
                dr.swipe(300, 800, 300, 400)
                time.sleep(1)
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.widget.Button[@content-desc='立即申请']")).click()
                time.sleep(1)
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_xpath("//android.view.View[@content-desc='立即下载APP，一键提现']"))
                time.sleep(random.randint(5, 10))
                dr.press_keycode(3)
                time.sleep(1)
                #结束记录信息
                self.endstime = "结束:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
                time.sleep(2)
                try:
                    with open('/sdcard/1/baijin.log', 'a') as f:
                        f.write('\n激活 %s.%s, %s, %s, count:%s' % (time.localtime().tm_mon, time.localtime().tm_mday, self.begintime, self.endstime, self.runnum))
                except:
                    pass
                time.sleep(3)
                self.runnum += 1
            except Exception as e:
                print("somting wrong")
                print(e)
            finally:
                pass
            print("Again\n")
        return self.exit

    #随机滑动
    def swipes(self, x1, y1, x2, y2, swipe_num=1, swipe_time_min=1, swipe_time_max=1):
        dr = self.driver
        print("swipenum:%s" % swipe_num)
        for x in range(swipe_num):
            dr.swipe(x1, y1, x2, y2)
            time.sleep(random.randint(swipe_time_min, swipe_time_max))

    # 上传记录文件
    def upload_file(self, addr, file):
        replace_wifi()
        time.sleep(1)
        replace_wifi()
        time.sleep(5)
        try:
            with open('/sdcard/device.txt', 'r') as f:
                selectuser = f.read()
        except:
            with open('device.txt', 'r') as f:
                selectuser = f.read()
        device = re.search(r'device:([0-9a-zA-Z\.]+)', selectuser).group(1)
        for filename in file: #最多可发送文件数量
            # filename = re.search(r'filename%s:([0-9a-zA-Z\.]+)' % num, selectuser)
            if filename:
                if os.path.exists(filename) or os.path.exists('/sdcard/1/' + filename): #检测文件是否存在,不存在不发送
                    send_file(device, filename, addr)
                else:
                    print("not find the file:%s" % filename)
            else:
                break
            time.sleep(2)

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
