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
    from util import copyfile, removefile
except ImportError:
    copyfile = lambda: 1
    removefile = lambda: 1


class Machinex(Machine):
    def __init__(self, driver, code_platform, fm_uname, fm_pwd):
        super(Machinex, self).__init__(self.initdata)
        self.driver = driver
        self.code_platform = code_platform      #接码平台
        self.code_user = fm_uname       #接码平台帐号
        self.code_pwd = fm_pwd      #接码平台密码
        self.appname = "图加"       #app名字
        self.appname_en = "tujia"     #记录文件用缩写英文名
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
        #选择初始化接码平台
        if self.code_platform == "feima":
            self.code = Feima(self.code_user, self.code_pwd, None)
        elif self.code_platform == "yama":
            self.code = Yama(self.code_user, self.code_pwd, None)
        elif self.code_platform == "yima":
            self.code = Yima(self.code_user, self.code_pwd, None)
        elif self.code_platform == "ailezan":
            self.code = Ailezan(self.code_user, self.code_pwd, 29529)
        elif self.code_platform == "jima":
            self.code = Jima(self.code_user, self.code_pwd, None)
        elif self.code_platform == "jiuma":
            self.code = Jiuma(self.code_user, self.code_pwd, None)
        elif self.code_platform == "shenhua":
            self.code = Shenhua(self.code_user, self.code_pwd, 86806)

        return self.begin

    def begin(self):
        dr = self.driver
        dr.press_keycode(3)
        time.sleep(1)
        #注册率
        sign_rate = random.randint(1, 10000)
        if sign_rate <= 8500:
            removefile("/sdcard/2/*.jpg")
            removefile("/sdcard/*.jpg")
            time.sleep(1)
            copyfile("/sdcard/1/\.1touxiang/PIC\ \(%s\).jpg" % random.randint(1, 1400), "/sdcard/")
            time.sleep(0.5)
            for _ in range(5):
                copyfile("/sdcard/1/\.1xiangce/PIC\ \(%s\).jpg" % random.randint(1, 1400), "/sdcard/2/")
                time.sleep(0.5)
            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("文件管理")).click()
            time.sleep(1)
            try:
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("手机")).click()
                time.sleep(1)
            except TimeoutException:
                dr.press_keycode(4)
                time.sleep(1)
                dr.press_keycode(4)
                time.sleep(1)
                dr.press_keycode(4)
                time.sleep(1)
                return self.begin
            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("2")).click()
            time.sleep(1)
            dr.swipe(600, 400, 590, 400, 50)
            time.sleep(1)
            try:
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("剪切")).click()
                time.sleep(1)
            except TimeoutException:
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("更多")).click()
                time.sleep(2)
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("剪切")).click()
                time.sleep(1)
            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("粘贴")).click()
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("文件管理")).click()
            time.sleep(1)
            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("图片")).click()
            time.sleep(5)
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            #加速器
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_name("GMD Speed Time")).click()
            time.sleep(1)
            try:
                WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.gmd.speedtime:id/buttonStop")).click()
                time.sleep(1)
                WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.gmd.speedtime:id/buttonStart")).click()
                time.sleep(1)
            except TimeoutException:
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("No, thanks")).click()
                time.sleep(1)
                WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.gmd.speedtime:id/buttonStop")).click()
                time.sleep(1)
                WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.gmd.speedtime:id/buttonStart")).click()
                time.sleep(1)
            dr.press_keycode(3)
            time.sleep(1)
            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name(self.appname)).click()
            time.sleep(5)
            #检测已进入app
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/btn_register"))
            self.begintime = "开始:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
            time.sleep(1)
            return self.login_code_platform
        #加速器
        WebDriverWait(dr, 10).until(lambda d: d.find_element_by_name("GMD Speed Time")).click()
        time.sleep(1)
        WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.gmd.speedtime:id/buttonStop")).click()
        time.sleep(1)
        WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.gmd.speedtime:id/buttonStart")).click()
        time.sleep(1)
        dr.press_keycode(3)
        time.sleep(1)
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name(self.appname)).click()
        time.sleep(5)
        #检测已进入app
        WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/btn_register"))
        self.begintime = "开始:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        time.sleep(random.randint(30, 60))
        return self.ends

    def login_code_platform(self):
        #登录接码平台
        print("login %s getcode ......" % self.code_platform)
        try:
            self.code.login()
        except Exception as e:
            print("error in login getcodeplatform,try_count:%s" % self.try_count)
            self.try_count += 1
            if self.try_count > 5:
                time.sleep(random.randint(180, 200))
                self.try_count = 0
                print("on try_count,exit")
                try:
                    with open('/sdcard/1/logerror.log', 'a') as f:
                        f.write("\nerror:%s" % self.begintime)
                except:
                    pass
                return self.ends
            return self.login_code_platform
        return self.signup

    def signup(self):
        dr = self.driver
        pwd_li = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                  "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                  "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                  "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                  "u", "v", "w", "x", "y", "z"]
        self.pwd = ""
        for _ in range(random.randint(6, 8)):
            self.pwd += choice(pwd_li)
        try:
            #进入注册页面
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/btn_register")).click()
            time.sleep(1)
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/register_service_agree_holder")).click()
            time.sleep(1)
            #选择接码平台获取手机号码
            # self.phone = self.code.getPhone()
            self.phone = self.code.getPhone(vno='0')
            edts = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_class_name("android.widget.EditText"))
            #输入手机号码
            edts.send_keys(self.phone)
            time.sleep(1)
            #点击获取验证码按钮
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/send_code")).click()
            time.sleep(5)
            # try:
            #     dr.find_element_by_name("60s")
            #     print("getMessage failed,try_count:%s" % self.try_count)
            #     #释放号码
            #     self.code.releasePhone(self.phone)
            #     dr.press_keycode(4)
            #     time.sleep(1)
            #     return self.signup
            # except NoSuchElementException:
            #     pass
            #选择接码平台获取验证码
            #图加的验证码：6668【图加科技】
            regrex = r'验证码：(\d+)'
            captcha = self.code.waitForMessage(regrex, self.phone)
            if captcha is None:
                print("getMessage failed,try_count:%s" % self.try_count)
                #释放号码
                self.code.releasePhone(self.phone)
                self.try_count += 1
                if self.try_count > 5:
                    return self.exit
                dr.press_keycode(4)
                time.sleep(1)
                return self.signup
            #输入验证码
            edts[2].send_keys(captcha)
            time.sleep(1)
            #输入密码
            edts[3].send_keys(self.pwd)
            time.sleep(1)
            edts[0].send_keys(self.get_filemessage("name.txt"))
            time.sleep(1)
            #点击完成按钮按钮
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/register")).click()
            time.sleep(1)
            #检测注册成功进入下一步
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/control_panel_camera"))
            return self.after_signup
        except Exception as e:
            print("error in getPhone,try_count:%s" % self.try_count)
            self.try_count += 1
            if self.try_count > 5:
                return self.exit
            dr.press_keycode(4)
            time.sleep(2)
            return self.signup

    def after_signup(self):
        dr = self.driver
        #选择头像
        if not random.randint(0, 4):
            WebDriverWait(dr, 20).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/control_panel_me")).click()
            time.sleep(1)
            WebDriverWait(dr, 20).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/me_avatar")).click()
            time.sleep(1)
            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("相册")).click()
            time.sleep(5)
            self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(0, 2), 2, 2)
            self.select_one_by_id("com.tujiaapp.tujia:id/grid_image")
            time.sleep(1)
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("保存")).click()
            time.sleep(5)
            #检测信息保存完毕跳转页面
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/control_panel_camera"))
        #记录帐号密码
        try:
            with open('/sdcard/1/user%s.log' % self.appname_en, 'a') as f:
                f.write('\nimei:%s,%s,%s (time %s.%s  %s:%s:%s)' % (self.imei, self.phone, self.pwd, time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec))
        except:
            with open('D:/brush/slave/scripts/doc/user%s.log' % self.appname_en, 'a') as f:
                f.write('\nimei:%s,%s,%s (time %s.%s  %s:%s:%s)' % (self.imei, self.phone, self.pwd, time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec))
        time.sleep(1)
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
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/control_panel_home")).click()
                        time.sleep(5)
                        return self.menu1
                    return self.do
                elif random_read == 1:
                    if self.ismenu2:
                        print("goto menu2")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/control_panel_location")).click()
                        time.sleep(5)
                        return self.menu2
                    return self.do
                elif random_read == 2:
                    if self.ismenu3:
                        print("goto menu3")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/control_panel_camera")).click()
                        time.sleep(5)
                        return self.menu3
                    return self.do
                elif random_read == 3:
                    if self.ismenu4:
                        print("goto menu4")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/control_panel_feed")).click()
                        time.sleep(5)
                        return self.menu4
                    return self.do
                else:
                    if self.ismenu5:
                        print("goto menu5")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/control_panel_me")).click()
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
            if random.randint(0, 1):
                WebDriverWait(dr, 20).until(lambda d: d.find_element_by_name("图文")).click()
                time.sleep(5)
                try:
                    WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/tv_info")).click()
                    time.sleep(1)
                except TimeoutException:
                    pass
                looknum = random.randint(2, 10)
                for _ in range(looknum):
                    for i in range(random.randint(0, 2)):
                        dr.swipe(300, random.randint(800, 1000), 300, random.randint(300, 600))
                        time.sleep(random.randint(2, 5))
                    self.select_one_by_id("com.tujiaapp.tujia:id/item_tv_title")
                    time.sleep(random.randint(5, 10))
                    if looknum <= 4:
                        for i in range(random.randint(4, 6)):
                            dr.swipe(300, random.randint(800, 1000), 300, random.randint(300, 600))
                            time.sleep(random.randint(2, 4))
                    elif 4 < looknum <= 8:
                        for i in range(random.randint(2, 4)):
                            dr.swipe(300, random.randint(800, 1000), 300, random.randint(300, 600))
                            time.sleep(random.randint(2, 4))
                    else:
                        for i in range(random.randint(1, 2)):
                            dr.swipe(300, random.randint(800, 1000), 300, random.randint(300, 600))
                            time.sleep(random.randint(2, 4))
                    #点赞
                    if not random.randint(0, 9):
                        try:
                            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/ll_heart")).click()
                            time.sleep(5)
                        except TimeoutException:
                            pass
                    #收藏
                    if not random.randint(0, 9):
                        try:
                            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/iv_like")).click()
                            time.sleep(5)
                        except TimeoutException:
                            pass
                    dr.press_keycode(4)
                    time.sleep(1)
                    dr.press_keycode(4)
                    time.sleep(1)
            else:
                WebDriverWait(dr, 20).until(lambda d: d.find_element_by_name("图集")).click()
                time.sleep(10)
                looknum = random.randint(2, 10)
                for _ in range(looknum):
                    for i in range(random.randint(0, 2)):
                        dr.swipe(300, random.randint(800, 1000), 300, random.randint(300, 600))
                        time.sleep(random.randint(2, 5))
                    self.select_one_by_id("com.tujiaapp.tujia:id/scope_cardview")
                    time.sleep(random.randint(5, 10))
                    for i in range(random.randint(1, 4)):
                        dr.swipe(300, random.randint(800, 1000), 300, random.randint(300, 600))
                        if looknum > 6:
                            time.sleep(random.randint(1, 2))
                        else:
                            time.sleep(random.randint(2, 4))
                    #收藏
                    if not random.randint(0, 4):
                        try:
                            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/iv_like")).click()
                            time.sleep(5)
                        except TimeoutException:
                            pass
                    dr.press_keycode(4)
                    time.sleep(1)
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
        city = ["黑龙江", "吉林", "辽宁", "河北", "山东", "江苏", "安徽", "浙江", "福建", "广东", "海南", "云南", "贵州", "四川", "北京", "天津",
                "湖北", "河南", "山西", "陕西", "甘肃", "青海", "江西", "台湾", "香港", "澳门", "广西", "内蒙古", "宁夏", "西藏", "新疆", "上海", "重庆"]
        try:
            edts = WebDriverWait(dr, 5).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
            edts.send_keys(choice(city))
            time.sleep(1)
            dr.press_keycode(66)
            time.sleep(5)
            if random.randint(0, 1):
                WebDriverWait(dr, 20).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/get_scopes")).click()
                time.sleep(5)
                for i in range(random.randint(1, 3)):
                    dr.swipe(300, random.randint(800, 1000), 300, random.randint(300, 600))
                    time.sleep(random.randint(2, 5))
                time.sleep(2)
                self.select_one_by_id("com.tujiaapp.tujia:id/scope_cover_image_overlay")
                time.sleep(random.randint(5, 15))
                for i in range(random.randint(10, 15)):
                    dr.swipe(300, random.randint(800, 1000), 300, random.randint(300, 600))
                    time.sleep(random.randint(5, 10))
                #收藏
                if not random.randint(0, 4):
                    try:
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/iv_like")).click()
                        time.sleep(5)
                    except TimeoutException:
                        pass
                dr.press_keycode(4)
                time.sleep(2)
            else:
                WebDriverWait(dr, 20).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/get_photos")).click()
                time.sleep(5)
                for i in range(random.randint(1, 3)):
                    dr.swipe(300, random.randint(800, 1000), 300, random.randint(300, 600))
                    time.sleep(random.randint(2, 5))
                time.sleep(2)
                self.select_one_by_id("com.tujiaapp.tujia:id/grid_image")
                time.sleep(random.randint(5, 15))
                for i in range(random.randint(10, 15)):
                    dr.swipe(300, random.randint(800, 1000), 300, random.randint(300, 600))
                    time.sleep(random.randint(5, 10))
                #收藏
                if not random.randint(0, 4):
                    try:
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/single_media_like_normal")).click()
                        time.sleep(5)
                    except TimeoutException:
                        pass
                dr.press_keycode(4)
                time.sleep(2)
            dr.press_keycode(4)
            time.sleep(2)
            dr.press_keycode(4)
            time.sleep(2)
            self.readnum -= 1
            self.ismenu2 = False
        except Exception as e:
            print("error in menu2")
            return self.exception_returnapp()
        return self.do

    def menu3(self):
        dr = self.driver
        try:
            if random.randint(0, 1):
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/iv_close_dialog")).click()
                time.sleep(1)
            else:
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/ll_atlas")).click()
                time.sleep(1)
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/row_rescope_holder")).click()
                time.sleep(1)
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/upload_media_upload")).click()
                time.sleep(1)
                for _ in range(5):
                    # self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(0, 2), 2, 2)
                    self.select_one_by_id("com.tujiaapp.tujia:id/grid_image")
                    time.sleep(1)
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/tv_next")).click()
                time.sleep(1)
                tags = WebDriverWait(dr, 10).until(lambda d: d.find_elements_by_xpath("//android.view.View[@resource-id='com.tujiaapp.tujia:id/flow_tags']/android.widget.TextView"))
                tags[random.randint(0, tags.__len__()-1)].click()
                time.sleep(1)
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/tv_next")).click()
                time.sleep(1)
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/iv_scope_back")).click()
                time.sleep(5)
            self.ismenu3 = False
        except Exception as e:
            print("error in menu3")
            return self.exception_returnapp()
        return self.do

    def menu4(self):
        dr = self.driver
        try:
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
        #加速器
        dr.press_keycode(3)
        time.sleep(1)
        dr.press_keycode(3)
        time.sleep(1)
        WebDriverWait(dr, 10).until(lambda d: d.find_element_by_name("GMD Speed Time")).click()
        time.sleep(1)
        try:
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.gmd.speedtime:id/buttonStop")).click()
            time.sleep(1)
        except TimeoutException:
            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("No, thanks")).click()
            time.sleep(1)
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.gmd.speedtime:id/buttonStop")).click()
            time.sleep(1)
        dr.press_keycode(3)
        time.sleep(1)
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
        self.appname = "图加"       #app名字
        self.appname_en = "tujia"     #记录文件用缩写英文名
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
        #加速器
        WebDriverWait(dr, 10).until(lambda d: d.find_element_by_name("GMD Speed Time")).click()
        time.sleep(1)
        try:
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.gmd.speedtime:id/buttonStop")).click()
            time.sleep(1)
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.gmd.speedtime:id/buttonStart")).click()
            time.sleep(1)
        except TimeoutException:
            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("No, thanks")).click()
            time.sleep(1)
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.gmd.speedtime:id/buttonStop")).click()
            time.sleep(1)
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.gmd.speedtime:id/buttonStart")).click()
            time.sleep(1)
        dr.press_keycode(3)
        time.sleep(1)
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name(self.appname)).click()
        time.sleep(10)
        #检测已进入app
        WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/btn_register"))
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
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/btn_login")).click()
            time.sleep(1)
            edit = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_class_name("android.widget.EditText"))
            edit[0].send_keys(str(user.group(1)))
            time.sleep(1)
            edit[1].send_keys(str(pwd.group(1)))
            time.sleep(1)
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/login")).click()
            time.sleep(5)
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/control_panel_camera"))
            return self.do
        time.sleep(random.randint(15, 30))
        return self.ends

    def do(self):
        dr = self.driver
        try:
            while self.readnum:
                print("剩下阅读次数:%s" % self.readnum)
                random_read = random.randint(0, 4)
                if random_read == 0:
                    if self.ismenu1:
                        print("goto menu1")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/control_panel_home")).click()
                        time.sleep(5)
                        return self.menu1
                    return self.do
                elif random_read == 1:
                    if self.ismenu2:
                        print("goto menu2")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/control_panel_location")).click()
                        time.sleep(5)
                        return self.menu2
                    return self.do
                elif random_read == 2:
                    if self.ismenu3:
                        print("goto menu3")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/control_panel_camera")).click()
                        time.sleep(5)
                        return self.menu3
                    return self.do
                elif random_read == 3:
                    if self.ismenu4:
                        print("goto menu4")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/control_panel_feed")).click()
                        time.sleep(5)
                        return self.menu4
                    return self.do
                else:
                    if self.ismenu5:
                        print("goto menu5")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/control_panel_me")).click()
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
            if random.randint(0, 1):
                WebDriverWait(dr, 20).until(lambda d: d.find_element_by_name("图文")).click()
                time.sleep(5)
                try:
                    WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/tv_info")).click()
                    time.sleep(1)
                except TimeoutException:
                    pass
                looknum = random.randint(2, 5)
                for _ in range(looknum):
                    for i in range(random.randint(0, 2)):
                        dr.swipe(300, random.randint(800, 1000), 300, random.randint(300, 600))
                        time.sleep(random.randint(2, 5))
                    self.select_one_by_id("com.tujiaapp.tujia:id/item_tv_title")
                    time.sleep(random.randint(5, 10))
                    for i in range(random.randint(1, 4)):
                        dr.swipe(300, random.randint(800, 1000), 300, random.randint(300, 600))
                        time.sleep(random.randint(1, 3))
                    #点赞
                    if not random.randint(0, 9):
                        try:
                            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/ll_heart")).click()
                            time.sleep(1)
                        except TimeoutException:
                            pass
                    #收藏
                    if not random.randint(0, 9):
                        try:
                            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/iv_like")).click()
                            time.sleep(1)
                        except TimeoutException:
                            pass
                    dr.press_keycode(4)
                    time.sleep(1)
                    dr.press_keycode(4)
                    time.sleep(1)
            else:
                WebDriverWait(dr, 20).until(lambda d: d.find_element_by_name("图集")).click()
                time.sleep(10)
                looknum = random.randint(2, 5)
                for _ in range(looknum):
                    for i in range(random.randint(0, 2)):
                        dr.swipe(300, random.randint(800, 1000), 300, random.randint(300, 600))
                        time.sleep(random.randint(2, 5))
                    self.select_one_by_id("com.tujiaapp.tujia:id/scope_cardview")
                    time.sleep(random.randint(5, 10))
                    for i in range(random.randint(1, 4)):
                        dr.swipe(300, random.randint(800, 1000), 300, random.randint(300, 600))
                        time.sleep(random.randint(1, 2))
                    #收藏
                    if not random.randint(0, 9):
                        try:
                            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/iv_like")).click()
                            time.sleep(1)
                        except TimeoutException:
                            pass
                    dr.press_keycode(4)
                    time.sleep(1)
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
            self.ismenu2 = False
        except Exception as e:
            print("error in menu2")
            return self.exception_returnapp()
        return self.do

    def menu3(self):
        dr = self.driver
        try:
            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.tujiaapp.tujia:id/iv_close_dialog")).click()
            time.sleep(1)
            self.ismenu3 = False
        except Exception as e:
            print("error in menu3")
            return self.exception_returnapp()
        return self.do

    def menu4(self):
        dr = self.driver
        try:
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
        #加速器
        dr.press_keycode(3)
        time.sleep(1)
        dr.press_keycode(3)
        time.sleep(1)
        WebDriverWait(dr, 10).until(lambda d: d.find_element_by_name("GMD Speed Time")).click()
        time.sleep(1)
        try:
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.gmd.speedtime:id/buttonStop")).click()
            time.sleep(1)
        except TimeoutException:
            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("No, thanks")).click()
            time.sleep(1)
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.gmd.speedtime:id/buttonStop")).click()
            time.sleep(1)
        dr.press_keycode(3)
        time.sleep(1)
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

