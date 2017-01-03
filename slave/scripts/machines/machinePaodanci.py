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
        self.appname = "泡单词"       #app名字
        self.appname_en = "paodanci"     #记录文件用缩写英文名
        self.imei = None
        self.runnum = None        #记录运行次数

    def initdata(self):
        self.phone = None
        self.pwd = None
        self.begintime = None
        self.endstime = None
        self.try_count = 0      #初始化出错尝试次数
        self.readnum = random.randint(1, 1)     #初始化阅读次数
        #初始化阅读菜单
        self.ismenu1 = True
        self.ismenu2 = True
        self.ismenu3 = True
        self.issign = False
        #选择初始化接码平台
        if self.code_platform == "feima":
            self.code = Feima(self.code_user, self.code_pwd, None)
        elif self.code_platform == "yama":
            self.code = Yama(self.code_user, self.code_pwd, None)
        elif self.code_platform == "yima":
            self.code = Yima(self.code_user, self.code_pwd, None)
        elif self.code_platform == "ailezan":
            self.code = Ailezan(self.code_user, self.code_pwd, 25314)
        elif self.code_platform == "jima":
            self.code = Jima(self.code_user, self.code_pwd, None)
        elif self.code_platform == "jiuma":
            self.code = Jiuma(self.code_user, self.code_pwd, None)
        elif self.code_platform == "shenhua":
            self.code = Shenhua(self.code_user, self.code_pwd, None)

        return self.begin

    def begin(self):
        dr = self.driver
        dr.press_keycode(3)
        time.sleep(1)
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name(self.appname)).click()
        time.sleep(10)
        #检测更新
        try:
            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/negative")).click()
            time.sleep(1)
        except TimeoutException:
            pass
        #检测已进入app
        WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/btn_login_enter"))
        self.begintime = "开始:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        time.sleep(1)
        #注册率
        sign_rate = random.randint(1, 10000)
        if sign_rate <= 8500:
            return self.login_code_platform
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/btn_login_enter")).click()
        time.sleep(1)
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/btn_visitor_login")).click()
        time.sleep(1)
        #检查广告
        try:
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/ivClose")).click()
            time.sleep(1)
        except TimeoutException:
            pass
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
                return self.exit
            return self.login_code_platform
        return self.signup

    def signup(self):
        dr = self.driver
        pwd_li = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                  "1", "2", "3", "4", "5", "6", "7", "8", "9", "0",
                  "a", "b", "c", "d", "e", "f", "g", "h", "i", "j",
                  "k", "l", "m", "n", "o", "p", "q", "r", "s", "t",
                  "u", "v", "w", "x", "y", "z"]
        self.pwd = choice(pwd_li)+choice(pwd_li)+choice(pwd_li)+choice(pwd_li)+choice(pwd_li)+choice(pwd_li)
        try:
            #进入注册页面
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/btn_login_enter")).click()
            time.sleep(1)
            #选择接码平台获取手机号码
            self.phone = self.code.getPhone()
            edts = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_class_name("android.widget.EditText"))
            #输入手机号码
            edts[0].send_keys(self.phone)
            time.sleep(1)
            #点击获取验证码按钮
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/btn_getChecked")).click()
            time.sleep(5)
            #选择接码平台获取验证码
            #【泡单词】你的验证码为：575715，10分钟内有效，请勿泄露给他人。
            regrex = r'验证码为：(\d+)'
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
            edts[1].send_keys(captcha)
            time.sleep(1)
            #点击完成按钮按钮
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/login")).click()
            time.sleep(1)
            #检查广告
            try:
                WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/ivClose")).click()
                time.sleep(1)
            except TimeoutException:
                pass
            #检测注册成功进入下一步
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/rbtn_personal_center")).click()
            time.sleep(1)
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
        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/tv_user_nickname")).click()
        time.sleep(1)
        #输入昵称
        name = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/et_nickname"))
        name.click()
        time.sleep(0.5)
        dr.press_keycode(123)
        time.sleep(0.5)
        for i in range(10):
            dr.press_keycode(67)
        name.send_keys(self.get_filemessage("name.txt"))
        time.sleep(1)
        #选择性别
        if random.randint(0, 1):
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/tv_gender")).click()
            time.sleep(1)
            dr.swipe(300, 1180, 300, 1100)
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("确定")).click()
            time.sleep(1)
        #选择年龄
        if not random.randint(0, 4):
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/tv_age")).click()
            time.sleep(1)
            self.swipes(300, 1180, 300, 1100, random.randint(17, 30), 1, 1)
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("确定")).click()
            time.sleep(1)
        #保存信息按钮
        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/ibtn_right")).click()
        time.sleep(10)
        #检测信息保存完毕跳转页面
        WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/rbtn_personal_center"))
        #选择头像
        if not random.randint(0, 9):
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/chiv_user_header")).click()
            time.sleep(1)
            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("相册")).click()
            time.sleep(1)
            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("文件管理")).click()
            time.sleep(1)
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("1")).click()
            time.sleep(1)
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("1touxiang")).click()
            time.sleep(1)
            for i in range(random.randint(0, 80)):
                dr.swipe(300, random.randint(800, 1000), 300, random.randint(300, 600))
                time.sleep(1)
            time.sleep(5)
            self.select_one_by_id("com.android.fileexplorer:id/file_image")
            time.sleep(1)
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/btn_done")).click()
            time.sleep(1)
            #检测信息保存完毕跳转页面
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/rbtn_personal_center"))
        self.issign = True
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
            if self.ismenu1:
                print("goto menu1")
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/rbtn_index")).click()
                time.sleep(5)
                return self.menu1
            if self.ismenu2 and self.issign and random.randint(0, 2):
                print("goto menu2")
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/rbtn_arena")).click()
                time.sleep(5)
                return self.menu2
            if self.ismenu3 and self.issign and random.randint(0, 1):
                print("goto menu3")
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/rbtn_personal_center")).click()
                time.sleep(5)
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
            #添加计划
            try:
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("添加计划")).click()
                time.sleep(1)
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/tv_title"))
                #选择词汇
                self.swipes(100, random.randint(800, 1000), 100, random.randint(400, 600), random.randint(0, 1), 1, 1)
                self.select_one_by_id("com.paoword.www.paoword:id/tv_title")
                time.sleep(1)
                self.select_one_by_id("com.paoword.www.paoword:id/typeName2")
                time.sleep(5)
                #每天词量/完成天数
                for i in range(random.randint(0, 5)):
                    dr.swipe(200, 1160, 200, 1060)
                    time.sleep(1)
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/btn_ok")).click()
                time.sleep(5)
            except TimeoutException:
                pass
            #学习
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/begin")).click()
            time.sleep(1)
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/layout_expand")).click()
            time.sleep(1)
            for x in range(random.randint(10, 20)):
                try:
                    #拆分单词
                    if random.randint(0, 4):
                        try:
                            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/layout_expand")).click()
                            time.sleep(random.randint(2, 5))
                        except TimeoutException:
                            pass
                    #查看视频
                    if not random.randint(0, 19):
                        try:
                            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/tv_btn_connect")).click()
                            time.sleep(random.randint(5, 15))
                        except TimeoutException:
                            pass
                    #收藏
                    if not random.randint(0, 4):
                        try:
                            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/actionAddWord")).click()
                            time.sleep(1)
                        except TimeoutException:
                            pass
                    #笔记
                    if not random.randint(0, 19) and self.issign:
                        # note = WebDriverWait(dr, 20).until(lambda d: d.find_element_by_id(choice(["com.paoword.www.paoword:id/memory_dec", "com.paoword.www.paoword:id/memory_assistance"]))).text
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/note")).click()
                        time.sleep(1)
                        self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(0, 2), 1, 2)
                        time.sleep(1)
                        try:
                            contenttext = WebDriverWait(dr, 10).until(lambda d: d.find_elements_by_id("com.paoword.www.paoword:id/tv_expandable_text"))
                            note = contenttext[random.randint(0, contenttext.__len__()-1)].text
                            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/tv_btn_write_note")).click()
                            time.sleep(1)
                            edts = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/et_note_content"))
                            edts.send_keys(note)
                            time.sleep(1)
                            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/btn_right")).click()
                            time.sleep(1)
                            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/actionBack")).click()
                            time.sleep(1)
                        except TimeoutException:
                            dr.press_keycode(4)
                            time.sleep(1)
                    time.sleep(random.randint(2, 5))
                    #检测学习完成
                    try:
                        WebDriverWait(dr, 2).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/img_btn_back"))
                        time.sleep(1)
                        break
                    except TimeoutException:
                        pass
                    #泡/爆
                    if random.randint(0, 4):
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/next")).click()
                        time.sleep(1)
                    else:
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/ignore")).click()
                        time.sleep(1)
                except TimeoutException:
                    break
            dr.press_keycode(4)
            time.sleep(5)
            dr.press_keycode(4)
            time.sleep(1)
            #复习
            if random.randint(0, 1):
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/redo")).click()
                time.sleep(1)
                for x in range(random.randint(2, 5)):
                    time.sleep(random.randint(2, 5))
                    #提示
                    if not random.randint(0, 4):
                        try:
                            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/reminder_image")).click()
                            time.sleep(2)
                        except TimeoutException:
                            pass
                    try:
                        ans = WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id(choice(["com.paoword.www.paoword:id/item1_margin", "com.paoword.www.paoword:id/item2_margin",
                                                                                            "com.paoword.www.paoword:id/item3_margin", "com.paoword.www.paoword:id/item4_margin"])))
                        dr.tap(ans.location['x']+5, ans.location['y']+5)
                        time.sleep(1)
                    except TimeoutException:
                        dr.press_keycode(4)
                        time.sleep(5)
                        break
                dr.press_keycode(4)
                time.sleep(1)
            self.ismenu1 = False
        except Exception as e:
            print("error in menu1")
            return self.exception_returnapp()
        return self.do

    def menu2(self):
        dr = self.driver
        try:
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("双人竞技")).click()
            time.sleep(5)
            for x in range(15):
                try:
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id(choice(["com.paoword.www.paoword:id/option_view_1", "com.paoword.www.paoword:id/option_view_2",
                                                                                        "com.paoword.www.paoword:id/option_view_3", "com.paoword.www.paoword:id/option_view_4"]))).click()
                    WebDriverWait(dr, 10).until_not(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/option_view_1"))
                    time.sleep(random.randint(1, 3))
                except TimeoutException:
                    try:
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/ibtn_back")).click()
                        time.sleep(1)
                        break
                    except TimeoutException:
                        pass
                    try:
                        dr.find_element_by_name("双人竞技")
                        time.sleep(1)
                        break
                    except NoSuchElementException:
                        pass
                    try:
                        dr.find_element_by_id("com.paoword.www.paoword:id/positive").click()
                        time.sleep(1)
                        break
                    except NoSuchElementException:
                        pass
                time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            self.ismenu2 = False
        except Exception as e:
            print("error in menu2")
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
        st = [1200, 2000, 2500, 3000, 3000, 1200, 180, 120, 40, 20, 10, 10,
              10, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0]

        print("现在时间是%s:%s,脚本将在%s秒后继续执行" % (time.localtime().tm_hour, time.localtime().tm_min, st[time.localtime().tm_hour-1]))
        time.sleep(st[time.localtime().tm_hour-1])

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
        self.appname = "泡单词"       #app名字
        self.appname_en = "paodanci"     #记录文件用缩写英文名
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
        self.issign = False
        return self.begin

    def begin(self):
        dr = self.driver
        dr.press_keycode(3)
        time.sleep(1)
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name(self.appname)).click()
        time.sleep(10)
        #检测更新
        try:
            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/negative")).click()
            time.sleep(1)
        except TimeoutException:
            pass
        #帐号其他地方登录
        try:
            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/positive")).click()
            time.sleep(1)
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/btn_visitor_login")).click()
            time.sleep(5)
        except TimeoutException:
            pass
        #检查广告
        try:
            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/ivClose")).click()
            time.sleep(1)
        except TimeoutException:
            pass
        try:
            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/btn_login_enter")).click()
            time.sleep(1)
            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/btn_visitor_login")).click()
            time.sleep(1)
        except TimeoutException:
            pass
        #检测已进入app
        WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/rbtn_index"))
        self.begintime = "开始:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        time.sleep(1)
        #检测是否已注册
        WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/rbtn_personal_center")).click()
        try:
            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/positive")).click()
            time.sleep(1)
        except TimeoutException:
            self.issign = True
        return self.do

    def do(self):
        dr = self.driver
        try:
            if self.ismenu1:
                print("goto menu1")
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/rbtn_index")).click()
                time.sleep(5)
                return self.menu1
            if self.ismenu2 and self.issign and random.randint(0, 1):
                print("goto menu2")
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/rbtn_arena")).click()
                time.sleep(5)
                return self.menu2
            if self.ismenu3 and self.issign and random.randint(0, 1):
                print("goto menu3")
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/rbtn_personal_center")).click()
                time.sleep(5)
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
            #无尽复习添加新任务
            try:
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("无尽复习"))
                time.sleep(1)
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/learnClass")).click()
                time.sleep(1)
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/ibtn_right")).click()
                time.sleep(1)
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/tv_title"))
                #选择词汇
                self.swipes(100, random.randint(800, 1000), 100, random.randint(400, 600), random.randint(0, 1), 1, 1)
                self.select_one_by_id("com.paoword.www.paoword:id/tv_title")
                time.sleep(1)
                self.select_one_by_id("com.paoword.www.paoword:id/typeName2")
                time.sleep(5)
                #每天词量/完成天数
                for i in range(random.randint(0, 5)):
                    dr.swipe(200, 1160, 200, 1060)
                    time.sleep(1)
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/btn_ok")).click()
                time.sleep(5)
            except TimeoutException:
                pass
            #添加计划
            try:
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("添加计划")).click()
                time.sleep(1)
                WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/tv_title"))
                #选择词汇
                self.swipes(100, random.randint(800, 1000), 100, random.randint(400, 600), random.randint(0, 1), 1, 1)
                self.select_one_by_id("com.paoword.www.paoword:id/tv_title")
                time.sleep(1)
                self.select_one_by_id("com.paoword.www.paoword:id/typeName2")
                time.sleep(5)
                #每天词量/完成天数
                for i in range(random.randint(0, 5)):
                    dr.swipe(200, 1160, 200, 1060)
                    time.sleep(1)
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/btn_ok")).click()
                time.sleep(5)
            except TimeoutException:
                pass
            #学习
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/begin")).click()
            time.sleep(1)
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/layout_expand")).click()
            time.sleep(1)
            for x in range(random.randint(10, 15)):
                try:
                    #拆分单词
                    if random.randint(0, 4):
                        try:
                            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/layout_expand")).click()
                            time.sleep(random.randint(1, 2))
                        except TimeoutException:
                            pass
                    #收藏
                    if not random.randint(0, 4):
                        try:
                            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/actionAddWord")).click()
                            time.sleep(1)
                        except TimeoutException:
                            pass
                    time.sleep(random.randint(1, 2))
                    #检测学习完成
                    try:
                        WebDriverWait(dr, 2).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/img_btn_back"))
                        time.sleep(1)
                        break
                    except TimeoutException:
                        pass
                    #泡/爆
                    if random.randint(0, 4):
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/next")).click()
                        time.sleep(1)
                    else:
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/ignore")).click()
                        time.sleep(1)
                except TimeoutException:
                    break
            dr.press_keycode(4)
            time.sleep(5)
            dr.press_keycode(4)
            time.sleep(1)
            #复习
            if random.randint(0, 1):
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/redo")).click()
                time.sleep(1)
                for x in range(random.randint(2, 5)):
                    time.sleep(random.randint(2, 5))
                    #提示
                    if not random.randint(0, 4):
                        try:
                            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/reminder_image")).click()
                            time.sleep(2)
                        except TimeoutException:
                            pass
                    try:
                        ans = WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id(choice(["com.paoword.www.paoword:id/item1_margin", "com.paoword.www.paoword:id/item2_margin",
                                                                                            "com.paoword.www.paoword:id/item3_margin", "com.paoword.www.paoword:id/item4_margin"])))
                        dr.tap(ans.location['x']+5, ans.location['y']+5)
                        time.sleep(1)
                    except TimeoutException:
                        dr.press_keycode(4)
                        time.sleep(5)
                        break
                dr.press_keycode(4)
                time.sleep(1)
            self.ismenu1 = False
        except Exception as e:
            print("error in menu1")
            return self.exception_returnapp()
        return self.do

    def menu2(self):
        dr = self.driver
        try:
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("双人竞技")).click()
            time.sleep(5)
            for x in range(15):
                try:
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id(choice(["com.paoword.www.paoword:id/option_view_1", "com.paoword.www.paoword:id/option_view_2",
                                                                                        "com.paoword.www.paoword:id/option_view_3", "com.paoword.www.paoword:id/option_view_4"]))).click()
                    WebDriverWait(dr, 10).until_not(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/option_view_1"))
                    time.sleep(random.randint(1, 3))
                except TimeoutException:
                    try:
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.paoword.www.paoword:id/ibtn_back")).click()
                        time.sleep(1)
                        break
                    except TimeoutException:
                        pass
                    try:
                        dr.find_element_by_name("双人竞技")
                        time.sleep(1)
                        break
                    except NoSuchElementException:
                        pass
                    try:
                        dr.find_element_by_id("com.paoword.www.paoword:id/positive").click()
                        time.sleep(1)
                        break
                    except NoSuchElementException:
                        pass
                time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            self.ismenu2 = False
        except Exception as e:
            print("error in menu2")
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

