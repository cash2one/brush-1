#! -*- coding=utf-8 -*-
import os
import time
# import logging
import random
import re
from machines.StateMachine import Machine
from appium4droid import webdriver
from appium4droid.common.exceptions import *
from appium4droid.support.ui import WebDriverWait
from random import choice


class Machinex(Machine):
    def __init__(self, driver):
        super(Machinex, self).__init__(self.initdata)
        self.driver = driver
        self.appname = "永恒之歌"       #app名字
        self.appname_en = "yongheng"     #记录文件用缩写英文名
        self.imei = None
        self.runnum = None        #记录运行次数

    def initdata(self):
        self.phone = None
        self.pwd = None
        self.begintime = None
        self.endstime = None
        self.try_count = 0      #初始化出错尝试次数
        self.readnum = random.randint(2, 2)     #初始化阅读次数
        #初始化阅读菜单
        self.ismenu1 = True
        self.ismenu2 = True
        self.ismenu3 = True
        self.ismenu4 = True
        self.ismenu5 = True

        return self.begin

    def begin(self):
        dr = self.driver
        dr.press_keycode(3)
        time.sleep(1)
        WebDriverWait(dr, 300).until(lambda d: d.find_element_by_name(self.appname)).click()
        time.sleep(10)
        #检测已进入app
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.ledo.fantasy.ledo:id/button_commonLogin_fragment_main"))
        self.begintime = "开始:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        time.sleep(1)
        #注册
        # WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.ledo.fantasy.ledo:id/button_commonLogin_fragment_main")).click()
        # time.sleep(1)
        # WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.ledo.fantasy.ledo:id/Button_userregister_login_common")).click()
        # time.sleep(1)
        return self.signup

    def signup(self):
        dr = self.driver
        liemail = ["@163.com", "@qq.com", '@126.com', '@sina.cn', '@souhu.com', '@outlook.com', "@qq.com",
                    "@qq.com", "@qq.com", "@qq.com", "@qq.com", "@qq.com", "@qq.com", "@qq.com", "@qq.com"]
        pwd_li = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                  "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                  "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                  "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                  "u", "v", "w", "x", "y", "z"]
        self.phone = str(random.randint(10000000, 9999999999))+choice(liemail)
        self.pwd = choice(pwd_li)+choice(pwd_li)+choice(pwd_li)+choice(pwd_li)+choice(pwd_li)+choice(pwd_li)
        try:
            #注册
            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.ledo.fantasy.ledo:id/button_commonLogin_fragment_main")).click()
            time.sleep(1)
            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.ledo.fantasy.ledo:id/Button_userregister_login_common")).click()
            time.sleep(1)
            edts = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.ledo.fantasy.ledo:id/EditText_phoneOrmail_register_phone"))
            #输入邮箱
            edts.send_keys(self.phone)
            time.sleep(1)
            #下一步
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.ledo.fantasy.ledo:id/Button_phoneOrmail_register_phone")).click()
            time.sleep(5)

            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.ledo.fantasy.ledo:id/Button_phoneOrmail_register_phone")).click()
            time.sleep(5)
            edts = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.ledo.fantasy.ledo:id/EditText_phoneOrmail_register_phone"))
            #输入密码
            edts.send_keys(self.pwd)
            time.sleep(1)
            edts = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.ledo.fantasy.ledo:id/EditText_confirmpassword_register_mail"))
            #再次输入密码
            edts.send_keys(self.pwd)
            time.sleep(1)
            #点击注册按钮
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.ledo.fantasy.ledo:id/Button_register_register_mail")).click()
            time.sleep(10)
            #记录帐号密码
            try:
                with open('/sdcard/1/user%s.log' % self.appname_en, 'a') as f:
                    f.write('\nimei:%s,%s,%s (time %s.%s  %s:%s:%s)' % (self.imei, self.phone, self.pwd, time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec))
            except:
                with open('D:/brush/slave/scripts/doc/user%s.log' % self.appname_en, 'a') as f:
                    f.write('\nimei:%s,%s,%s (time %s.%s  %s:%s:%s)' % (self.imei, self.phone, self.pwd, time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec))
            time.sleep(1)
            return self.do
        except Exception as e:
            print("error in getPhone,try_count:%s" % self.try_count)
            self.try_count += 1
            if self.try_count > 5:
                return self.exit
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            try:
                WebDriverWait(dr, 2).until(lambda d: d.find_element_by_id("android:id/button2")).click()
                time.sleep(5)
                dr.tap(600, 440)
                time.sleep(1)
            except TimeoutException:
                pass
            return self.signup

    def do(self):
        dr = self.driver
        try:
            #进入游戏
            dr.tap(666, 566)
            time.sleep(10)
            #选职业
            dr.tap(1170, choice([125, 246, 388, 500]))
            time.sleep(5)
            #进入游戏
            dr.tap(1170, 655)
            time.sleep(random.randint(10, 15))
            #退出游戏
            dr.press_keycode(4)
            time.sleep(1)
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("android:id/button1")).click()
            time.sleep(1)
        except TimeoutException:
            print("查找菜单出错")
            return self.exception_returnapp()
        print("阅览完毕")
        return self.ends

    def ends(self):
        #记录时间
        self.endstime = "结束:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        print(self.begintime)
        print(self.endstime)
        time.sleep(2)
        try:
            with open('/sdcard/1/time%s.log' % self.appname_en, 'a') as f:
                f.write('\n激活 %s.%s, %s, %s, count:%s' % (time.localtime().tm_mon, time.localtime().tm_mday, self.begintime, self.endstime, self.runnum))
        except:
            pass
        time.sleep(3)
        #效率控制
        # st = [1200, 1200, 1200, 1200, 1200, 1200, 180, 120, 40, 20, 10, 10,
        #       10, 20, 20, 20, 10, 10, 5, 0, 0, 0, 0, 0]
        #
        # print("现在时间是%s:%s,脚本将在%s秒后继续执行" % (time.localtime().tm_hour, time.localtime().tm_min, st[time.localtime().tm_hour-1]))
        # time.sleep(st[time.localtime().tm_hour-1])

        return self.exit

    def get_filemessage(self, filename):
        if os.path.exists("D:/brush/slave/scripts/doc/%s" % filename):
            with open("D:/brush/slave/scripts/doc/%s" % filename, 'r', encoding='utf-8') as f:
                 strname = f.readlines()
        elif os.path.exists("/sdcard/1/%s" % filename):
            with open("/sdcard/1/%s" % filename, 'r', encoding='utf-8') as f:
                 strname = f.readlines()
        else:
            strname = ""
        time.sleep(1)
        return strname[random.randint(0, strname.__len__()-1)].strip()

    def swipes(self, x1, y1, x2, y2, swipe_num=1, swipe_time_a=1, swipe_time_b=1):
        dr = self.driver
        print("swipenum:%s" % swipe_num)
        for x in range(swipe_num):
            dr.swipe(x1, y1, x2, y2)
            time.sleep(random.randint(swipe_time_a, swipe_time_b))

    def select_one_by_id(self, find_id, find_time=30, find_min=0, find_max=0):
        selectone = WebDriverWait(self.driver, find_time).until(lambda d: d.find_elements_by_id(find_id))
        if find_max == 0:
            selectone[random.randint(find_min, selectone.__len__()-1)].click()
        else:
            selectone[random.randint(find_min, find_max)].click()

    def exception_returnapp(self):
        dr = self.driver
        print("try_count:%s" % self.try_count)
        self.try_count += 1
        if self.try_count > 5:
            return self.exit
        dr.press_keycode(4)
        time.sleep(1)
        dr.press_keycode(4)
        time.sleep(1)
        try:
            WebDriverWait(dr, 2).until(lambda d: d.find_element_by_id("android:id/button2")).click()
        except TimeoutException:
            pass
        time.sleep(5)
        return self.do


class Machinex2(Machine):
    def __init__(self, driver):
        super(Machinex2, self).__init__(self.initdata)
        self.driver = driver
        self.appname = "永恒之歌"       #app名字
        self.appname_en = "yongheng"     #记录文件用缩写英文名
        self.imei = None        #imei
        self.remain_day = None      #留存天数

    def initdata(self):
        self.begintime = None
        self.endstime = None
        self.try_count = 0      #初始化出错尝试次数

        return self.begin

    def begin(self):
        dr = self.driver
        dr.press_keycode(3)
        time.sleep(1)
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name(self.appname)).click()
        time.sleep(10)
        #检测已进入app
        WebDriverWait(dr, 300).until(lambda d: d.find_element_by_id("com.ledo.fantasy.ledo:id/button_commonLogin_fragment_main"))
        self.begintime = "开始:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        time.sleep(1)
        return self.login

    def login(self):
        dr = self.driver
        try:
            with open('/sdcard/1/user%s.log' % self.appname_en, 'r') as f:
                selectuser = f.read()
        except:
            with open('D:/brush/slave/scripts/doc/user%s.log' % self.appname_en, 'r') as f:
                selectuser = f.read()
        user = re.search(r'imei:%s,([0-9a-z\@\.]+)' % self.imei, selectuser)
        pwd = re.search(r'imei:%s,[0-9a-z\@\.]+,([0-9a-z]+)' % self.imei, selectuser)
        if user and pwd:
            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.ledo.fantasy.ledo:id/button_commonLogin_fragment_main")).click()
            time.sleep(1)
            edit = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.ledo.fantasy.ledo:id/EditText_username_login_common"))
            edit.send_keys(str(user.group(1)))
            time.sleep(1)
            edit = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.ledo.fantasy.ledo:id/EditText_password_login_common"))
            edit.send_keys(str(pwd.group(1)))
            time.sleep(1)
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.ledo.fantasy.ledo:id/Button_login_login_common")).click()
            time.sleep(1)
        time.sleep(random.randint(5, 10))
        return self.do

    def do(self):
        dr = self.driver
        try:
            #进入游戏
            dr.tap(666, 566)
            time.sleep(10)
            #选职业
            # dr.tap(1170, choice([125, 246, 388, 500]))
            # time.sleep(5)
            #进入游戏
            dr.tap(1170, 655)
            time.sleep(random.randint(10, 15))
            #退出游戏
            dr.press_keycode(4)
            time.sleep(1)
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("android:id/button1")).click()
            time.sleep(1)
        except TimeoutException:
            print("查找菜单出错")
            return self.exception_returnapp()
        print("阅览完毕")
        return self.ends

    def ends(self):
        #记录时间
        self.endstime = "结束:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        print(self.begintime)
        print(self.endstime)
        time.sleep(2)
        try:
            with open('/sdcard/1/time%s2.log' % self.appname_en, 'a') as f:
                f.write('\n留存%s  %s.%s, %s, %s' % (self.remain_day, time.localtime().tm_mon, time.localtime().tm_mday, self.begintime, self.endstime))
        except:
            pass
        time.sleep(3)
        return self.exit

    def get_filemessage(self, filename):
        if os.path.exists("D:/brush/slave/scripts/doc/%s" % filename):
            with open("D:/brush/slave/scripts/doc/%s" % filename, 'r', encoding='utf-8') as f:
                 strname = f.readlines()
        elif os.path.exists("/sdcard/1/%s" % filename):
            with open("/sdcard/1/%s" % filename, 'r', encoding='utf-8') as f:
                 strname = f.readlines()
        else:
            strname = ""
        time.sleep(1)
        return strname[random.randint(0, strname.__len__()-1)].strip()

    def swipes(self, x1, y1, x2, y2, swipe_num=1, swipe_time_a=1, swipe_time_b=1):
        dr = self.driver
        print("swipenum:%s" % swipe_num)
        for x in range(swipe_num):
            dr.swipe(x1, y1, x2, y2)
            time.sleep(random.randint(swipe_time_a, swipe_time_b))

    def select_one_by_id(self, find_id, find_time=30, find_min=0, find_max=0):
        selectone = WebDriverWait(self.driver, find_time).until(lambda d: d.find_elements_by_id(find_id))
        if find_max == 0:
            selectone[random.randint(find_min, selectone.__len__()-1)].click()
        else:
            selectone[random.randint(find_min, find_max)].click()

    def exception_returnapp(self):
        dr = self.driver
        print("try_count:%s" % self.try_count)
        self.try_count += 1
        if self.try_count > 5:
            return self.exit
        dr.press_keycode(4)
        time.sleep(1)
        dr.press_keycode(4)
        time.sleep(1)
        try:
            WebDriverWait(dr, 2).until(lambda d: d.find_element_by_id("android:id/button2")).click()
        except TimeoutException:
            pass
        time.sleep(5)
        return self.do



if __name__ == "__main__":
    wd = webdriver.Remote()
    time.sleep(2)

