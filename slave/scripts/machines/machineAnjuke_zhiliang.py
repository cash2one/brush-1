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
        self.appname = "安居客"       #app名字
        self.appname_en = "anjuke"     #记录文件用缩写英文名
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
        self.ismenu4 = True
        #选择初始化接码平台
        if self.code_platform == "feima":
            self.code = Feima(self.code_user, self.code_pwd, None)
        elif self.code_platform == "yama":
            self.code = Yama(self.code_user, self.code_pwd, None)
        elif self.code_platform == "yima":
            self.code = Yima(self.code_user, self.code_pwd, None)
        elif self.code_platform == "ailezan":
            self.code = Ailezan(self.code_user, self.code_pwd, 1327)
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
        #检测已进入app
        WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.anjuke.android.app:id/viewGroup"))
        self.begintime = "开始:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        time.sleep(1)
        #新开软件翻页
        self.swipes(600, 300, 300, 300, 4, 2, 2)
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.anjuke.android.app:id/guidePages")).click()
        try:
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("定位失败，请检查网络"))
            self.select_one_by_id("com.anjuke.android.app:id/select_city_tv_item", find_min=1)
            time.sleep(5)
        except TimeoutException:
            pass
        try:
            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.anjuke.android.app:id/autoupdate_no")).click()
            time.sleep(1)
        except TimeoutException:
            pass
        #注册率
        sign_rate = random.randint(1, 10000)
        if sign_rate <= 3000:
            WebDriverWait(dr, 30).until(lambda d: d.find_elements_by_id("com.anjuke.android.app:id/view_maintab_model_icon"))[3].click()
            time.sleep(1)
            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.anjuke.android.app:id/user_photo_civ")).click()
            time.sleep(1)
            return self.login_code_platform
        time.sleep(5)
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
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.anjuke.android.app:id/login_by_phone")).click()
            time.sleep(1)
            #选择接码平台获取手机号码
            self.phone = self.code.getPhone()
            edts = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_class_name("android.widget.EditText"))
            #输入手机号码
            edts[0].send_keys(self.phone)
            time.sleep(1)
            #点击获取验证码按钮
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.anjuke.android.app:id/send_sms_button")).click()
            time.sleep(5)
            #输入密码
            # edts[2].send_keys(self.pwd)
            # time.sleep(1)
            #选择接码平台获取验证码
            #【安居客】亲爱的安居客用户您好，您的验证码为6045，验证码30分钟内有效。(来自106575681095585)
            regrex = r'验证码为(\d+)'
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
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.anjuke.android.app:id/btn_login")).click()
            time.sleep(1)
            #检测注册成功进入下一步
            WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.anjuke.android.app:id/user_name_tv"))
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
        WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.anjuke.android.app:id/user_name_tv")).click()
        time.sleep(1)
        WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.anjuke.android.app:id/personal_info_name_view")).click()
        time.sleep(1)
        #输入昵称
        edts = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
        edts.send_keys(self.get_filemessage("name.txt"))
        time.sleep(1)
        #选择性别
        WebDriverWait(dr, 20).until(lambda d: d.find_element_by_id(choice(["com.anjuke.android.app:id/gender_male_rb", "com.anjuke.android.app:id/gender_female_rb"]))).click()
        time.sleep(1)
        WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.anjuke.android.app:id/btnright")).click()
        time.sleep(1)
        if random.randint(0, 9) == 0:
            #选择头像
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.anjuke.android.app:id/personal_info_portrait_view")).click()
            time.sleep(1)
            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("从相册选择")).click()
            time.sleep(1)
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("1touxiang")).click()
            time.sleep(1)
            self.swipes(300, random.randint(800, 1000), 300, random.randint(300, 500), random.randint(0, 80))
            time.sleep(5)
            self.select_one_by_id("com.anjuke.android.app:id/imgQueue")
            time.sleep(1)
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.anjuke.android.app:id/btnright")).click()
            time.sleep(5)
        #保存信息按钮
        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.anjuke.android.app:id/imagebtnleft")).click()
        time.sleep(5)
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
                random_read = random.randint(0, 3)
                if random_read == 0:
                    if self.ismenu1:
                        print("goto menu1")
                        WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id("com.anjuke.android.app:id/view_maintab_model_icon"))[0].click()
                        time.sleep(5)
                        return self.menu1
                    return self.do
                elif random_read == 1:
                    if self.ismenu2:
                        print("goto menu2")
                        WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id("com.anjuke.android.app:id/view_maintab_model_icon"))[1].click()
                        time.sleep(5)
                        return self.menu2
                    return self.do
                elif random_read == 2:
                    if self.ismenu3:
                        print("goto menu3")
                        WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id("com.anjuke.android.app:id/view_maintab_model_icon"))[2].click()
                        time.sleep(5)
                        return self.menu3
                    return self.do
                else:
                    if self.ismenu4:
                        print("goto menu4")
                        WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id("com.anjuke.android.app:id/view_maintab_model_icon"))[3].click()
                        time.sleep(5)
                        return self.menu4
                    return self.do
        except TimeoutException:
            print("查找菜单出错")
            return self.exception_returnapp()
        print("阅览完毕")
        return self.ends

    def menu1(self):
        dr = self.driver
        try:
            #进入搜索
            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.anjuke.android.app:id/home_title_search_view")).click()
            time.sleep(1)
            try:
                self.select_one_by_id("com.anjuke.android.app:id/searchtype_item_tv")
                time.sleep(1)
            except TimeoutException:
                pass
            search_ci = ["刚需房", "精装修", "不限购", "低首付", "低总价", "南北通透", "婚房", "地铁房", "学区房", "满五唯一",
                         "交通便利", "配套成熟", "小户型", "大户型", "景区", "公园", "改善房", "大客厅", "学校", "银行",
                         "医院", "市场", "广场", "商场", "投资", "大平层", "大主卧", "养老房", "品牌", "公交", "社区",
                         "小区", "洋房", "环境", "得房率高", "安全", "停车", "电梯", "安静", "繁华"]
            #选择分类
            # self.select_one_by_id("com.anjuke.android.app:id/tag_btn")
            edts = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
            edts.send_keys(choice(search_ci))
            time.sleep(1)
            dr.press_keycode(66)
            time.sleep(5)
            #随机搜索房源
            randomnum = random.randint(1, 10000)
            if randomnum < 0:
                read_house_num = random.randint(1, 3)
            elif 0 <= randomnum <= 3000:
                read_house_num = random.randint(4, 6)
            else:
                read_house_num = random.randint(7, 10)
            #选房源查看
            for x in range(read_house_num):
                self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(0, 2), 2, 5)
                self.select_one_by_id("com.anjuke.android.app:id/title", find_min=1)
                time.sleep(random.randint(5, 10))
                self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(1, 3), 2, 5)
                dr.press_keycode(4)
                time.sleep(2)
                if random.randint(0, 4) == 0:
                    try:
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.anjuke.android.app:id/imagebtnright")).click()
                        time.sleep(1)
                    except TimeoutException:
                        pass
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(2, 5), 2, 5)
            # self.select_one_by_id("com.anjuke.android.app:id/title")
            # time.sleep(random.randint(5, 10))
            # self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(1, 2), 2, 10)
            # if random.randint(0, 9) == 0:
            #     try:
            #         WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.anjuke.android.app:id/favorite")).click()
            #         time.sleep(1)
            #     except TimeoutException:
            #         pass
            # dr.press_keycode(4)
            # time.sleep(1)
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
            liread = ["com.anjuke.android.app:id/second_text", "com.anjuke.android.app:id/rent_text", "com.anjuke.android.app:id/new_text"]
            try:
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id(choice(liread))).click()
                time.sleep(5)
            except TimeoutException:
                pass
            self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(2, 5), 2, 5)
            # self.select_one_by_id("com.anjuke.android.app:id/title")
            # time.sleep(random.randint(5, 10))
            # self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(2, 4), 2, 10)
            # if random.randint(0, 19) == 0:
            #     try:
            #         WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.anjuke.android.app:id/favorite")).click()
            #         time.sleep(1)
            #     except TimeoutException:
            #         pass
            # dr.press_keycode(4)
            # time.sleep(1)
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

    def ends(self):
        dr = self.driver
        #二次打开
        for x in range(random.randint(1, 1)):
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
        self.appname = "安居客"       #app名字
        self.appname_en = "anjuke"     #记录文件用缩写英文名
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
        return self.begin

    def begin(self):
        dr = self.driver
        dr.press_keycode(3)
        time.sleep(1)
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name(self.appname)).click()
        time.sleep(10)
        #检测已进入app
        WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.anjuke.android.app:id/viewGroup"))
        self.begintime = "开始:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        time.sleep(1)
        #新开软件翻页
        self.swipes(600, 300, 300, 300, 4, 2, 2)
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.anjuke.android.app:id/guidePages")).click()
        try:
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("定位失败，请检查网络"))
            self.select_one_by_id("com.anjuke.android.app:id/select_city_tv_item", find_min=1)
            time.sleep(5)
        except TimeoutException:
            pass
        try:
            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.anjuke.android.app:id/autoupdate_no")).click()
            time.sleep(1)
        except TimeoutException:
            pass
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
                        WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id("com.anjuke.android.app:id/view_maintab_model_icon"))[0].click()
                        time.sleep(5)
                        return self.menu1
                    return self.do
                elif random_read == 1:
                    if self.ismenu2:
                        print("goto menu2")
                        WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id("com.anjuke.android.app:id/view_maintab_model_icon"))[1].click()
                        time.sleep(5)
                        return self.menu2
                    return self.do
                elif random_read == 2:
                    if self.ismenu3:
                        print("goto menu3")
                        WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id("com.anjuke.android.app:id/view_maintab_model_icon"))[2].click()
                        time.sleep(5)
                        return self.menu3
                    return self.do
                else:
                    if self.ismenu4:
                        print("goto menu4")
                        WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id("com.anjuke.android.app:id/view_maintab_model_icon"))[3].click()
                        time.sleep(5)
                        return self.menu4
                    return self.do
        except TimeoutException:
            print("查找菜单出错")
            return self.exception_returnapp()
        print("阅览完毕")
        return self.ends

    def menu1(self):
        dr = self.driver
        try:
            #进入搜索
            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.anjuke.android.app:id/home_title_search_view")).click()
            time.sleep(1)
            try:
                self.select_one_by_id("com.anjuke.android.app:id/searchtype_item_tv")
                time.sleep(1)
            except TimeoutException:
                pass
            search_ci = ["刚需房", "精装修", "不限购", "低首付", "低总价", "南北通透", "婚房", "地铁房", "学区房", "满五唯一",
                         "交通便利", "配套成熟", "小户型", "大户型", "景区", "公园", "改善房", "大客厅", "学校", "银行",
                         "医院", "市场", "广场", "商场", "投资", "大平层", "大主卧", "养老房", "品牌", "公交", "社区",
                         "小区", "洋房", "环境", "得房率高", "安全", "停车", "电梯", "安静", "繁华"]
            #选择分类
            # self.select_one_by_id("com.anjuke.android.app:id/tag_btn")
            edts = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_class_name("android.widget.EditText"))
            edts.send_keys(choice(search_ci))
            time.sleep(1)
            dr.press_keycode(66)
            time.sleep(5)
            #选房源查看
            for x in range(random.randint(2, 6)):
                self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(0, 2), 2, 5)
                self.select_one_by_id("com.anjuke.android.app:id/title", find_min=1)
                time.sleep(random.randint(5, 10))
                self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(2, 4), 2, 10)
                if random.randint(0, 4) == 0:
                    try:
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.anjuke.android.app:id/imagebtnright")).click()
                        time.sleep(1)
                    except TimeoutException:
                        pass
                dr.press_keycode(4)
                time.sleep(2)
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(2, 5), 2, 5)
            # self.select_one_by_id("com.anjuke.android.app:id/title")
            # time.sleep(random.randint(5, 10))
            # self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(1, 2), 2, 10)
            # if random.randint(0, 9) == 0:
            #     try:
            #         WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.anjuke.android.app:id/favorite")).click()
            #         time.sleep(1)
            #     except TimeoutException:
            #         pass
            # dr.press_keycode(4)
            # time.sleep(1)
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
            liread = ["com.anjuke.android.app:id/second_text", "com.anjuke.android.app:id/rent_text", "com.anjuke.android.app:id/new_text"]
            try:
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id(choice(liread))).click()
                time.sleep(5)
            except TimeoutException:
                pass
            self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(2, 5), 2, 5)
            # self.select_one_by_id("com.anjuke.android.app:id/title")
            # time.sleep(random.randint(5, 10))
            # self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(2, 4), 2, 10)
            # if random.randint(0, 19) == 0:
            #     try:
            #         WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.anjuke.android.app:id/favorite")).click()
            #         time.sleep(1)
            #     except TimeoutException:
            #         pass
            # dr.press_keycode(4)
            # time.sleep(1)
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

    def ends(self):
        dr = self.driver
        #二次打开
        for x in range(random.randint(1, 1)):
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

