#! -*- coding=utf-8 -*-
import time
import random
import re
from appium4droid import webdriver
from appium4droid.common.exceptions import *
from appium4droid.support.ui import WebDriverWait
from machines.StateMachine import Machine


try:
    from util import reset_wifi, alert
except ImportError:
    reset_wifi = lambda: 1
    alert = lambda: 1


class MachineXHook(Machine):
    def __init__(self, driver, tasks=None, remain_day=1):
        super(MachineXHook, self).__init__(self.setup_task)
        self.driver = driver
        self.task_schedule = [] if tasks is None else tasks
        self.tasks = iter([])
        self.remain_day = remain_day
        self.imei = None
        self.try_count = 0
        self.operator_name = None     #46000中国移动/46001中国联通/46002中国移动/46003中国电信
        self.operator_num = None


    def setup_task(self):
        tasks = []
        for task in self.task_schedule:
            try:
                method = getattr(self, task)
                tasks.append(method)
            except AttributeError:
                print("no such method: %s" % task)
            self.tasks = iter(tasks)
        return self.enter_xposehook

    #进入007
    def enter_xposehook(self):
        print("enter xpose hook")
        dr = self.driver
        dr.press_keycode(3)
        time.sleep(1)
        dr.press_keycode(3)
        time.sleep(1)
        dr.find_element_by_name("XposeHook").click()
        time.sleep(1)
        try:
            xpath = "//android.support.v7.widget.LinearLayoutCompat/android.widget.ImageView"
            dr.find_element_by_xpath(xpath)
        except NoSuchElementException:
            print("wrong page")
            return self.reenter
        return self.do_task

    #重进007
    def reenter(self):
        dr = self.driver
        xpath = "//android.view.View[@package='com.miui.home']"
        Home = dr.find_elements_by_xpath(xpath)  # 寻找miui home界面
        while Home == []:
            dr.press_keycode(4)
            time.sleep(1)
            Home = dr.find_elements_by_xpath(xpath)  # 寻找miui home界面
        return self.enter_xposehook

    #退出007
    def exit_xposehook(self):
        dr = self.driver
        xpath = "//android.view.View[@package='com.miui.home']"
        Home = dr.find_elements_by_xpath(xpath)  # 寻找miui home界面
        while Home == []:
            dr.press_keycode(4)
            time.sleep(1)
            Home = dr.find_elements_by_xpath(xpath)  # 寻找miui home界面
        return self.exit

    #开始做任务
    def do_task(self):
        try:
            method = next(self.tasks)
            return method
        except StopIteration:
            return self.exit_xposehook

    #一键卸载
    def uninstall_apk(self):
        dr = self.driver
        dr.find_element_by_name("一键卸载").click()
        time.sleep(1)
        dr.find_element_by_name("全选").click()
        time.sleep(1)
        dr.find_element_by_class_name("android.widget.ImageView").click()
        time.sleep(5)
        dr.press_keycode(4)
        time.sleep(1)
        return self.do_task

    #清除数据
    def clear_data(self):
        dr = self.driver
        dr.find_element_by_name("清除数据").click()
        time.sleep(1)
        dr.find_element_by_class_name("android.widget.ImageView").click()
        time.sleep(3)
        dr.press_keycode(4)
        time.sleep(1)
        return self.do_task

    #查找apk
    def find_apk(self):
        dr = self.driver
        dr.find_element_by_name("查找apk").click()
        time.sleep(1)
        dr.find_element_by_class_name("android.widget.ImageView").click()
        time.sleep(1)
        try:
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_id("com.meiriq.xposehook:id/actv_appname")).click()
            time.sleep(1)
            dr.find_element_by_name("删除").click()
            time.sleep(5)
        except TimeoutException:
            pass
        dr.press_keycode(4)
        time.sleep(1)
        return self.do_task

    #清除记录文件
    def record_file(self):
        dr = self.driver
        dr.find_element_by_name("记录文件").click()
        time.sleep(1)
        dr.find_element_by_name("删除").click()
        time.sleep(3)
        dr.press_keycode(4)
        time.sleep(1)
        return self.do_task

    #更换数据
    def replace_data(self):
        dr = self.driver
        dr.find_element_by_name("修改数据").click()
        time.sleep(1)
        try:
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_name("本地数据")).click()
            time.sleep(1)
            WebDriverWait(dr, 10).until(lambda d: d.find_elements_by_class_name("android.widget.TextView"))[1].click()
            time.sleep(1)
            randomdate = WebDriverWait(dr, 10).until(lambda d: d.find_elements_by_class_name("android.widget.TextView"))
            randomdate[random.randint(1, randomdate.__len__()-1)].click()
            time.sleep(1)
            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("保存")).click()
            time.sleep(1)
        except TimeoutException:
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            dr.find_element_by_name("网络获取失败,退出重新调VPN")
        #获取imei
        edts = dr.find_elements_by_class_name("android.widget.EditText")
        if edts.__len__() > 6:
            self.imei = edts[9].text
        else:
            self.imei = edts[0].text
        print('imei:' + self.imei)
        dr.press_keycode(4)
        time.sleep(1)
        return self.do_task

    #修改数据
    def modify_data(self):
        dr = self.driver
        dr.find_element_by_name("修改数据").click()
        time.sleep(1)
        xpath = "//android.widget.Spinner/android.widget.TextView"
        spinners = dr.find_elements_by_xpath(xpath)
        self.remain_day = spinners[1].text.split(":")[1]
        #获取旧imei
        imei_xpath = "//android.widget.LinearLayout[@resource-id='com.meiriq.xposehook:id/til_device_id']/android.widget.EditText"
        imei = dr.find_element_by_xpath(imei_xpath)
        oldimei = imei.text
        if self.remain_day == '1':
            dr.find_element_by_name("网络获取").click()
        elif self.remain_day == '0':
            dr.press_keycode(4)
            time.sleep(60)
            return self.modify_data
        else:
            dr.find_element_by_name("本地获取").click()
        try:
            save = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("保存"))
            save.click()
        except TimeoutException:
            self.try_count += 1
            if self.try_count <= 3:
                dr.press_keycode(4)
                time.sleep(1)
                dr.press_keycode(4)
                time.sleep(1)
                return self.modify_data
            self.try_count = 0
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            raise Exception("网络获取数据失败重新开始")
        time.sleep(1)
        #获取新imei
        self.imei = imei.text
        print('imei:' + self.imei)
        #检测留存是否已做完
        if oldimei == self.imei:
            dr.press_keycode(4)
            print("留存已跑完挂机300s")
            time.sleep(300)
            raise Exception("挂机完成重新开始")
        dr.press_keycode(4)
        time.sleep(1)
        return self.do_task

    #修改数据_随机
    def modify_data_suiji(self):
        dr = self.driver
        dr.find_element_by_name("修改数据").click()
        time.sleep(1)
        xpath = "//android.widget.Spinner/android.widget.TextView"
        spinners = dr.find_elements_by_xpath(xpath)
        self.remain_day = spinners[1].text.split(":")[1]
        #获取旧imei
        imei_xpath = "//android.widget.LinearLayout[@resource-id='com.meiriq.xposehook:id/til_device_id']/android.widget.EditText"
        imei = dr.find_element_by_xpath(imei_xpath)
        oldimei = imei.text
        if self.remain_day == '1':
            dr.find_element_by_name("随机数据").click()
        elif self.remain_day == '0':
            dr.press_keycode(4)
            time.sleep(60)
            return self.modify_data_suiji
        else:
            dr.find_element_by_name("本地获取").click()
        try:
            save = WebDriverWait(dr, 15).until(lambda d: d.find_element_by_name("保存"))
            save.click()
        except TimeoutException:
            self.try_count += 1
            if self.try_count <= 3:
                dr.press_keycode(4)
                time.sleep(1)
                dr.press_keycode(4)
                time.sleep(1)
                return self.modify_data_suiji
            self.try_count = 0
            dr.press_keycode(4)
            time.sleep(1)
            dr.press_keycode(4)
            time.sleep(1)
            raise Exception("随机获取数据失败重新开始")
        time.sleep(1)
        #获取新imei
        self.imei = imei.text
        print('imei:' + self.imei)
        if oldimei == self.imei:
            dr.press_keycode(4)
            print("留存已跑完挂机300s")
            time.sleep(300)
            raise Exception("挂机完成重新开始")
        dr.press_keycode(4)
        time.sleep(1)
        return self.do_task

    #再激活
    def is0(self):
        dr = self.driver
        dr.find_element_by_name("修改数据").click()
        time.sleep(1)
        xpath = "//android.widget.Spinner/android.widget.TextView"
        spinners = dr.find_elements_by_xpath(xpath)
        self.remain_day = spinners[1].text.split(":")[1]

        if self.remain_day == '0':
            WebDriverWait(dr, 10).until(lambda d: d.find_element_by_name("本地数据")).click()
            time.sleep(1)
            lastdata = WebDriverWait(dr, 10).until(lambda d: d.find_elements_by_class_name("android.widget.TextView"))
            lastdata[lastdata.__len__()-1].click()
            # lastdata[1].click()
            time.sleep(1)
            for i in range(20):
                dr.swipe(300, 800, 300, 200)
                time.sleep(1)
                datetext = WebDriverWait(dr, 10).until(lambda d: d.find_elements_by_class_name("android.widget.TextView"))
                match = None
                for x in range(datetext.__len__()):
                    print("现在钟数:%s点，查找%s点前数据" % (time.localtime().tm_hour, time.localtime().tm_hour-3))
                    if time.localtime().tm_mday > 9:
                        match = re.search(r'2016-03-%s %s(.+)' % (time.localtime().tm_mday, time.localtime().tm_hour-3), datetext[x].text)
                    else:
                        match = re.search(r'2016-03-0%s %s(.+)' % (time.localtime().tm_mday, time.localtime().tm_hour-3), datetext[x].text)
                    if match:
                        print("查询成功,数据是:%s" % match.group(0))
                        break
                    if time.localtime().tm_mday > 9:
                        match = re.search(r'2016-03-%s %s(.+)' % (time.localtime().tm_mday, time.localtime().tm_hour-2), datetext[x].text)
                    else:
                        match = re.search(r'2016-03-0%s %s(.+)' % (time.localtime().tm_mday, time.localtime().tm_hour-2), datetext[x].text)
                    if match:
                        print("查询成功,数据是:%s" % match.group(0))
                        break
                    if time.localtime().tm_mday > 9:
                        match = re.search(r'2016-03-%s %s(.+)' % (time.localtime().tm_mday, time.localtime().tm_hour-1), datetext[x].text)
                    else:
                        match = re.search(r'2016-03-0%s %s(.+)' % (time.localtime().tm_mday, time.localtime().tm_hour-1), datetext[x].text)
                    if match:
                        print("查询成功,数据是:%s" % match.group(0))
                        break
                if match:
                    print("开始寻找3小时前数据")
                    break
            for x in range(random.randint(1, 5)):
                dr.swipe(300, random.randint(200, 400), 300, random.randint(500, 700))
                time.sleep(1)
            time.sleep(1)
            randomdate = WebDriverWait(dr, 10).until(lambda d: d.find_elements_by_class_name("android.widget.TextView"))
            randomdate[random.randint(1, randomdate.__len__()-1)].click()
            time.sleep(1)
            WebDriverWait(dr, 30).until(lambda d: d.find_element_by_name("保存")).click()
            time.sleep(1)
            #获取imei
            imei_xpath = "//android.widget.LinearLayout[@resource-id='com.meiriq.xposehook:id/til_device_id']/android.widget.EditText"
            imei = dr.find_element_by_xpath(imei_xpath)
            self.imei = imei.text
            print('imei:' + self.imei)
            dr.press_keycode(4)
            time.sleep(1)
            return self.exit
        dr.press_keycode(4)
        time.sleep(1)
        return self.do_task

    #更换运营商
    def replace_operator(self):
        dr = self.driver
        dr.find_element_by_name("修改数据").click()
        time.sleep(2)
        dr.swipe(200, 1000, 200, 850)
        time.sleep(1)
        #修改isim
        isim_xpath = "//android.widget.LinearLayout[@resource-id='com.meiriq.xposehook:id/til_isim']/android.widget.EditText"
        edt_isim = dr.find_element_by_xpath(isim_xpath)
        oldisim = edt_isim.text
        newisim = self.operator_num+oldisim[5: 15]
        edt_isim.click()
        time.sleep(0.5)
        dr.press_keycode(123)
        time.sleep(0.5)
        for i in range(40):
            dr.press_keycode(67)
        if not edt_isim.text:
            edt_isim.send_keys(newisim)
        #修改运营商
        operator_num_xpath = "//android.widget.LinearLayout[@resource-id='com.meiriq.xposehook:id/til_operator']/android.widget.EditText"
        edt_operator_num = dr.find_element_by_xpath(operator_num_xpath)
        edt_operator_num.click()
        time.sleep(0.5)
        dr.press_keycode(123)
        time.sleep(0.5)
        for i in range(10):
            dr.press_keycode(67)
        if not edt_operator_num.text:
            edt_operator_num.send_keys(self.operator_num)
        #修改网络类型名
        operator_name_xpath = "//android.widget.LinearLayout[@resource-id='com.meiriq.xposehook:id/til_net_type_name']/android.widget.EditText"
        edt_operator_name = dr.find_element_by_xpath(operator_name_xpath)
        edt_operator_name.click()
        time.sleep(0.5)
        dr.press_keycode(123)
        time.sleep(0.5)
        for i in range(10):
            dr.press_keycode(67)
        if not edt_operator_name.text:
            edt_operator_name.send_keys(self.operator_name)
        time.sleep(1)
        dr.press_keycode(4)
        time.sleep(1)
        return self.do_task


if __name__ == "__main__":
    wd = webdriver.Remote()
    mxh = MachineXHook(wd)
    mxh.task_schedule = ["uninstall_apk", "clear_data", "find_apk", "record_file", "modify_data"]

    mxh.run()
