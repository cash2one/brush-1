#! -*- coding=utf-8 -*-
import time
import datetime
from appium4droid import webdriver
from appium4droid.common.exceptions import *
from appium4droid.support.ui import WebDriverWait
from machines.StateMachine import Machine
import random

try:
    from util import reset_wifi, alert, copyfile, removefile
except ImportError:
    reset_wifi = lambda: 1
    alert = lambda: 1
    copyfile = lambda: 1
    removefile = lambda: 1


class Machine008(Machine):
    def __init__(self, driver, tasks=None, **kwargs):
        super(Machine008, self).__init__(self.enter_toolbox)
        self.driver = driver
        self.frist_day = 1
        self.enter_excetption_count = 0
        self.task_schedule = ["do_all_one_key", "modify_data"] if tasks is None else tasks
        self.tasks = iter([])
        self.imei = None
        self.remain_rate = []
        self.change = True
        self.NO_NEW_DAY = 2
        self.begin_time_month = 0
        self.begin_time_day = 0
        self.remain_day = 14

    #设置任务
    def enter_toolbox(self):
        tasks = []
        for task in self.task_schedule:
            try:
                method = getattr(self, task)
                tasks.append(method)
            except AttributeError:
                print("no such method: %s" % task)
            self.tasks = iter(tasks)
        return self.enter_008

    #进入008
    def enter_008(self):
        print("enter 008")
        dr = self.driver
        dr.press_keycode(3)
        time.sleep(1)
        dr.press_keycode(3)
        time.sleep(1)
        WebDriverWait(dr, 10).until(lambda d: d.find_element_by_name("008神器0727")).click()
        time.sleep(1)
        #检测已进入008首页
        try:
            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("工具箱"))
        except TimeoutException:
            #检测网络是否正常
            try:
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("请检查当前网络是否可用"))
                time.sleep(1)
                WebDriverWait(dr, 10).until(lambda d: d.find_element_by_name("确定")).click()
                time.sleep(1)
            except TimeoutException:
                pass
            #出错
            try:
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("注意"))
                time.sleep(1)
                WebDriverWait(dr, 10).until(lambda d: d.find_element_by_name("确定")).click()
                time.sleep(1)
            except TimeoutException:
                pass
            return self.onEnterException

        return self.do_toolbox_task

    #退出008
    def exit_008(self):
        dr = self.driver
        xpath = "//android.view.View[@package='com.miui.home']"
        Home = dr.find_elements_by_xpath(xpath)  # 寻找miui home界面
        while Home == []:
            dr.press_keycode(4)
            time.sleep(1)
            try:
                dr.find_element_by_name("确定").click()
            except NoSuchElementException:
                Home = dr.find_elements_by_xpath(xpath)  # 寻找miui home界面
        return self.exit

    #重新进入008
    def reenter_008(self):
        print("Going to exit and reenter")
        dr = self.driver
        xpath = "//android.view.View[@package='com.miui.home']"
        Home = dr.find_elements_by_xpath(xpath)  # 寻找miui home界面
        while Home == []:
            dr.press_keycode(4)
            time.sleep(1)
            try:
                dr.find_element_by_name("确定").click()
            except NoSuchElementException:
                Home = dr.find_elements_by_xpath(xpath)  # 寻找miui home界面
        return self.enter_008

    #出错处理
    def onEnterException(self):
        # dr = self.driver
        self.enter_excetption_count += 1
        if self.enter_excetption_count > 3:
            # alert()
            reset_wifi()
            self.enter_excetption_count = 0
            raise Exception("网络获取数据失败重新开始")
        return self.reenter_008

    #重设任务
    def set_toolbox_task(self, task_list):
        self.task_schedule = task_list

    #执行设置任务
    def do_toolbox_task(self):
        dr = self.driver
        try:
            method = next(self.tasks)
            return method
        except StopIteration:
            dr.press_keycode(3)
            time.sleep(1)
            return self.exit

    #一键卸载
    def uninstall_apk(self):
        dr = self.driver
        dr.find_element_by_name("工具箱").click()
        time.sleep(1)
        dr.find_element_by_name("一键静默卸载").click()
        time.sleep(1)
        dr.find_element_by_name("重置").click()
        time.sleep(1)
        dr.find_element_by_name("选择反选").click()
        time.sleep(1)
        dr.find_element_by_name("一键卸载").click()
        time.sleep(2)
        WebDriverWait(dr, 15).until_not(lambda d: d.find_elements_by_class_name("android.widget.CheckBox") != [])
        dr.press_keycode(4)
        time.sleep(1)
        dr.press_keycode(4)
        time.sleep(1)
        return self.do_toolbox_task

    #一键删除文件夹
    def delete_dir(self):
        dr = self.driver
        dr.find_element_by_name("工具箱").click()
        time.sleep(1)
        dr.find_element_by_name("一键删除文件夹").click()
        time.sleep(1)
        dr.find_element_by_name("删除文件夹").click()
        time.sleep(2)
        dr.press_keycode(4)
        time.sleep(1)
        dr.press_keycode(4)
        time.sleep(1)
        return self.do_toolbox_task

    #一键删除apk
    def delete_apk(self):
        dr = self.driver
        dr.find_element_by_name("工具箱").click()
        time.sleep(1)
        dr.find_element_by_name("一键删除apk").click()
        time.sleep(1)
        dr.find_element_by_name("开始查找").click()
        time.sleep(5)
        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("删除")).click()
        time.sleep(2)
        dr.press_keycode(4)
        time.sleep(1)
        dr.press_keycode(4)
        time.sleep(1)
        return self.do_toolbox_task

    #一键数据清除
    def clear_apk_data(self):
        dr = self.driver
        dr.find_element_by_name("工具箱").click()
        time.sleep(1)
        dr.find_element_by_name("一键数据清除（同时关闭应用）").click()
        time.sleep(1)
        dr.find_element_by_name("一键清除数据").click()
        time.sleep(2)
        dr.press_keycode(4)
        time.sleep(1)
        dr.press_keycode(4)
        time.sleep(1)
        return self.do_toolbox_task

    #清空应用文件操作
    def listen_files(self):
        dr = self.driver
        dr.find_element_by_name("工具箱").click()
        time.sleep(1)
        dr.find_element_by_name("监听应用文件操作").click()
        time.sleep(1)
        dr.find_element_by_name("删除记录中的文件").click()
        time.sleep(2)
        dr.press_keycode(4)
        time.sleep(1)
        dr.press_keycode(4)
        time.sleep(1)
        return self.do_toolbox_task

    #清空监听系统值设置
    def listen_system_values(self):
        dr = self.driver
        dr.find_element_by_name("工具箱").click()
        time.sleep(1)
        dr.find_element_by_name("监听系统值设置").click()
        time.sleep(1)
        dr.find_element_by_name("清除所选").click()
        time.sleep(2)
        dr.press_keycode(4)
        time.sleep(1)
        dr.press_keycode(4)
        time.sleep(1)
        return self.do_toolbox_task

    #一键操作
    def do_all_one_key(self):
        dr = self.driver
        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("工具箱")).click()
        time.sleep(1)
        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("快捷操作")).click()
        time.sleep(1)
        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("一键操作")).click()
        time.sleep(5)
        WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("一键操作"))
        time.sleep(1)
        dr.press_keycode(4)
        time.sleep(1)
        dr.press_keycode(4)
        time.sleep(1)
        return self.do_toolbox_task

    #修改数据
    def modify_data(self):
        dr = self.driver
        WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.soft.apk008v:id/main_centerImg")).click()
        time.sleep(1)
        #0点增加留存记录
        if time.localtime().tm_hour == 0 and time.localtime().tm_min < 15:
            self.add_remain_data()
        #激活
        if self.frist_day:
            dr.find_element_by_name("从网络获取数据").click()
            try:
                save = WebDriverWait(dr, 60).until(lambda d: d.find_element_by_name("保存"))
                self.imei = dr.find_element_by_class_name("android.widget.EditText").text
                save.click()
                time.sleep(1)
                #确定根据日期分类
                try:
                    dr.find_element_by_name("确定").click()
                    time.sleep(1)
                except NoSuchElementException:
                    pass
                dr.press_keycode(4)
                time.sleep(1)
            except TimeoutException:
                #获取数据失败..网络出错
                dr.press_keycode(4)  # keypress back
                time.sleep(1)
                try:
                    dr.find_element_by_name("确定").click()
                    time.sleep(1)
                    dr.press_keycode(4)  # keypress back
                    time.sleep(1)
                except NoSuchElementException:
                    pass
                print("Mode Switch!@")
                return self.onEnterException
        #留存
        else:
            dr.find_element_by_id("com.soft.apk008v:id/menu_remainControl").click()  ## 留存控制按键
            time.sleep(1)
            dr.find_element_by_name("下一条数据").click()
            time.sleep(1)
            try:
                save = dr.find_element_by_name("保存")  # 若到达100%则无法返回上一个页面
                self.imei = dr.find_element_by_class_name("android.widget.EditText").text
                save.click()
                dr.press_keycode(4)
                time.sleep(1)
            except Exception as e:
                if self.change:
                    self.frist_day = 1
                    dr.press_keycode(4)  # keypress back
                    time.sleep(1)
                    dr.press_keycode(4)  # keypress back
                    time.sleep(1)
                    return self.modify_data
                else:
                    self.frist_day = 2
                    dr.press_keycode(4)  # keypress back
                    time.sleep(1)
                    dr.press_keycode(4)  # keypress back
                    time.sleep(1)
                    return self.exit_008()
        return self.do_toolbox_task

    #修改数据&定位
    def modify_data_location(self):
        dr = self.driver
        WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.soft.apk008v:id/main_centerImg")).click()
        time.sleep(1)
        #添加留存记录
        if time.localtime().tm_hour == 0 and time.localtime().tm_min < 15:
            self.add_remain_data()
        # 激活
        if self.frist_day:
            dr.find_element_by_name("从网络获取数据").click()
            try:
                WebDriverWait(dr, 60).until(lambda d: d.find_element_by_name("保存"))
                self.imei = dr.find_element_by_class_name("android.widget.EditText").text
                #定位
                dr.swipe(300, 1000, 300, 200)
                time.sleep(1)
                dr.swipe(300, 1000, 300, 200)
                time.sleep(1)
                dr.find_element_by_id("com.soft.apk008v:id/set_map_buttonSetJiZhan").click()
                time.sleep(1)
                WebDriverWait(dr, 15).until(lambda d: d.find_element_by_id("com.soft.apk008Tool:id/jizhanNew_button_getData")).click()
                time.sleep(1)
                nextpage = WebDriverWait(dr, 30).until(lambda d: d.find_element_by_id("com.soft.apk008Tool:id/jizhanNew_buttonNextPage"))
                for x in range(random.randint(0, 10)):
                    nextpage.click()
                    time.sleep(1)
                for x in range(random.randint(0, 2)):
                    dr.swipe(300, random.randint(800, 1000), 300, random.randint(300, 500))
                    time.sleep(1)
                selectone = WebDriverWait(dr, 15).until(lambda d: d.find_elements_by_id("com.soft.apk008Tool:id/jizhan_new_item_name"))
                selectone[random.randint(0, selectone.__len__()-1)].click()
                time.sleep(2)
                WebDriverWait(dr, 60).until(lambda d: d.find_element_by_name("保存")).click()
                time.sleep(1)
                try:
                    dr.find_element_by_name("确定").click()
                    time.sleep(1)
                except NoSuchElementException:
                    pass
                dr.press_keycode(4)
                time.sleep(1)
            except TimeoutException:
                dr.press_keycode(4)  # keypress back
                time.sleep(0.5)
                try:
                    dr.find_element_by_name("确定").click()
                    time.sleep(1)
                    dr.press_keycode(4)  # keypress back
                    time.sleep(1)
                except NoSuchElementException:
                    pass
                print("Mode Switch!@")
                return self.onEnterException
        #留存
        else:
            dr.find_element_by_id("com.soft.apk008v:id/menu_remainControl").click()  ## 留存控制按键
            time.sleep(1)
            dr.find_element_by_name("下一条数据").click()
            time.sleep(1)
            try:
                save = dr.find_element_by_name("保存")  # 若到达100%则无法返回上一个页面
                self.imei = dr.find_element_by_class_name("android.widget.EditText").text
                save.click()
                dr.press_keycode(4)
                time.sleep(1)
            except Exception as e:
                if self.change:
                    self.frist_day = 1
                    dr.press_keycode(4)  # keypress back
                    time.sleep(1)
                    dr.press_keycode(4)  # keypress back
                    time.sleep(1)
                    return self.modify_data_location
                else:
                    self.frist_day = 2
                    dr.press_keycode(4)  # keypress back
                    time.sleep(1)
                    dr.press_keycode(4)  # keypress back
                    time.sleep(1)
                    return self.exit_008()
        return self.do_toolbox_task

    #获取随机数据
    def modify_data_suiji(self):
        dr = self.driver
        WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.soft.apk008v:id/main_centerImg")).click()
        time.sleep(1)
        if time.localtime().tm_hour == 0 and time.localtime().tm_min < 15:
            self.add_remain_data()
        #激活
        if self.frist_day:
            dr.find_element_by_name("随机生成").click()
            try:
                save = WebDriverWait(dr, 60).until(lambda d: d.find_element_by_name("保存"))
                self.imei = dr.find_element_by_class_name("android.widget.EditText").text
                save.click()
                time.sleep(1)
                #确定根据日期分类
                try:
                    dr.find_element_by_name("确定").click()
                    time.sleep(1)
                except NoSuchElementException:
                    pass
                dr.press_keycode(4)
                time.sleep(1)
            except TimeoutException:
                #获取数据失败..网络出错
                dr.press_keycode(4)  # keypress back
                time.sleep(1)
                try:
                    dr.find_element_by_name("确定").click()
                    time.sleep(1)
                    dr.press_keycode(4)  # keypress back
                    time.sleep(1)
                except NoSuchElementException:
                    pass
                print("Mode Switch!@")
                return self.onEnterException
        #留存
        else:
            dr.find_element_by_id("com.soft.apk008v:id/menu_remainControl").click()  ## 留存控制按键
            time.sleep(1)
            dr.find_element_by_name("下一条数据").click()
            time.sleep(1)
            try:
                save = dr.find_element_by_name("保存")  # 若到达100%则无法返回上一个页面
                self.imei = dr.find_element_by_class_name("android.widget.EditText").text
                save.click()
                dr.press_keycode(4)
                time.sleep(1)
            except Exception as e:
                if self.change:
                    self.frist_day = 1
                    dr.press_keycode(4)  # keypress back
                    time.sleep(1)
                    dr.press_keycode(4)  # keypress back
                    time.sleep(1)
                    return self.modify_data_suiji
                else:
                    self.frist_day = 2
                    dr.press_keycode(4)  # keypress back
                    time.sleep(1)
                    dr.press_keycode(4)  # keypress back
                    time.sleep(1)
                    return self.exit_008()
        return self.exit

    #添加留存记录
    def add_remain_data(self):
        dr = self.driver
        dr.find_element_by_id("com.soft.apk008v:id/menu_remainControl").click()  ## 留存控制按键
        time.sleep(1)
        #清除当前留存记录
        for x in range(60):
            try:
                dr.find_element_by_id("com.soft.apk008v:id/remain_item_title")
                dr.swipe(400, 250, 410, 250, 50)
                WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("确定")).click()
                time.sleep(0.5)
            except NoSuchElementException:
                break
        #添加留存记录
        add_end = False
        find_day = self.NO_NEW_DAY
        for x in range(self.remain_day):
            if add_end:
                break
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.soft.apk008v:id/menu_remain_addRecord")).click()        #添加记录按钮
            time.sleep(0.5)
            # 获取昨天的时间datetime
            begin_time = datetime.datetime.now()
            #设置留存开始时间
            if self.begin_time_month:
                begin_time = begin_time.replace(month=self.begin_time_month)
            if self.begin_time_day:
                begin_time = begin_time.replace(day=self.begin_time_day)
            yes_time = begin_time + datetime.timedelta(days=-x-1)
            #滑动查找
            for i in range(10):
                try:
                    dr.find_element_by_name(yes_time.strftime('%Y-%m-%d')).click()
                    time.sleep(1)
                    edt = dr.find_element_by_class_name("android.widget.EditText")
                    if self.begin_time_month or self.begin_time_day:
                        edt.send_keys(self.remain_rate[x+(datetime.datetime.now()-begin_time).days])
                    else:
                        edt.send_keys(self.remain_rate[x])
                    time.sleep(1)
                    dr.find_element_by_name("确定").click()
                    time.sleep(1)
                    find_day = self.NO_NEW_DAY
                    break
                except NoSuchElementException:
                    dr.swipe(300, 800, 300, 500)
                    time.sleep(1)
                if i == 9:
                    dr.press_keycode(4)
                    time.sleep(1)
                    if find_day == 0:
                        add_end = True
                    else:
                        find_day -= 1
        dr.press_keycode(4)
        time.sleep(1)

    #备份程序
    def backup_app(self):
        dr = self.driver
        dr.find_element_by_name("工具箱").click()
        time.sleep(1)
        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("备份程序数据")).click()
        time.sleep(1)
        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("备份")).click()
        time.sleep(1)
        #检测备份完成
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("备份"))
        #移动备份文件
        copyfile("/sdcard/008backUp/*", "/sdcard/008backUp2/")
        time.sleep(5)
        removefile("/sdcard/008backUp/*")
        time.sleep(5)
        dr.press_keycode(4)
        time.sleep(1)
        dr.press_keycode(4)
        time.sleep(1)
        return self.do_toolbox_task

    #还原程序
    def recovery_app(self):
        dr = self.driver
        dr.find_element_by_name("工具箱").click()
        time.sleep(1)
        try:
            #提取备份文件
            copyfile("/sdcard/008backUp2/*__%s" % self.imei, "/sdcard/008backUp/")
            time.sleep(5)
            removefile("/sdcard/008backUp2/*__%s" % self.imei)
            time.sleep(5)
            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("备份程序数据")).click()
            time.sleep(1)
            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name(self.imei)).click()
            time.sleep(1)
            WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("还原")).click()
            time.sleep(1)
            #检测还原成功
            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name(self.imei))
        except TimeoutException:
            pass
        dr.press_keycode(4)
        time.sleep(1)
        dr.press_keycode(4)
        time.sleep(1)
        return self.do_toolbox_task

    #备份程序
    def backup_app_lib(self):
        dr = self.driver
        dr.find_element_by_name("工具箱").click()
        time.sleep(1)
        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("备份程序数据")).click()
        time.sleep(1)
        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("备份")).click()
        time.sleep(5)
        #检测备份完成
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("备份"))
        #删除lib文件
        removefile("/sdcard/008backUp/*/*/lib")
        time.sleep(2)
        #移动备份文件
        copyfile("/sdcard/008backUp/*", "/sdcard/008backUp2/")
        time.sleep(5)
        removefile("/sdcard/008backUp/*")
        time.sleep(5)
        dr.press_keycode(4)
        time.sleep(1)
        dr.press_keycode(4)
        time.sleep(1)
        return self.do_toolbox_task

    #还原程序
    def recovery_app_lib(self):
        dr = self.driver
        dr.find_element_by_name("工具箱").click()
        time.sleep(1)
        #提取备份文件
        copyfile("/sdcard/008backUp2/*__%s" % self.imei, "/sdcard/008backUp/")
        time.sleep(5)
        copyfile("/sdcard/lib", "/sdcard/008backUp/*/*/")
        time.sleep(5)
        removefile("/sdcard/008backUp2/*__%s" % self.imei)
        time.sleep(5)
        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("备份程序数据")).click()
        time.sleep(1)
        dr.find_element_by_name(self.imei).click()
        time.sleep(1)
        WebDriverWait(dr, 5).until(lambda d: d.find_element_by_name("还原")).click()
        time.sleep(1)
        #检测还原成功
        WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name(self.imei))
        dr.press_keycode(4)
        time.sleep(1)
        dr.press_keycode(4)  # keypress back
        time.sleep(1)
        return self.do_toolbox_task



if __name__ == "__main__":
    pass
    # dr = webdriver.Remote()
    # time.sleep(2)
    # dr.press_keycode(3)
    #
    # # m = Machine008(dr)
    # m = Second008(dr)
    # while True:
    #     m.run()
    #     print("m.second= %s" % m.second_day)
    #     print("Again")

    # m = Machine008(dr)
    # m.task_schedule = ["change_date_dir"]
    # m.run()
