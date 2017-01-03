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

try:
    from util import screenshot, run_qpy2_script
except ImportError:
    screenshot = lambda: 1
    run_qpy2_script = lambda x: None


class Machinex(Machine):
    def __init__(self, driver):
        super(Machinex, self).__init__(self.initdata)
        self.driver = driver
        self.appname = "秒拍"       #app名字
        self.appname_en = "miaopai"     #记录文件用缩写英文名
        self.imei = None
        self.runnum = None        #记录运行次数

    def initdata(self):
        self.phone = None
        self.pwd = None
        self.begintime = None
        self.endstime = None
        self.try_count = 0      #初始化出错尝试次数
        self.readnum = random.randint(2, 3)     #初始化阅读次数
        #初始化阅读菜单
        self.ismenu1 = True
        self.ismenu2 = True
        self.ismenu3 = True
        self.ismenu4 = True
        self.ismenu5 = True
        self.issign = False
        return self.begin

    def begin(self):
        dr = self.driver
        dr.press_keycode(3)
        time.sleep(1)
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name(self.appname)).click()
        time.sleep(10)
        #检测已进入app
        WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/bottom_record_top"))
        self.begintime = "开始:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        time.sleep(1)
        #注册率
        sign_rate = random.randint(1, 10000)
        if sign_rate <= 3000:
            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/bottom_my_lay")).click()
            time.sleep(1)
            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/no_login_views")).click()
            time.sleep(1)
            return self.signup

        return self.do

    def signup(self):
        dr = self.driver
        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/login_qq_button")).click()
        time.sleep(1)
        #进入QQ登录界面
        WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.tencent.mobileqq:id/name"))
        time.sleep(1)
        try:
            with open('/sdcard/1/qq.txt', 'r', encoding='utf-8') as f:
                tfile = "/sdcard/1/qq.txt"
                strqq = f.read()
        except:
            with open('D:/brush/slave/scripts/doc/qq.txt', 'r', encoding='utf-8') as f:
                tfile = "D:/brush/slave/scripts/doc/qq.txt"
                strqq = f.read()
        match = re.search(r'notuse,(\d+,[0-9a-zA-Z\_\@]+)', strqq)
        if match:
            self.phone = re.search(r'notuse,(\d+)', match.group(0)).group(1)
            self.pwd = re.search(r'notuse,\d+,([0-9a-zA-Z\_\@]+)', match.group(0)).group(1)
            #修改标志QQ已使用
            try:
                lines = open(tfile, 'r').readlines()
                flen = len(lines)
                for i in range(flen):
                    if match.group(0) in lines[i]:
                        usetime = '(time %s.%s  %s:%s:%s)' % (time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
                        modify = 'use,' + match.group(1) + " " + usetime
                        lines[i] = lines[i].replace(match.group(0), modify)
                        break
                open(tfile, 'w').writelines(lines)
            except Exception as e:
                print(e)
        else:
            #帐号已用完
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            return self.do
        edit = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_class_name("android.widget.EditText"))
        edit[0].send_keys(self.phone)
        time.sleep(1)
        edit[1].send_keys(self.pwd)
        time.sleep(1)
        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("登 录")).click()
        time.sleep(5)
        try:
            for _ in range(5):
                WebDriverWait(dr, 60).until(lambda d: d.find_element_by_name("看不清？换一张"))
                time.sleep(5)
                screenshot("/sdcard/screenshot.png")
                run_qpy2_script("get_captchaimg_qqdongman.py")
                imgcaptcha = self.uuwise()
                if imgcaptcha is None:
                    print("getimgcaptcha failed")
                    self.try_count += 1
                    if self.try_count > 5:
                        self.try_count = 0
                        return self.exit
                    dr.press_keycode(4)
                    time.sleep(1)
                    dr.press_keycode(4)
                    time.sleep(1)
                    return self.signup
                dr.press_keycode(4)
                time.sleep(5)
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("登 录")).click()
                time.sleep(1)
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("看不清？换一张"))
                time.sleep(1)
                edts = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
                edts.send_keys(imgcaptcha)
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.tencent.mobileqq:id/ivTitleBtnRightText")).click()
                time.sleep(5)
                try:
                    #图片验证码是否正确
                    WebDriverWait(dr, 10).until(lambda d: d.find_element_by_name("看不清？换一张"))
                    time.sleep(1)
                except TimeoutException:
                    break
            #注册成功页面检测
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_name("授权并登录")).click()
            time.sleep(1)
            WebDriverWait(dr, 120).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/titleLeft")).click()
            time.sleep(1)
            #记录帐号密码
            try:
                with open('/sdcard/1/user%s.log' % self.appname_en, 'a') as f:
                    f.write('\nimei:%s,%s,%s (time %s.%s  %s:%s:%s)' % (self.imei, self.phone, self.pwd, time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec))
            except:
                with open('D:/brush/slave/scripts/doc/user%s.log' % self.appname_en, 'a') as f:
                    f.write('\nimei:%s,%s,%s (time %s.%s  %s:%s:%s)' % (self.imei, self.phone, self.pwd, time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec))
            time.sleep(1)
            self.issign = True
        except TimeoutException:
            try:
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("授权并登录")).click()
                time.sleep(1)
                WebDriverWait(dr, 120).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/titleLeft")).click()
                time.sleep(1)
                #记录帐号密码
                try:
                    with open('/sdcard/1/user%s.log' % self.appname_en, 'a') as f:
                        f.write('\nimei:%s,%s,%s (time %s.%s  %s:%s:%s)' % (self.imei, self.phone, self.pwd, time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec))
                except:
                    with open('D:/brush/slave/scripts/doc/user%s.log' % self.appname_en, 'a') as f:
                        f.write('\nimei:%s,%s,%s (time %s.%s  %s:%s:%s)' % (self.imei, self.phone, self.pwd, time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec))
                time.sleep(1)
                self.issign = True
                return self.do
            except TimeoutException:
                pass
            #修改标志QQ使用失败
            try:
                lines = open(tfile, 'r').readlines()
                flen = len(lines)
                for i in range(flen):
                    if modify in lines[i]:
                        lines[i] = lines[i].replace(modify, modify + ',false')
                        break
                open(tfile, 'w').writelines(lines)
            except Exception as e:
                print(e)
            screenshot("/sdcard/error/%s.png" % (str(time.localtime().tm_mon) + str(time.localtime().tm_mday) + str(time.localtime().tm_hour) + str(time.localtime().tm_min) + str(time.localtime().tm_sec)))
            time.sleep(5)
            self.try_count += 1
            if self.try_count > 5:
                self.try_count = 0
                return self.exit
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            return self.signup
        return self.do

    def do(self):
        dr = self.driver
        try:
            while self.readnum:
                print("剩下阅读次数:%s" % self.readnum)
                random_read = random.randint(0, 4)
                if random_read == 0:
                    if self.ismenu1:
                        print("goto menu1")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/bottom_feed_lay")).click()
                        time.sleep(5)
                        return self.menu1
                    return self.do
                elif random_read == 1:
                    if self.ismenu2:
                        print("goto menu2")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/bottom_friend_lay")).click()
                        time.sleep(5)
                        return self.menu2
                    return self.do
                elif random_read == 2:
                    if self.ismenu3:
                        print("goto menu3")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/bottom_record_top")).click()
                        time.sleep(5)
                        return self.menu3
                    return self.do
                elif random_read == 3:
                    if self.ismenu4:
                        print("goto menu4")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/bottom_message_lay")).click()
                        time.sleep(5)
                        return self.menu4
                    return self.do
                else:
                    if self.ismenu5:
                        print("goto menu5")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/bottom_my_lay")).click()
                        time.sleep(5)
                        return self.menu5
                    return self.do
        except TimeoutException:
            print("查找菜单出错")
            return self.exception_returnapp()
        print("阅览完毕")
        dr.press_keycode(4)
        time.sleep(1)
        dr.press_keycode(4)
        time.sleep(1)
        dr.press_keycode(4)
        time.sleep(1)
        return self.ends

    def menu1(self):
        dr = self.driver
        try:
            for _ in range(random.randint(1, 3)):
                self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(1, 3), 2, 5)
                self.select_one_by_id("com.yixia.videoeditor:id/des")
                time.sleep(random.randint(10, 15))
                #关注
                if not random.randint(0, 4):
                    try:
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/relation")).click()
                        time.sleep(1)
                        WebDriverWait(dr, 2).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/dialog_left_buton")).click()
                        time.sleep(1)
                    except TimeoutException:
                        pass
                time.sleep(random.randint(10, 15))
                #赞
                if not random.randint(0, 4):
                    try:
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/video_good_count_layout")).click()
                        time.sleep(1)
                    except TimeoutException:
                        pass
                time.sleep(random.randint(10, 15))
                #评论
                if not random.randint(0, 19) and self.issign:
                    try:
                        contentnum = WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/feed_video_comment_count"))
                        if int(contentnum.text) > 10:
                            contentnum.click()
                            time.sleep(5)
                            self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(2, 10), 2, 2)
                            time.sleep(2)
                            contenttext = WebDriverWait(dr, 30).until(lambda d: d.find_elements_by_id("com.yixia.videoeditor:id/comment_content"))
                            comtext = contenttext[random.randint(0, contenttext.__len__()-1)].text
                            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/comment_input")).click()
                            time.sleep(1)
                            edit = WebDriverWait(dr, 30).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
                            edit.send_keys(comtext)
                            time.sleep(1)
                            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/send_text")).click()
                            time.sleep(1)
                            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/detail_title_back")).click()
                            time.sleep(1)
                    except TimeoutException:
                        pass
                time.sleep(random.randint(10, 15))
                dr.press_keycode(4)
                time.sleep(1)
            self.readnum -= 1
            self.ismenu1 = False
        except Exception as e:
            print("error in menu1")
            return self.exception_returnapp()
        return self.do

    def menu2(self):
        dr = self.driver
        try:
            for i in range(random.randint(1, 3)):
                dr.swipe(300, random.randint(800, 1000), 300, random.randint(300, 600))
                time.sleep(random.randint(10, 15))
                #关注
                if not random.randint(0, 4):
                    try:
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/relation")).click()
                        time.sleep(1)
                        WebDriverWait(dr, 2).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/dialog_left_buton")).click()
                        time.sleep(1)
                    except TimeoutException:
                        pass
                time.sleep(random.randint(10, 15))
                #赞
                if not random.randint(0, 4):
                    try:
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/video_good_count_layout")).click()
                        time.sleep(1)
                    except TimeoutException:
                        pass
                time.sleep(random.randint(10, 15))
                #评论
                if not random.randint(0, 19) and self.issign:
                    try:
                        contentnum = WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/feed_video_comment_count"))
                        if int(contentnum.text) > 10:
                            contentnum.click()
                            time.sleep(5)
                            self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(2, 10), 2, 2)
                            time.sleep(2)
                            contenttext = WebDriverWait(dr, 30).until(lambda d: d.find_elements_by_id("com.yixia.videoeditor:id/comment_content"))
                            comtext = contenttext[random.randint(0, contenttext.__len__()-1)].text
                            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/comment_input")).click()
                            time.sleep(1)
                            edit = WebDriverWait(dr, 30).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
                            edit.send_keys(comtext)
                            time.sleep(1)
                            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/send_text")).click()
                            time.sleep(1)
                            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/detail_title_back")).click()
                            time.sleep(1)
                    except TimeoutException:
                        pass
                time.sleep(random.randint(10, 15))
            self.readnum -= 1
            self.ismenu2 = False
        except Exception as e:
            print("error in menu2")
            return self.exception_returnapp()
        return self.do

    def menu3(self):
        dr = self.driver
        try:
            dr.press_keycode(4)
            time.sleep(1)
            self.ismenu3 = False
        except Exception as e:
            print("error in menu3")
            return self.exception_returnapp()
        return self.do

    def menu4(self):
        dr = self.driver
        try:
            self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(1, 3), 2, 5)
            self.select_one_by_id("com.yixia.videoeditor:id/discovery_topic_title")
            time.sleep(random.randint(5, 10))
            for _ in range(random.randint(1, 3)):
                self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(0, 2), 2, 5)
                self.select_one_by_id("com.yixia.videoeditor:id/des")
                time.sleep(random.randint(10, 15))
                #关注
                if not random.randint(0, 4):
                    try:
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/relation")).click()
                        time.sleep(1)
                        WebDriverWait(dr, 2).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/dialog_left_buton")).click()
                        time.sleep(1)
                    except TimeoutException:
                        pass
                time.sleep(random.randint(10, 15))
                #赞
                if not random.randint(0, 4):
                    try:
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/video_good_count_layout")).click()
                        time.sleep(1)
                    except TimeoutException:
                        pass
                time.sleep(random.randint(10, 15))
                #评论
                if not random.randint(0, 19) and self.issign:
                    try:
                        contentnum = WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/feed_video_comment_count"))
                        if int(contentnum.text) > 10:
                            contentnum.click()
                            time.sleep(5)
                            self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(2, 10), 2, 2)
                            time.sleep(2)
                            contenttext = WebDriverWait(dr, 30).until(lambda d: d.find_elements_by_id("com.yixia.videoeditor:id/comment_content"))
                            comtext = contenttext[random.randint(0, contenttext.__len__()-1)].text
                            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/comment_input")).click()
                            time.sleep(1)
                            edit = WebDriverWait(dr, 30).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
                            edit.send_keys(comtext)
                            time.sleep(1)
                            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/send_text")).click()
                            time.sleep(1)
                            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/detail_title_back")).click()
                            time.sleep(1)
                    except TimeoutException:
                        pass
                time.sleep(random.randint(10, 15))
                dr.press_keycode(4)
                time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            self.readnum -= 1
            self.ismenu4 = False
        except Exception as e:
            print("error in menu4")
            return self.exception_returnapp()
        return self.do

    def menu5(self):
        dr = self.driver
        try:
            self.ismenu5 = False
        except Exception as e:
            print("error in menu5")
            return self.exception_returnapp()
        return self.do

    def ends(self):
        dr = self.driver
        #二次打开
        for x in range(random.randint(0, 1)):
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
        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name(self.appname)).click()
        return captcha

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
        self.appname = "秒拍"       #app名字
        self.appname_en = "miaopai"     #记录文件用缩写英文名
        self.imei = None        #imei
        self.remain_day = None      #留存天数

    def initdata(self):
        self.begintime = None
        self.endstime = None
        self.try_count = 0      #初始化出错尝试次数
        self.readnum = random.randint(1, 1)     #初始化阅读次数
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
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name(self.appname)).click()
        time.sleep(10)
        #检测已进入app
        WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/bottom_record_top"))
        self.begintime = "开始:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        time.sleep(5)
        return self.do

    def do(self):
        dr = self.driver
        try:
            while self.readnum:
                print("剩下阅读次数:%s" % self.readnum)
                random_read = random.randint(0, 4)
                if random_read == 0:
                    if self.ismenu1:
                        print("goto menu1")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/bottom_feed_lay")).click()
                        time.sleep(5)
                        return self.menu1
                    return self.do
                elif random_read == 1:
                    if self.ismenu2:
                        print("goto menu2")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/bottom_friend_lay")).click()
                        time.sleep(5)
                        return self.menu2
                    return self.do
                elif random_read == 2:
                    if self.ismenu3:
                        print("goto menu3")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/bottom_record_top")).click()
                        time.sleep(5)
                        return self.menu3
                    return self.do
                elif random_read == 3:
                    if self.ismenu4:
                        print("goto menu4")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/bottom_message_lay")).click()
                        time.sleep(5)
                        return self.menu4
                    return self.do
                else:
                    if self.ismenu5:
                        print("goto menu5")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/bottom_my_lay")).click()
                        time.sleep(5)
                        return self.menu5
                    return self.do
        except TimeoutException:
            print("查找菜单出错")
            return self.exception_returnapp()
        print("阅览完毕")
        dr.press_keycode(4)
        time.sleep(1)
        dr.press_keycode(4)
        time.sleep(1)
        dr.press_keycode(4)
        time.sleep(1)
        return self.ends

    def menu1(self):
        dr = self.driver
        try:
            for _ in range(random.randint(1, 2)):
                self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(1, 3), 2, 5)
                self.select_one_by_id("com.yixia.videoeditor:id/des")
                time.sleep(random.randint(15, 20))
                #关注
                if not random.randint(0, 4):
                    try:
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/relation")).click()
                        time.sleep(1)
                        WebDriverWait(dr, 2).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/dialog_left_buton")).click()
                        time.sleep(1)
                    except TimeoutException:
                        pass
                time.sleep(random.randint(15, 20))
                #赞
                if not random.randint(0, 4):
                    try:
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/video_good_count_layout")).click()
                        time.sleep(1)
                    except TimeoutException:
                        pass
                time.sleep(random.randint(15, 20))
                dr.press_keycode(4)
                time.sleep(1)
            self.readnum -= 1
            self.ismenu1 = False
        except Exception as e:
            print("error in menu1")
            return self.exception_returnapp()
        return self.do

    def menu2(self):
        dr = self.driver
        try:
            for i in range(random.randint(1, 2)):
                dr.swipe(300, random.randint(800, 1000), 300, random.randint(300, 600))
                time.sleep(random.randint(15, 20))
                #关注
                if not random.randint(0, 4):
                    try:
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/relation")).click()
                        time.sleep(1)
                        WebDriverWait(dr, 2).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/dialog_left_buton")).click()
                        time.sleep(1)
                    except TimeoutException:
                        pass
                time.sleep(random.randint(15, 20))
                #赞
                if not random.randint(0, 4):
                    try:
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/video_good_count_layout")).click()
                        time.sleep(1)
                    except TimeoutException:
                        pass
                time.sleep(random.randint(15, 20))
            self.readnum -= 1
            self.ismenu2 = False
        except Exception as e:
            print("error in menu2")
            return self.exception_returnapp()
        return self.do

    def menu3(self):
        dr = self.driver
        try:
            dr.press_keycode(4)
            time.sleep(1)
            self.ismenu3 = False
        except Exception as e:
            print("error in menu3")
            return self.exception_returnapp()
        return self.do

    def menu4(self):
        dr = self.driver
        try:
            self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(1, 3), 2, 5)
            self.select_one_by_id("com.yixia.videoeditor:id/discovery_topic_title")
            time.sleep(random.randint(5, 10))
            for _ in range(random.randint(1, 2)):
                self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(0, 2), 2, 5)
                self.select_one_by_id("com.yixia.videoeditor:id/des")
                time.sleep(random.randint(15, 20))
                #关注
                if not random.randint(0, 4):
                    try:
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/relation")).click()
                        time.sleep(1)
                        WebDriverWait(dr, 2).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/dialog_left_buton")).click()
                        time.sleep(1)
                    except TimeoutException:
                        pass
                time.sleep(random.randint(15, 20))
                #赞
                if not random.randint(0, 4):
                    try:
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.yixia.videoeditor:id/video_good_count_layout")).click()
                        time.sleep(1)
                    except TimeoutException:
                        pass
                time.sleep(random.randint(15, 20))
                dr.press_keycode(4)
                time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            self.readnum -= 1
            self.ismenu4 = False
        except Exception as e:
            print("error in menu4")
            return self.exception_returnapp()
        return self.do

    def menu5(self):
        dr = self.driver
        try:
            self.ismenu5 = False
        except Exception as e:
            print("error in menu5")
            return self.exception_returnapp()
        return self.do

    def ends(self):
        dr = self.driver
        #二次打开
        for x in range(random.randint(0, 1)):
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

