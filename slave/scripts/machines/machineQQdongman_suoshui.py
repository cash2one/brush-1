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
        self.appname = "腾讯动漫"       #app名字
        self.appname_en = "qqdongman"     #记录文件用缩写英文名
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

        return self.begin

    def begin(self):
        dr = self.driver
        dr.press_keycode(3)
        time.sleep(1)
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name(self.appname)).click()
        time.sleep(10)
        #检测更新
        try:
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/btn_cancel")).click()
        except TimeoutException:
            pass
        #检测已进入app
        WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/rel_main"))
        self.begintime = "开始:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        time.sleep(1)
        #新开软件翻页
        self.swipes(600, 300, 300, 300, 3, 2, 2)
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/rel_main")).click()
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
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/tab_icon_recommend")).click()
                        time.sleep(5)
                        return self.menu1
                    return self.do
                elif random_read == 1:
                    if self.ismenu2:
                        print("goto menu2")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/tab_icon_bookshelf")).click()
                        time.sleep(5)
                        return self.menu2
                    return self.do
                elif random_read == 2:
                    if self.ismenu3:
                        print("goto menu3")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/tab_icon_square")).click()
                        time.sleep(5)
                        return self.menu3
                    return self.do
                else:
                    if self.ismenu4:
                        print("goto menu4")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/tab_icon_center")).click()
                        time.sleep(5)
                        return self.menu4
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
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("分类")).click()
            time.sleep(1)
            #选择分类
            self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(0, 1), 2, 5)
            selectone = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id(choice(["com.qq.ac.android:id/class_img_left", "com.qq.ac.android:id/class_img_right"])))
            selectone[random.randint(0, selectone.__len__()-2)].click()
            time.sleep(5)
            #选择动漫
            for i in range(random.randint(2, 2)):
                self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(0, 2), 2, 5)
                try:
                    self.select_one_by_id("com.qq.ac.android:id/top_title")
                    time.sleep(5)
                    #开始阅读
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/tv_start_read")).click()
                    time.sleep(5)
                    #初次阅读教程
                    try:
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/iv_guide_comment")).click()
                        time.sleep(1)
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/iv_guide_more")).click()
                        time.sleep(1)
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/iv_guide_more_list")).click()
                        time.sleep(1)
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/iv_guide_download")).click()
                        time.sleep(1)
                    except TimeoutException:
                        pass
                    for x in range(random.randint(10, 15)):
                        dr.swipe(300, random.randint(800, 1000), 300, random.randint(400, 600))
                        time.sleep(random.randint(2, 5))
                    dr.press_keycode(4)
                    time.sleep(1)
                    try:
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/btn_cancel")).click()
                        time.sleep(1)
                    except TimeoutException:
                        pass
                    #收藏
                    # if random.randint(0, 9) == 0:
                    #     try:
                    #         WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/lin_favorite")).click()
                    #         time.sleep(1)
                    #     except TimeoutException:
                    #         pass
                except TimeoutException:
                    try:
                        #进入条漫返回
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_class_name("android.webkit.WebView"))
                        time.sleep(1)
                        dr.press_keycode(4)
                        time.sleep(1)
                        return self.menu1()
                    except TimeoutException:
                        self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(0, 2), 2, 5)
                        self.select_one_by_id("com.qq.ac.android:id/animation_cover")
                        time.sleep(random.randint(180, 240))
                        break
                dr.press_keycode(4)
                time.sleep(1)
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
            for x in range(random.randint(5, 10)):
                dr.swipe(300, random.randint(800, 1000), 300, random.randint(400, 600))
                time.sleep(random.randint(2, 10))
                #点赞
                # if random.randint(0, 9) == 0:
                #     try:
                #         WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/good_img")).click()
                #         time.sleep(1)
                #         try:
                #             WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/btn_actionbar_back")).click()
                #             time.sleep(1)
                #         except TimeoutException:
                #             pass
                #     except TimeoutException:
                #         pass
                #进入查看
                if random.randint(0, 9) == 0:
                    try:
                        self.select_one_by_id("com.qq.ac.android:id/title")
                        time.sleep(random.randint(5, 10))
                        self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(2, 5), 5, 10)
                        dr.press_keycode(4)
                        time.sleep(1)
                        break
                    except TimeoutException:
                        pass
            self.readnum -= 1
            self.ismenu3 = False
        except Exception as e:
            print("error in menu3")
            return self.exception_returnapp()
        return self.do

    def menu4(self):
        dr = self.driver
        try:
            try:
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/iv_guide_setting")).click()
                time.sleep(1)
                dr.press_keycode(4)
                time.sleep(1)
            except TimeoutException:
                pass
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
        try:
            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("残忍拒绝")).click()
            time.sleep(1)
        except TimeoutException:
            pass
        return self.do


class Machinex2(Machine):
    def __init__(self, driver):
        super(Machinex2, self).__init__(self.initdata)
        self.driver = driver
        self.appname = "腾讯动漫"       #app名字
        self.appname_en = "qqdongman"     #记录文件用缩写英文名
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
        time.sleep(15)
        #检测已进入app
        # WebDriverWait(dr, 60).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/rel_main"))
        self.begintime = "开始:%s:%s:%s" % (time.localtime().tm_hour, time.localtime().tm_min, time.localtime().tm_sec)
        time.sleep(1)
        #检测更新
        try:
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/btn_cancel")).click()
            time.sleep(5)
        except TimeoutException:
            pass
        try:
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/rel_main"))
            time.sleep(1)
            #新开软件翻页
            self.swipes(600, 300, 300, 300, 3, 2, 2)
        except TimeoutException:
            pass
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
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/tab_icon_recommend")).click()
                        time.sleep(5)
                        return self.menu1
                    return self.do
                elif random_read == 1:
                    if self.ismenu2:
                        print("goto menu2")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/tab_icon_bookshelf")).click()
                        time.sleep(5)
                        return self.menu2
                    return self.do
                elif random_read == 2:
                    if self.ismenu3:
                        print("goto menu3")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/tab_icon_square")).click()
                        time.sleep(5)
                        return self.menu3
                    return self.do
                else:
                    if self.ismenu4:
                        print("goto menu4")
                        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/tab_icon_center")).click()
                        time.sleep(5)
                        return self.menu4
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
            WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("分类")).click()
            time.sleep(1)
            #选择分类
            self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(0, 2), 2, 5)
            selectone = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id(choice(["com.qq.ac.android:id/class_img_left", "com.qq.ac.android:id/class_img_right"])))
            selectone[random.randint(0, selectone.__len__()-1)].click()
            time.sleep(5)
            #选择动漫
            for i in range(random.randint(1, 2)):
                self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(0, 1), 2, 5)
                try:
                    self.select_one_by_id("com.qq.ac.android:id/top_title", find_time=5)
                    time.sleep(5)
                    #开始阅读
                    WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/tv_start_read")).click()
                    time.sleep(5)
                    #初次阅读教程
                    try:
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/iv_guide_comment")).click()
                        time.sleep(1)
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/iv_guide_more")).click()
                        time.sleep(1)
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/iv_guide_more_list")).click()
                        time.sleep(1)
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/iv_guide_download")).click()
                        time.sleep(1)
                    except TimeoutException:
                        pass
                    for x in range(random.randint(10, 15)):
                        dr.swipe(300, random.randint(800, 1000), 300, random.randint(400, 600))
                        time.sleep(random.randint(2, 5))
                    dr.press_keycode(4)
                    time.sleep(1)
                    try:
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/btn_cancel")).click()
                        time.sleep(1)
                    except TimeoutException:
                        pass
                    #收藏
                    # if random.randint(0, 9) == 0:
                    #     try:
                    #         WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/lin_favorite")).click()
                    #         time.sleep(1)
                    #     except TimeoutException:
                    #         pass
                except TimeoutException:
                    try:
                        #进入条漫返回
                        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_class_name("android.webkit.WebView"))
                        time.sleep(1)
                        dr.press_keycode(4)
                        time.sleep(1)
                        return self.menu1()
                    except TimeoutException:
                        self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(0, 2), 2, 5)
                        self.select_one_by_id("com.qq.ac.android:id/animation_cover")
                        time.sleep(random.randint(60, 150))
                        break
                dr.press_keycode(4)
                time.sleep(1)
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
            for x in range(random.randint(5, 10)):
                dr.swipe(300, random.randint(800, 1000), 300, random.randint(400, 600))
                time.sleep(random.randint(2, 10))
                #点赞
                # if random.randint(0, 9) == 0:
                #     try:
                #         WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/good_img")).click()
                #         time.sleep(1)
                #         try:
                #             WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/btn_actionbar_back")).click()
                #             time.sleep(1)
                #         except TimeoutException:
                #             pass
                #     except TimeoutException:
                #         pass
                #进入查看
                if random.randint(0, 9) == 0:
                    try:
                        self.select_one_by_id("com.qq.ac.android:id/title")
                        time.sleep(random.randint(5, 10))
                        self.swipes(300, random.randint(800, 1000), 300, random.randint(400, 600), random.randint(2, 5), 5, 10)
                        dr.press_keycode(4)
                        time.sleep(1)
                        break
                    except TimeoutException:
                        pass
            self.readnum -= 1
            self.ismenu3 = False
        except Exception as e:
            print("error in menu3")
            return self.exception_returnapp()
        return self.do

    def menu4(self):
        dr = self.driver
        try:
            try:
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_id("com.qq.ac.android:id/iv_guide_setting")).click()
                time.sleep(1)
                dr.press_keycode(4)
                time.sleep(1)
            except TimeoutException:
                pass
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
        try:
            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("残忍拒绝")).click()
            time.sleep(1)
        except TimeoutException:
            pass
        return self.do



if __name__ == "__main__":
    wd = webdriver.Remote()
    time.sleep(2)

