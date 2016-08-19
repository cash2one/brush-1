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

from jiema.jiumaSDK import Jiuma
from jiema.feimaSDK import Feima
from jiema.yamaSDK import Yama
from jiema.ailezanSDK import Ailezan
from jiema.jimaSDK import Jima
from jiema.shenhuaSDK import Shenhua
from jiema.yimaSDK import Yima

from random import choice


class Machine1video(Machine):
    def __init__(self, driver, code_platform, fm_uname, fm_pwd):
        super(Machine1video, self).__init__(self.initdata)
        self.driver = driver
        self.code_platform = code_platform      #接码平台
        self.code_user = fm_uname       #接码平台帐号
        self.code_pwd = fm_pwd      #接码平台密码
        self.appname = "第一视频"       #app名字
        self.appname_en = "1video"     #记录文件用缩写英文名
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
        self.ismenu5 = True
        #选择初始化接码平台
        if self.code_platform == "feima":
            self.code = Feima(self.code_user, self.code_pwd, 23144)
        elif self.code_platform == "yama":
            self.code = Yama(self.code_user, self.code_pwd, None)
        elif self.code_platform == "yima":
            self.code = Yima(self.code_user, self.code_pwd, None)
        elif self.code_platform == "ailezan":
            self.code = Ailezan(self.code_user, self.code_pwd, None)
        elif self.code_platform == "jima":
            self.code = Jima(self.code_user, self.code_pwd, None)
        elif self.code_platform == "jiuma":
            self.code = Jiuma(self.code_user, self.code_pwd, None)
        else:
            self.code = Shenhua(self.code_user, self.code_pwd, 45947)
        return self.begin

    def begin(self):
        dr = self.driver
        dr.press_keycode(3)
        time.sleep(1)
        dr.press_keycode(3)
        time.sleep(1)
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name(self.appname)).click()
        time.sleep(10)
        #检测已进入app
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.v1.video:id/iv_guide"))
        self.begintime = "开始:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        #新开软件翻页
        self.swipes(600, 300, 50, 300, 1, 2)
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.v1.video:id/v_go")).click()
        time.sleep(1)
        #选择喜欢的
        for x in range(random.randint(3, 5)):
            self.select_one_by_id("com.v1.video:id/item_guide_name")
            time.sleep(1)
        for x in range(20):
            try:
                WebDriverWait(dr, 2).until(lambda d: d.find_element_by_id("com.v1.video:id/guide_lay_btn_back")).click()
                time.sleep(1)
                break
            except TimeoutException:
                self.select_one_by_id("com.v1.video:id/item_guide_name")
                time.sleep(1)
        #注册率
        sign_rate = random.randint(1, 3000)
        if sign_rate <= 10000:
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.v1.video:id/lay_personal")).click()
            time.sleep(1)
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.v1.video:id/mylogin_user_head_img")).click()
            time.sleep(1)
            return self.login_code_platform

        return self.do

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
                self.try_count = 0
                return self.exit
            return self.login_code_platform
        return self.signup

    def signup(self):
        dr = self.driver
        signpwdli = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                     "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                     "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                     "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                     "u", "v", "w", "x", "y", "z"]
        self.pwd = choice(signpwdli)+choice(signpwdli)+choice(signpwdli)+choice(signpwdli)+choice(signpwdli)+choice(signpwdli)
        try:
            #进入注册页面
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.v1.video:id/textView_register")).click()
            time.sleep(1)
            #选择接码平台获取手机号码
            self.phone = self.code.getPhone()
            edts = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_class_name("android.widget.EditText"))
            #输入手机号码
            edts[0].send_keys(self.phone)
            time.sleep(1)
            #点击获取验证码按钮
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.v1.video:id/btn_verify")).click()
            time.sleep(5)
            #输入密码
            edts[2].send_keys(self.pwd)
            time.sleep(1)
            edts[3].send_keys(self.pwd)
            time.sleep(1)
            #选择接码平台获取验证码
            #欢迎注册第一视频网.您的手机验证码为:293703此验证码30分钟后失效!【第一视频】
            regrex = r'验证码为:(\d+)'
            captcha = self.code.waitForMessage(regrex, self.phone)
            if captcha is None:
                print("getMessage failed,try_count:%s" % self.try_count)
                #释放号码
                self.code.releasePhone(self.phone)
                self.try_count += 1
                if self.try_count > 5:
                    self.try_count = 0
                    return self.exit
                dr.press_keycode(4)
                time.sleep(1)
                return self.signup
            edts = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_class_name("android.widget.EditText"))
            #输入验证码
            edts[1].send_keys(captcha)
            time.sleep(1)
            #点击完成按钮按钮
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.v1.video:id/btn_register")).click()
            time.sleep(1)
            #检测注册成功进入下一步
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.v1.video:id/lay_personal"))
            #记录帐号密码
            try:
                with open('/sdcard/1/user%s.log' % self.appname_en, 'a') as f:
                    f.write('\nimei:%s,%s,%s (time %s:%s:%s)' % (self.imei, self.phone, self.pwd, time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour))
            except:
                with open('D:/brush/slave/scripts/doc/user%s.log' % self.appname_en, 'a') as f:
                    f.write('\nimei:%s,%s,%s (time %s:%s:%s)' % (self.imei, self.phone, self.pwd, time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour))
            time.sleep(1)
            return self.do
        except Exception as e:
            print("error in getPhone,try_count:%s" % self.try_count)
            self.try_count += 1
            if self.try_count > 5:
                self.try_count = 0
                return self.exit
            dr.press_keycode(4)
            time.sleep(2)
            return self.signup

    def do(self):
        dr = self.driver
        try:
            while self.readnum:
                print("剩下阅读次数:%s" % self.readnum)
                random_read = random.randint(0, 3)
                if random_read == 0:
                    if self.ismenu1:
                        print("goto menu1")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.v1.video:id/lay_home")).click()
                        time.sleep(5)
                        return self.menu1
                    return self.do
                elif random_read == 1:
                    if self.ismenu2:
                        print("goto menu2")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.v1.video:id/lay_subscribe")).click()
                        time.sleep(5)
                        return self.menu2
                    return self.do
                elif random_read == 2:
                    if self.ismenu3:
                        print("goto menu3")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.v1.video:id/lay_find")).click()
                        time.sleep(5)
                        return self.menu3
                    return self.do
                else:
                    if self.ismenu5:
                        print("goto menu5")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.v1.video:id/lay_personal")).click()
                        time.sleep(5)
                        return self.menu5
                    return self.do
        except TimeoutException:
            print("查找菜单出错")
            return self.exception_returnapp()
        print("阅览完毕")
        return self.ends

    def menu1(self):
        dr = self.driver
        try:
            issee = False
            # WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.v1.video:id/iv_add")).click()
            # time.sleep(1)
            # selectone = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id("com.v1.video:id/tv_item"))
            # selectnum = random.randint(0, selectone.__len__()-1)
            # readtext = selectone[selectnum].text
            # selectone[selectnum].click()
            # time.sleep(random.randint(5, 10))
            # self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(1, 3), random.randint(2, 5))
            # if readtext == "头条":
            for i in range(5):
                dr.swipe(300, random.randint(800, 1000), 300, random.randint(400, 600))
                time.sleep(1)
                selectvideo = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id("com.v1.video:id/tv_time"))
                for j in range(selectvideo.__len__()-1):
                    videotext = selectvideo[j].text
                    if int(videotext[0] + videotext[1]) >= 2:
                        selectvideo[j].click()
                        time.sleep(random.randint(150, 180))
                        issee = True
                        break
                #观看视频成功则退出
                if issee:
                    break
            # elif readtext == "全景VR":
            #     return self.menu1
            # else:
            #     for i in range(5):
            #         dr.swipe(300, random.randint(800, 1000), 300, random.randint(400, 600))
            #         time.sleep(1)
            #         selectvideo = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id("com.v1.video:id/tv_time_big"))
            #         for j in range(selectvideo.__len__()-1):
            #             videotext = selectvideo[j].text
            #             if int(videotext[0] + videotext[1]) >= 2:
            #                 selectvideo[j].click()
            #                 time.sleep(random.randint(150, 180))
            #                 issee = True
            #                 break
            #         #观看视频成功则退出
            #         if issee:
            #             break
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
            issee = False
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.v1.video:id/head_theme_all_back")).click()
            time.sleep(5)
            for i in range(5):
                self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(0, 1), random.randint(2, 2))
                if random.randint(0, 1):
                    self.select_one_by_id("com.v1.video:id/item_theme_all_btn_guanzhu")
                    time.sleep(1)
                self.select_one_by_id("com.v1.video:id/item_theme_all_title_txt")
                time.sleep(1)
                try:
                    WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.v1.video:id/tv_time"))
                except TimeoutException:
                    dr.swipe(300, 500, 300, 1000)
                    time.sleep(5)
                try:
                    selectvideo = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id("com.v1.video:id/tv_time"))
                    for j in range(selectvideo.__len__()-1):
                        videotext = selectvideo[j].text
                        if int(videotext[0] + videotext[1]) >= 2:
                            selectvideo[j].click()
                            time.sleep(random.randint(150, 180))
                            dr.press_keycode(4)
                            time.sleep(1)
                            issee = True
                            break
                except TimeoutException:
                    pass
                dr.press_keycode(4)
                time.sleep(1)
                #观看视频成功则退出
                if issee:
                    break
            self.readnum -= 1
            self.ismenu2 = False
        except Exception as e:
            print("error in menu2")
            return self.exception_returnapp()
        return self.do

    def menu3(self):
        dr = self.driver
        try:
            # issee = False
            self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(0, 5), random.randint(2, 5))
            self.select_one_by_id("com.v1.video:id/tv_more")
            time.sleep(5)
            # for i in range(5):
            #     self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(0, 1), random.randint(2, 5))
            #     selectvideo = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id("com.v1.video:id/tv_time"))
            #     for j in range(selectvideo.__len__()-1):
            #         videotext = selectvideo[j].text
            #         if int(videotext[0] + videotext[1]) >= 2:
            #             selectvideo[j].click()
            #             time.sleep(random.randint(150, 180))
            #             dr.press_keycode(4)
            #             time.sleep(1)
            #             issee = True
            #             break
            #     #观看视频成功则退出
            #     if issee:
            #         break
            dr.press_keycode(4)
            time.sleep(1)
            # self.readnum -= 1
            self.ismenu3 = False
        except Exception as e:
            print("error in menu3")
            return self.exception_returnapp()
        return self.do

    def menu5(self):
        dr = self.driver
        try:
            self.ismenu5 = False
        except Exception as e:
            print("error in menu4")
            return self.exception_returnapp()
        return self.do

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
        # strname = None
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

    def swipes(self, x1, y1, x2, y2, swipe_num=1, swipe_time=1):
        dr = self.driver
        print("swipenum:%s" % swipe_num)
        for x in range(swipe_num):
            dr.swipe(x1, y1, x2, y2)
            time.sleep(swipe_time)

    def select_one_by_id(self, find_id, find_min=0, find_max=0, find_time=15):
        dr = self.driver
        selectone = WebDriverWait(dr, find_time).until(lambda d: d.find_elements_by_id(find_id))
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
        dr.press_keycode(82)
        time.sleep(2)
        try:
            WebDriverWait(dr, 2).until(lambda d: d.find_element_by_name(self.appname)).click()
        except TimeoutException:
            dr.press_keycode(4)
        time.sleep(5)
        return self.do


class Machine1video2(Machine):
    def __init__(self, driver):
        super(Machine1video2, self).__init__(self.initdata)
        self.driver = driver
        self.appname = "第一视频"       #app名字
        self.appname_en = "1video"     #记录文件用缩写英文名
        self.imei = None
        self.remain_day = None

    def initdata(self):
        self.begintime = None
        self.endstime = None
        self.try_count = 0      #初始化出错尝试次数
        self.readnum = random.randint(1, 2)     #初始化阅读次数
        #初始化阅读菜单
        self.ismenu1 = True
        self.ismenu2 = True
        self.ismenu3 = True
        self.ismenu5 = True

        return self.begin

    def begin(self):
        dr = self.driver
        dr.press_keycode(3)
        time.sleep(1)
        dr.press_keycode(3)
        time.sleep(1)
        #     WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("文件管理")).click()
        #     time.sleep(1)
        #     WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("安装包")).click()
        #     time.sleep(1)
        #     WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("第一视频4.5_100066.apk")).click()
        #     time.sleep(1)
        #     try:
        #         WebDriverWait(dr, 10).until(lambda d: d.find_element_by_name("确定")).click()
        #         time.sleep(1)
        #     except TimeoutException:
        #         pass
        #     WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("安装")).click()
        #     time.sleep(1)
        #     WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("打开")).click()
        #     time.sleep(1)
        # except TimeoutException:
        #     #卡在完成页面
        #     for x in range(10):
        #         try:
        #             WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("完成")).click()
        #             time.sleep(1)
        #         except TimeoutException:
        #             break
        #     return self.exit
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name(self.appname)).click()
        time.sleep(10)
        #检测已进入app
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.v1.video:id/iv_guide"))
        self.begintime = "开始:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        #新开软件翻页
        self.swipes(600, 300, 50, 300, 2, 2)
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.v1.video:id/v_go")).click()
        time.sleep(1)
        #选择喜欢的
        for x in range(random.randint(3, 5)):
            self.select_one_by_id("com.v1.video:id/item_guide_name")
            time.sleep(1)
        for x in range(10):
            try:
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.v1.video:id/guide_lay_btn_back")).click()
                time.sleep(1)
                break
            except TimeoutException:
                self.select_one_by_id("com.v1.video:id/item_guide_name")
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
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.v1.video:id/lay_personal")).click()
            time.sleep(1)
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.v1.video:id/mylogin_user_head_img")).click()
            time.sleep(1)
            edit = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_class_name("android.widget.EditText"))
            edit[0].send_keys(str(user.group(1)))
            time.sleep(1)
            edit[1].send_keys(str(pwd.group(1)))
            time.sleep(1)
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.v1.video:id/button_login")).click()
            time.sleep(5)
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.v1.video:id/lay_personal"))
        time.sleep(5)
        return self.do

    def do(self):
        dr = self.driver
        try:
            while self.readnum:
                print("剩下阅读次数:%s" % self.readnum)
                random_read = random.randint(0, 3)
                if random_read == 0:
                    if self.ismenu1:
                        print("goto menu1")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.v1.video:id/lay_home")).click()
                        time.sleep(5)
                        return self.menu1
                    return self.do
                elif random_read == 1:
                    if self.ismenu2:
                        print("goto menu2")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.v1.video:id/lay_subscribe")).click()
                        time.sleep(5)
                        return self.menu2
                    return self.do
                elif random_read == 2:
                    if self.ismenu3:
                        print("goto menu3")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.v1.video:id/lay_find")).click()
                        time.sleep(5)
                        return self.menu3
                    return self.do
                else:
                    if self.ismenu5:
                        print("goto menu5")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.v1.video:id/lay_personal")).click()
                        time.sleep(5)
                        return self.menu5
                    return self.do
        except TimeoutException:
            print("查找菜单出错")
            return self.exception_returnapp()
        print("阅览完毕")
        return self.ends

    def menu1(self):
        dr = self.driver
        try:
            issee = False
            # WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.v1.video:id/iv_add")).click()
            # time.sleep(1)
            # selectone = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id("com.v1.video:id/tv_item"))
            # selectnum = random.randint(0, selectone.__len__()-1)
            # readtext = selectone[selectnum].text
            # selectone[selectnum].click()
            # time.sleep(random.randint(5, 10))
            # self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(1, 3), random.randint(2, 5))
            # if readtext == "头条":
            for i in range(5):
                dr.swipe(300, random.randint(800, 1000), 300, random.randint(400, 600))
                time.sleep(1)
                selectvideo = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id("com.v1.video:id/tv_time"))
                for j in range(selectvideo.__len__()-1):
                    videotext = selectvideo[j].text
                    if int(videotext[0] + videotext[1]) >= 2:
                        selectvideo[j].click()
                        time.sleep(random.randint(150, 180))
                        issee = True
                        break
                #观看视频成功则退出
                if issee:
                    break
            # elif readtext == "全景VR":
            #     return self.menu1
            # else:
            #     for i in range(5):
            #         dr.swipe(300, random.randint(800, 1000), 300, random.randint(400, 600))
            #         time.sleep(1)
            #         selectvideo = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id("com.v1.video:id/tv_time_big"))
            #         for j in range(selectvideo.__len__()-1):
            #             videotext = selectvideo[j].text
            #             if int(videotext[0] + videotext[1]) >= 2:
            #                 selectvideo[j].click()
            #                 time.sleep(random.randint(150, 180))
            #                 issee = True
            #                 break
            #         #观看视频成功则退出
            #         if issee:
            #             break
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
            issee = False
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.v1.video:id/head_theme_all_back")).click()
            time.sleep(5)
            for i in range(5):
                self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(0, 1), random.randint(2, 2))
                if random.randint(0, 1):
                    self.select_one_by_id("com.v1.video:id/item_theme_all_btn_guanzhu")
                    time.sleep(1)
                self.select_one_by_id("com.v1.video:id/item_theme_all_title_txt")
                time.sleep(1)
                try:
                    WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.v1.video:id/tv_time"))
                except TimeoutException:
                    dr.swipe(300, 500, 300, 1000)
                    time.sleep(5)
                try:
                    selectvideo = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id("com.v1.video:id/tv_time"))
                    for j in range(selectvideo.__len__()-1):
                        videotext = selectvideo[j].text
                        if int(videotext[0] + videotext[1]) >= 2:
                            selectvideo[j].click()
                            time.sleep(random.randint(150, 180))
                            dr.press_keycode(4)
                            time.sleep(1)
                            issee = True
                            break
                except TimeoutException:
                    pass
                dr.press_keycode(4)
                time.sleep(1)
                #观看视频成功则退出
                if issee:
                    break
            self.readnum -= 1
            self.ismenu2 = False
        except Exception as e:
            print("error in menu2")
            return self.exception_returnapp()
        return self.do

    def menu3(self):
        dr = self.driver
        try:
            # issee = False
            self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(0, 5), random.randint(2, 5))
            self.select_one_by_id("com.v1.video:id/tv_more")
            time.sleep(5)
            # for i in range(5):
            #     self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(0, 1), random.randint(2, 5))
            #     selectvideo = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id("com.v1.video:id/tv_time"))
            #     for j in range(selectvideo.__len__()-1):
            #         videotext = selectvideo[j].text
            #         if int(videotext[0] + videotext[1]) >= 2:
            #             selectvideo[j].click()
            #             time.sleep(random.randint(150, 180))
            #             dr.press_keycode(4)
            #             time.sleep(1)
            #             issee = True
            #             break
            #     #观看视频成功则退出
            #     if issee:
            #         break
            dr.press_keycode(4)
            time.sleep(1)
            # self.readnum -= 1
            self.ismenu3 = False
        except Exception as e:
            print("error in menu3")
            return self.exception_returnapp()
        return self.do

    def menu5(self):
        dr = self.driver
        try:
            self.ismenu5 = False
        except Exception as e:
            print("error in menu4")
            return self.exception_returnapp()
        return self.do

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

    def swipes(self, x1, y1, x2, y2, swipe_num=1, swipe_time=1):
        dr = self.driver
        print("swipenum:%s" % swipe_num)
        for x in range(swipe_num):
            dr.swipe(x1, y1, x2, y2)
            time.sleep(swipe_time)

    def select_one_by_id(self, find_id, find_min=0, find_max=0, find_time=15):
            dr = self.driver
            selectone = WebDriverWait(dr, find_time).until(lambda d: d.find_elements_by_id(find_id))
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

