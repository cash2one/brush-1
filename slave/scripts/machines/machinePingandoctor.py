#! -*- coding=utf-8 -*-
import os
import time
# import logging
import re
from machines.StateMachine import Machine
from appium4droid import webdriver
from appium4droid.common.exceptions import *
from appium4droid.support.ui import WebDriverWait
import random
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
        self.appname = "平安好医生"       #app名字
        self.appname_en = "pingandoctor"     #记录文件用缩写英文名
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
            self.code = Feima(self.code_user, self.code_pwd, 1494)
        elif self.code_platform == "yama":
            self.code = Yama(self.code_user, self.code_pwd, 357)
        elif self.code_platform == "yima":
            self.code = Yima(self.code_user, self.code_pwd, None)
        elif self.code_platform == "ailezan":
            self.code = Ailezan(self.code_user, self.code_pwd, 1923)
        elif self.code_platform == "jima":
            self.code = Jima(self.code_user, self.code_pwd, None)
        elif self.code_platform == "jiuma":
            self.code = Jiuma(self.code_user, self.code_pwd, None)
        elif self.code_platform == "shenhua":
            self.code = Shenhua(self.code_user, self.code_pwd, 367)

        return self.begin

    def begin(self):
        dr = self.driver
        dr.press_keycode(3)
        time.sleep(1)
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name(self.appname)).click()
        time.sleep(10)
        #检测已进入app
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.pingan.papd:id/iv_guide_1"))
        self.begintime = "开始:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        time.sleep(1)
        #新开软件翻页
        self.swipes(600, 300, 300, 300, 4, 2)
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.pingan.papd:id/go_btn")).click()
        #注册率
        sign_rate = random.randint(1, 10000)
        if sign_rate <= 5000:
            return self.login_code_platform
        time.sleep(random.randint(5, 15))
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
            #选择接码平台获取手机号码
            self.phone = self.code.getPhone()
            edts = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_class_name("android.widget.EditText"))
            #输入手机号码
            edts[0].send_keys(self.phone)
            time.sleep(1)
            #点击获取验证码按钮
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.pingan.papd:id/send_reqcode_btn")).click()
            time.sleep(5)
            #输入密码
            # edts[2].send_keys(self.pwd)
            # time.sleep(1)
            #选择接码平台获取验证码
            #【平安好医生】短信验证码：191954。(来自10690483063644)
            regrex = r'验证码：(\d+)'
            captcha = self.code.waitForMessage(regrex, self.phone)
            if captcha is None:
                print("getMessage failed,try_count:%s" % self.try_count)
                self.try_count += 1
                if self.try_count > 5:
                    return self.exit
                edts[0].click()
                dr.press_keycode(123)
                time.sleep(0.5)
                for i in range(40):
                    dr.press_keycode(67)
                    if edts[0].text == "请输入手机号":
                        break
                return self.signup
            #输入验证码
            edts[1].send_keys(captcha)
            time.sleep(1)
            #点击完成按钮按钮
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.pingan.papd:id/login_btn")).click()
            time.sleep(1)
            try:
                WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.pingan.papd:id/btn_next_step"))
                return self.after_signup
            except TimeoutException:
                #记录帐号密码
                try:
                    with open('/sdcard/1/user%s.log' % self.appname_en, 'a') as f:
                        f.write('\nimei:%s,%s,%s (time %s:%s:%s)' % (self.imei, self.phone, self.pwd, time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour))
                except:
                    with open('D:/brush/slave/scripts/doc/user%s.log' % self.appname_en, 'a') as f:
                        f.write('\nimei:%s,%s,%s (time %s:%s:%s)' % (self.imei, self.phone, self.pwd, time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour))
                time.sleep(3)
                return self.do
        except Exception as e:
            print("error in getPhone,try_count:%s" % self.try_count)
            self.try_count += 1
            if self.try_count > 5:
                self.try_count = 0
                return self.exit
            edts = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_class_name("android.widget.EditText"))
            edts[0].click()
            dr.press_keycode(123)
            time.sleep(0.5)
            for i in range(40):
                dr.press_keycode(67)
                if edts[0].text == "请输入手机号":
                    break
            edts[1].click()
            dr.press_keycode(123)
            time.sleep(0.5)
            for i in range(40):
                dr.press_keycode(67)
                if edts[1].text == "请输入验证码":
                    break
            return self.signup

    def after_signup(self):
        dr = self.driver
        #选择性别
        WebDriverWait(dr, 20).until(lambda d: d.find_element_by_id(choice(["com.pingan.papd:id/rb_sex_female", "com.pingan.papd:id/rb_sex_male"]))).click()
        time.sleep(1)
        #输入昵称
        edts = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
        edts.send_keys(self.get_filemessage("name.txt"))
        time.sleep(1)
        #保存信息按钮
        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.pingan.papd:id/btn_next_step")).click()
        time.sleep(2)
        #选择兴趣
        for x in range(random.randint(1, 3)):
            self.select_one_by_id("com.pingan.papd:id/cb_tag_select")
            time.sleep(1)
        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.pingan.papd:id/btn_tag_select_complete")).click()
        time.sleep(1)
        #检测信息保存完毕跳转页面
        WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.pingan.papd:id/rl_tab_first"))
        time.sleep(2)
        #记录帐号密码
        try:
            with open('/sdcard/1/user%s.log' % self.appname_en, 'a') as f:
                f.write('\nimei:%s,%s,%s (time %s:%s:%s)' % (self.imei, self.phone, self.pwd, time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour))
        except:
            with open('D:/brush/slave/scripts/doc/user%s.log' % self.appname_en, 'a') as f:
                f.write('\nimei:%s,%s,%s (time %s:%s:%s)' % (self.imei, self.phone, self.pwd, time.localtime().tm_mon, time.localtime().tm_mday, time.localtime().tm_hour))
        time.sleep(3)
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
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.pingan.papd:id/rl_tab_first")).click()
                        time.sleep(5)
                        return self.menu1
                    return self.do
                elif random_read == 1:
                    if self.ismenu2:
                        print("goto menu2")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.pingan.papd:id/rl_tab0")).click()
                        time.sleep(5)
                        return self.menu2
                    return self.do
                elif random_read == 2:
                    if self.ismenu3:
                        print("goto menu3")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.pingan.papd:id/rl_tab1")).click()
                        time.sleep(5)
                        return self.menu3
                    return self.do
                elif random_read == 3:
                    if self.ismenu4:
                        print("goto menu4")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.pingan.papd:id/rl_tab2")).click()
                        time.sleep(5)
                        return self.menu4
                    return self.do
                else:
                    if self.ismenu5:
                        print("goto menu5")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.pingan.papd:id/rl_tab3")).click()
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
            self.swipes(300, random.randint(800, 1000), 300, random.randint(300, 600), random.randint(2, 4), random.randint(3, 5))
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
            if random.randint(0, 10000) <= 3000:
                #进入更多问诊类型选择
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("更多")).click()
                time.sleep(5)
                self.swipes(300, random.randint(800, 1000), 300, random.randint(500, 700), random.randint(0, 2), 2)
                selectone = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id("com.pingan.papd:id/tv_department_name"))
                randomnum = random.randint(0, selectone.__len__()-1)
                #获取问诊类型
                question_type = selectone[randomnum].text
                #进入问诊类型选择医生
                selectone[randomnum].click()
                time.sleep(1)
                #选择医生
                self.select_one_by_id("com.pingan.papd:id/rl_top")
                time.sleep(5)
                #点击提问/留言按钮
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.pingan.papd:id/btn_consult")).click()
                time.sleep(5)
                # print(question_type)
                #文档中获取对应问题
                if os.path.exists("D:/brush/slave/scripts/doc/doctor/%s.txt" % question_type):
                    with open("D:/brush/slave/scripts/doc/doctor/%s.txt" % question_type, 'r', encoding="utf-8") as f:
                         strname = f.readlines()
                elif os.path.exists("/sdcard/1/doctor/%s.txt" % question_type):
                    with open("/sdcard/1/doctor/%s.txt" % question_type, 'r', encoding="utf-8") as f:
                         strname = f.readlines()
                else:
                    # strname = ""
                    dr.press_keycode(4)
                    time.sleep(15)
                    self.readnum -= 1
                    self.ismenu2 = False
                    return self.do
                time.sleep(1)
                #选择一个问题
                question = strname[random.randint(0, strname.__len__()-1)].strip()
                #判断提问/留言
                try:
                    WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("问诊:100健康点/15分钟"))
                    time.sleep(5)
                    #确定消费100健康点提问
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.pingan.papd:id/btn_consult")).click()
                    time.sleep(2)
                    dr.tap(550, 1200)
                    time.sleep(1)
                    #输入问题
                    edts = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
                    edts.send_keys(question)
                    time.sleep(1)
                    #下一步按钮
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.pingan.papd:id/inquiry_next_button")).click()
                    time.sleep(5)
                    #选择年龄
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.pingan.plugin.question_v6:id/questioner_age")).click()
                    time.sleep(5)
                    dr.swipe(300, random.randint(650, 850), 300, random.randint(650, 850))
                    time.sleep(1)
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.pingan.plugin.question_v6:id/go_to_consult")).click()
                    time.sleep(2)
                    #提交问题
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.pingan.papd:id/cq_commit")).click()
                    time.sleep(5)
                except TimeoutException:
                    #输入问题
                    edts = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
                    edts.send_keys(question)
                    time.sleep(1)
                    #发送留言
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.pingan.papd:id/tv_right")).click()
                    time.sleep(5)
                time.sleep(random.randint(30, 45))
                #返回上一步
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.pingan.papd:id/tv_left")).click()
                time.sleep(5)
                dr.press_keycode(4)
                time.sleep(1)
                dr.press_keycode(4)
                time.sleep(1)
                dr.press_keycode(4)
                time.sleep(5)
                dr.press_keycode(4)
                time.sleep(1)
            else:
                self.swipes(300, random.randint(800, 1000), 300, random.randint(300, 600), random.randint(2, 4), random.randint(5, 10))
            self.readnum -= 1
            self.ismenu2 = False
        except Exception as e:
            print("error in menu2")
            return self.exception_returnapp()
        return self.do

    def menu3(self):
        dr = self.driver
        try:
            context = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id("com.pingan.papd:id/iv_item_icon"))
            if context.__len__() > 1:
                context.click()
                time.sleep(10)
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.pingan.papd:id/tv_left")).click()
                time.sleep(1)
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
            # self.swipes(300, random.randint(800, 1000), 300, random.randint(300, 500), random.randint(0, 2), random.randint(2, 5))
            dr.press_keycode(4)
            time.sleep(1)
            self.ismenu4 = False
        except Exception as e:
            print("error in menu4")
            return self.exception_returnapp()
        return self.do

    def menu5(self):
        dr = self.driver
        try:
            #一键关注
            try:
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.pingan.papd:id/btn_attention_all")).click()
                time.sleep(5)
            except TimeoutException:
                pass
            # self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(1, 5), random.randint(3, 7))
            #选择其中一个消息查看
            # self.select_one_by_id("com.pingan.papd:id/subject_submitter_name")
            # time.sleep(random.randint(5, 15))
            # self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(3, 5), random.randint(2, 5))
            # #随机评论
            # if random.randint(0, 1):
            #     try:
            #         #随机获取其他人的评论
            #         selectone = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id("com.pingan.papd:id/tv_content"))
            #         content = selectone[random.randint(0, selectone.__len__()-1)].text
            #         #打开评论输入框
            #         WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.pingan.papd:id/tv_send")).click()
            #         #输入评论
            #         edts = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
            #         edts.send_keys(content)
            #         time.sleep(1)
            #         #点击确定按钮
            #         WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.pingan.papd:id/msg_send")).click()
            #         time.sleep(5)
            #     except TimeoutException:
            #         pass
            # dr.press_keycode(4)
            # time.sleep(2)
            # #随机查看健康圈其他内容
            # WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name(choice(["我关注的", "圈子", "发现"]))).click()
            # time.sleep(5)
            # self.swipes(300, random.randint(500, 700), 300, random.randint(800, 1000), random.randint(1, 1), random.randint(2, 5))
            self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(4, 6), random.randint(5, 15))
            dr.press_keycode(4)
            time.sleep(1)
            self.readnum -= 1
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
        self.appname = "平安好医生"       #app名字
        self.appname_en = "pingandoctor"     #记录文件用缩写英文名
        self.imei = None

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
        self.begintime = "开始:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        time.sleep(1)
        #检测已进入app
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.pingan.papd:id/iv_guide_1"))
        self.begintime = "开始:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        time.sleep(random.randint(5, 15))
        return self.ends

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
                f.write('\n留存 %s.%s, %s, %s' % (time.localtime().tm_mon, time.localtime().tm_mday, self.begintime, self.endstime))
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
            # self.try_count = 0
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

