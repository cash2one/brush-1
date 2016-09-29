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

from jiema.jiumaSDK import Jiuma
from jiema.feimaSDK import Feima
from jiema.yamaSDK import Yama
from jiema.ailezanSDK import Ailezan
from jiema.jimaSDK import Jima
from jiema.shenhuaSDK import Shenhua
from jiema.yimaSDK import Yima


class Machinex(Machine):
    def __init__(self, driver, code_platform, fm_uname, fm_pwd):
        super(Machinex, self).__init__(self.initdata)
        self.driver = driver
        self.code_platform = code_platform      #接码平台
        self.code_user = fm_uname       #接码平台帐号
        self.code_pwd = fm_pwd      #接码平台密码
        self.appname = "平安普惠"       #app名字
        self.appname_en = "puhui"     #记录文件用缩写英文名
        self.imei = None
        self.runnum = None        #记录运行次数

    def initdata(self):
        self.phone = None
        self.pwd = None
        self.begintime = None
        self.endstime = None
        self.try_count = 0      #初始化出错尝试次数
        self.readnum = random.randint(2, 2)     #初始化阅读次数
        #选择初始化接码平台
        if self.code_platform == "feima":
            self.code = Feima(self.code_user, self.code_pwd, None)
        elif self.code_platform == "yama":
            self.code = Yama(self.code_user, self.code_pwd, None)
        elif self.code_platform == "yima":
            self.code = Yima(self.code_user, self.code_pwd, None)
        elif self.code_platform == "ailezan":
            self.code = Ailezan(self.code_user, self.code_pwd, 5191)
        elif self.code_platform == "jima":
            self.code = Jima(self.code_user, self.code_pwd, None)
        elif self.code_platform == "jiuma":
            self.code = Jiuma(self.code_user, self.code_pwd, None)
        elif self.code_platform == "shenhua":
            self.code = Shenhua(self.code_user, self.code_pwd, None)

        return self.login_code_platform()

    def login_code_platform(self):
        #登录接码平台
        print("login %s getcode ......" % self.code_platform)
        try:
            self.code.login()
        except Exception as e:
            print("error in login getcodeplatform,try_count:%s" % self.try_count)
            self.try_count += 1
            if self.try_count > 5:
                print("on try_count,exit")
                return self.exit
            return self.login_code_platform
        return self.down_app

    def down_app(self):
        dr = self.driver
        WebDriverWait(dr, 60).until(lambda d: d.find_element_by_name("Chrome")).click()
        time.sleep(1)
        WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.android.chrome:id/terms_accept")).click()
        time.sleep(1)
        #输入网址
        edts = WebDriverWait(dr, 60).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
        edts.click()
        edts.send_keys("http://www.10100000.com/m/mini/ppb/2016/07/iloan.html?utm_source=pxmwwzxrll-test7-m&utm_medium=cpm&utm_campaign=m0050-pp_xr08-iln&WT.mc_id=CXX-PXMWWZXRLL-TEST7M-CMM-M0050PP_XR08ILN&")
        time.sleep(1)
        dr.press_keycode(66)
        time.sleep(5)
        edts.click()
        time.sleep(0.5)
        self.phone = self.code.getPhone()
        for x in str(self.phone):
            dr.press_keycode((int(x)+7))
            time.sleep(0.5)
        #点击下载
        WebDriverWait(dr, 60).until(lambda d: d.find_element_by_xpath("//android.view.View[@content-desc='提交号码']")).click()
        time.sleep(1)
        WebDriverWait(dr, 60).until(lambda d: d.find_elements_by_xpath("//android.view.View[@content-desc='javascript:void(0);']"))[1].click()
        time.sleep(1)
        WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.android.chrome:id/button_primary")).click()
        time.sleep(1)
        WebDriverWait(dr, 300).until(lambda d: d.find_element_by_id("com.android.chrome:id/snackbar_button")).click()
        time.sleep(1
                   )
        #检测下载完成开始安装
        WebDriverWait(dr, 60).until(lambda d: d.find_element_by_name("安装")).click()
        time.sleep(1)
        #检测安装完成打开
        WebDriverWait(dr, 60).until(lambda d: d.find_element_by_name("打开")).click()
        time.sleep(1)
        return self.begin

    def begin(self):
        dr = self.driver
        #检测已进入app
        WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.paem:id/tv_user_login_or_regist"))
        self.begintime = "开始:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        time.sleep(1)
        return self.signup

    def signup(self):
        dr = self.driver
        pwd_li = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                  "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                  "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                  "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                  "u", "v", "w", "x", "y", "z"]
        pwd_num = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        pwd_en = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                  "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                  "u", "v", "w", "x", "y", "z"]
        self.pwd = choice(pwd_li)+choice(pwd_li)+choice(pwd_li)+choice(pwd_li)+choice(pwd_li)+choice(pwd_num)+choice(pwd_en)+choice(pwd_li)
        try:
            #进入注册页面
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.paem:id/tv_user_login_or_regist")).click()
            time.sleep(1)
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.paem:id/right_header_textview")).click()
            time.sleep(5)
            dr.tap(250, 200)
            time.sleep(1)
            #选择接码平台获取手机号码
            self.phone = self.code.getPhone(self.phone)
            edts = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_class_name("android.widget.EditText"))
            #输入手机号码
            edts[0].send_keys(self.phone)
            time.sleep(1)
            #点击获取验证码按钮
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_xpath("//android.view.View[@content-desc='获取验证码']")).click()
            time.sleep(5)
            #检测是否被注册
            try:
                WebDriverWait(dr, 10).until(lambda d: d.find_element_by_xpath("//android.view.View[@content-desc='取消']")).click()
                time.sleep(1)
                print("getMessage failed,try_count:%s" % self.try_count)
                #加黑号码
                self.code.addblackPhone(self.phone)
                self.try_count += 1
                if self.try_count > 5:
                    return self.exit
                WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.paem:id/back_btn")).click()
                time.sleep(1)
                WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.paem:id/back_btn")).click()
                time.sleep(1)
                #进入浏览器重新填写号码
                dr.press_keycode(82)
                time.sleep(2)
                WebDriverWait(dr, 2).until(lambda d: d.find_element_by_name("Chrome")).click()
                time.sleep(1)
                #更换号码
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.view.View[@content-desc='iloan.html?WT']")).click()
                time.sleep(10)
                # dr.press_keycode(4)
                # time.sleep(5)
                edts = WebDriverWait(dr, 60).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
                edts.click()
                for x in range(15):
                    dr.press_keycode(67)
                self.phone = self.code.getPhone()
                for x in str(self.phone):
                    dr.press_keycode((int(x)+7))
                    time.sleep(0.5)
                WebDriverWait(dr, 60).until(lambda d: d.find_element_by_xpath("//android.view.View[@content-desc='提交号码']")).click()
                time.sleep(1)
                #检测更换完毕
                WebDriverWait(dr, 60).until(lambda d: d.find_element_by_xpath("//android.view.View[@content-desc='javascript:void(0);']"))
                time.sleep(1)
                #返回app
                dr.press_keycode(82)
                time.sleep(2)
                WebDriverWait(dr, 2).until(lambda d: d.find_element_by_name(self.appname)).click()
                time.sleep(1)
                return self.signup
            except TimeoutException:
                pass
            #输入密码
            edts[2].send_keys(self.pwd)
            time.sleep(1)
            #选择接码平台获取验证码
            #您在注册平安普惠手机应用，验证码6912428，2分钟内有效。【中国平安】(来自95511)
            regrex = r'验证码(\d+)'
            captcha = self.code.waitForMessage(regrex, self.phone)
            if captcha is None:
                print("getMessage failed,try_count:%s" % self.try_count)
                #释放号码
                self.code.releasePhone(self.phone)
                self.try_count += 1
                if self.try_count > 5:
                    return self.exit
                WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.paem:id/back_btn")).click()
                time.sleep(1)
                WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.paem:id/back_btn")).click()
                time.sleep(1)
                #进入浏览器重新填写号码
                dr.press_keycode(82)
                time.sleep(2)
                WebDriverWait(dr, 2).until(lambda d: d.find_element_by_name("Chrome")).click()
                time.sleep(1)
                #更换号码
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_xpath("//android.view.View[@content-desc='iloan.html?WT']"))
                time.sleep(1)
                dr.press_keycode(4)
                time.sleep(1)
                edts = WebDriverWait(dr, 60).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
                edts.click()
                for x in range(15):
                    dr.press_keycode(67)
                self.phone = self.code.getPhone()
                for x in str(self.phone):
                    dr.press_keycode((int(x)+7))
                    time.sleep(0.5)
                WebDriverWait(dr, 60).until(lambda d: d.find_element_by_xpath("//android.view.View[@content-desc='提交号码']")).click()
                time.sleep(1)
                #检测更换完毕
                WebDriverWait(dr, 60).until(lambda d: d.find_element_by_xpath("//android.view.View[@content-desc='javascript:void(0);']"))
                time.sleep(1)
                #返回app
                dr.press_keycode(82)
                time.sleep(2)
                WebDriverWait(dr, 2).until(lambda d: d.find_element_by_name(self.appname)).click()
                time.sleep(1)
                return self.signup
            #输入验证码
            edts[1].send_keys(captcha)
            time.sleep(1)
            #点击完成按钮按钮
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_xpath("//android.view.View[@content-desc='注册']")).click()
            time.sleep(5)
            #检测注册成功进入下一步
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_xpath("//android.view.View[@content-desc='确定']")).click()
            time.sleep(1)
            #实名认证
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_xpath("//android.view.View[@content-desc='暂时跳过>']")).click()
            time.sleep(1)
            #设置手势密码
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.paem:id/right_header_textview")).click()
            time.sleep(1)
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.paem:id/right_header_BtnAndTxt_layout2"))
            time.sleep(1)
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
            time.sleep(2)
            return self.signup

    def do(self):
        dr = self.driver
        try:
            #签到
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.paem:id/right_header_BtnAndTxt_layout2")).click()
            time.sleep(1)
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_xpath("//android.view.View[@content-desc='平安易贷 - 签到']"))
            time.sleep(10)
            dr.tap(350, 600)
            time.sleep(5)
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_xpath("//android.view.View[@content-desc='关闭']")).click()
            time.sleep(5)
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.paem:id/back_btn")).click()
            time.sleep(5)
            #设置
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_xpath("//android.view.View[@content-desc='%s']" % choice(["借钱", "花钱", "赚钱"]))).click()
            time.sleep(random.randint(15, 30))
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.paem:id/back_btn")).click()
            time.sleep(5)
            if random.randint(0, 1):
                WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.paem:id/back_btn")).click()
                time.sleep(random.randint(10, 15))
                WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.paem:id/back_btn")).click()
                time.sleep(5)
        except TimeoutException:
            print("查找菜单出错")
            return self.exception_returnapp()
        print("阅览完毕")
        return self.ends

    def ends(self):
        dr = self.driver
        #二次打开
        for x in range(random.randint(0, 0)):
            dr.press_keycode(3)
            time.sleep(1)
            dr.press_keycode(3)
            time.sleep(30)
            WebDriverWait(dr, 2).until(lambda d: d.find_element_by_name(self.appname)).click()
            time.sleep(1)
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

    #指定文档中随机获取数据
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

    #随机滑动
    def swipes(self, x1, y1, x2, y2, swipe_num=1, swipe_time_min=1, swipe_time_max=1):
        dr = self.driver
        print("swipenum:%s" % swipe_num)
        for x in range(swipe_num):
            dr.swipe(x1, y1, x2, y2)
            time.sleep(random.randint(swipe_time_min, swipe_time_max))

    #随机选择
    def select_one_by_id(self, find_id, find_time=30, find_min=0, find_max=0):
        selectone = WebDriverWait(self.driver, find_time).until(lambda d: d.find_elements_by_id(find_id))
        if find_max == 0:
            find_max = selectone.__len__()-1
        selectone[random.randint(find_min, find_max)].click()

    #出错处理
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
        dr.press_keycode(82)
        time.sleep(2)
        try:
            WebDriverWait(dr, 2).until(lambda d: d.find_element_by_name(self.appname)).click()
        except TimeoutException:
            dr.press_keycode(4)
        time.sleep(5)
        return self.do


class Machinex2(Machine):
    def __init__(self, driver):
        super(Machinex2, self).__init__(self.initdata)
        self.driver = driver
        self.appname = "平安普惠"       #app名字
        self.appname_en = "puhui"     #记录文件用缩写英文名
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
        try:
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("文件管理"))
            time.sleep(1)
            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("安装包"))
            time.sleep(1)
        except TimeoutException:
            pass
        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("PAYiDai_WXTEJY.apk"))
        time.sleep(1)
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("安装")).click()
        time.sleep(1)
        WebDriverWait(dr, 60).until(lambda d: d.find_element_by_name("打开")).click()
        time.sleep(1)
        #检测已进入app
        WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.paem:id/tv_user_login_or_regist"))
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
        user = re.search(r'imei:%s,(\d+)' % self.imei, selectuser)
        pwd = re.search(r'imei:%s,\d+,([0-9a-z]+)' % self.imei, selectuser)
        if user and pwd:
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.paem:id/tv_user_login_or_regist")).click()
            time.sleep(1)
            edit = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_class_name("android.widget.EditText"))
            edit[0].send_keys(str(user.group(1)))
            time.sleep(1)
            edit[1].send_keys(str(pwd.group(1)))
            time.sleep(1)
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.paem:id/btn_login")).click()
            time.sleep(5)
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.paem:id/right_header_textview")).click()
            time.sleep(5)
            return self.do
        time.sleep(5)
        return self.ends

    def do(self):
        dr = self.driver
        try:
            #签到
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.paem:id/right_header_BtnAndTxt_layout2")).click()
            time.sleep(1)
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_xpath("//android.view.View[@content-desc='平安易贷 - 签到']"))
            time.sleep(10)
            dr.tap(350, 600)
            time.sleep(5)
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_xpath("//android.view.View[@content-desc='关闭']")).click()
            time.sleep(5)
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.paem:id/back_btn")).click()
            time.sleep(5)
            #设置
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_xpath("//android.view.View[@content-desc='%s']" % choice(["借钱", "花钱", "赚钱"]))).click()
            time.sleep(random.randint(15, 30))
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.paem:id/back_btn")).click()
            time.sleep(5)
            if random.randint(0, 1):
                WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.paem:id/back_btn")).click()
                time.sleep(random.randint(10, 15))
                WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.paem:id/back_btn")).click()
                time.sleep(5)
        except TimeoutException:
            print("查找菜单出错")
            return self.exception_returnapp()
        print("阅览完毕")
        return self.ends

    def ends(self):
        dr = self.driver
        #二次打开
        for x in range(random.randint(0, 0)):
            dr.press_keycode(3)
            time.sleep(1)
            dr.press_keycode(3)
            time.sleep(30)
            WebDriverWait(dr, 2).until(lambda d: d.find_element_by_name(self.appname)).click()
            time.sleep(1)
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

    #指定文档中随机获取数据
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

    #随机滑动
    def swipes(self, x1, y1, x2, y2, swipe_num=1, swipe_time_min=1, swipe_time_max=1):
        dr = self.driver
        print("swipenum:%s" % swipe_num)
        for x in range(swipe_num):
            dr.swipe(x1, y1, x2, y2)
            time.sleep(random.randint(swipe_time_min, swipe_time_max))

    #随机选择
    def select_one_by_id(self, find_id, find_time=30, find_min=0, find_max=0):
        selectone = WebDriverWait(self.driver, find_time).until(lambda d: d.find_elements_by_id(find_id))
        if find_max == 0:
            find_max = selectone.__len__()-1
        selectone[random.randint(find_min, find_max)].click()

    #出错处理
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
        dr.press_keycode(82)
        time.sleep(2)
        try:
            WebDriverWait(dr, 2).until(lambda d: d.find_element_by_name(self.appname)).click()
        except TimeoutException:
            dr.press_keycode(4)
        time.sleep(5)
        return self.do



if __name__ == "__main__":
    wd = webdriver.Remote()
    time.sleep(2)

