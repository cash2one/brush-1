#! -*- coding=utf-8 -*-


############################记录文件#########################################################################################################
# import logging
# import random
# from random import choice
# logging.basicConfig(filename='/sdcard/com.hipipal.qpyplus/scripts3/slave/scripts/zhs.log', level=logging.DEBUG)
# logging.basicConfig(filename='logtest.log', level=logging.DEBUG)
# def logtest():
#     phone_num = 321321321321
#     # 随机输入密码
#     signpwdli = ["1","2","3","4","5","6","7","8","9","0",
#                 "a","b","c","d","e","f","g","h","i","j",
#                 "1","2","3","4","5","6","7","8","9","0",
#                 "k","l","m","n","o","p","q","r","s","t",
#                 "u","v","w","x","y","z"]
#     signpwd = choice(signpwdli)+choice(signpwdli)+choice(signpwdli)+choice(signpwdli)+choice(signpwdli)+choice(signpwdli)
#     imei = "A120FSDF321"
#     logging.info("%s,%s,%s" % (imei,phone_num,signpwd))
#     # print("记录完毕")
#
# if __name__ == "__main__":
#     logtest()


############################读取文件##########################################################################################################
# import random
# def getName():
#     # f = open('name.txt','r')
#     with open('/sdcard/com.hipipal.qpyplus/scripts3/slave/scripts/name.txt','r',encoding='utf-8') as f:
#         name_list = f.readlines()
#     # f.close()
#     selectname = name_list[random.randint(0,name_list.__len__()-1)]
#     return selectname
#
# if __name__ == "__main__":
#     print(getName())


############################爬虫##########################################################################################################
# import re
# from urllib import request
#
# def getHtml(url):
#     with request.urlopen(url) as page:
#         html = page.read()
#         print(html)
#         return html
# def getImg(html):
#     reg = r'src="(.+?\.jpg)" pic_ext'
#     imgre = re.compile(reg)
#     # print(imgre)
#     imglist = re.findall(imgre,html)
#     x = 0
#     for imgurl in imglist:
#         request.urlretrieve(imgurl,'%s.jpg' % x)
#         x+=1
#
# if __name__ == "__main__":
#     html = getHtml("https://www.baidu.com/")
#     print(getImg(html))


############################图片处理##########################################################################################################
# from PIL import Image, ImageDraw, ImageFont, ImageFilter
#
# import random
#
# # 随机字母:
# def rndChar():
#     return chr(random.randint(65, 90))
#
# # 随机颜色1:
# def rndColor():
#     return (random.randint(64, 255), random.randint(64, 255), random.randint(64, 255))
#
# # 随机颜色2:
# def rndColor2():
#     return (random.randint(32, 127), random.randint(32, 127), random.randint(32, 127))
#
# # 240 x 60:
# width = 60 * 4
# height = 60
# image = Image.new('RGB', (width, height), (255, 255, 255))
# # 创建Font对象:
# # font = ImageFont.truetype('Arial.ttf', 36)
# font = ImageFont.truetype('c:/Windows/Fonts/Arial.ttf',39)
# # font = ImageFont.truetype('c:/Windows/Fonts/simsun.ttc',36)
# # 创建Draw对象:
# draw = ImageDraw.Draw(image)
# # 填充每个像素:
# for x in range(width):
#     for y in range(height):
#         draw.point((x, y), fill=rndColor())
# # 输出文字:
# for t in range(4):
#     draw.text((60 * t + 10, 10), str(random.randint(0,9)), font=font, fill=rndColor2())
# # 模糊:
# image = image.filter(ImageFilter.BLUR)
# image.save('code.jpg', 'jpeg')


############################截屏##########################################################################################################
# from PIL import Image, ImageDraw, ImageFont, ImageFilter
# import  requests
# import time
#
# def downloadImg():
#     pic_file = int(time.time())
#     pic_url = "https://kyfw.12306.cn/otn/passcodeNew/getPassCodeNew?module=login&rand=sjrand"
#     print('[+] Download Picture: {}'.format(pic_url))
#     try:
#         resp = requests.get(pic_url, verify=False, timeout=5)
#     except:
#         resp = requests.get(pic_url, verify=False, timeout=3)
#     with open("./12306_pic/%s.jpg"%pic_file, 'wb') as fp:
#         fp.write(resp.content)
#     return pic_file
#
# def imgCut():
#     pic_file = downloadImg()
#     pic_path = "./12306_pic/%s.jpg" % pic_file
#     pic_text_path = './12306_pic/%s_text.jpg' % pic_file
#     pic_obj = Image.open(pic_path)
#     box = (120,0,290,25)
#     region = pic_obj.crop(box)
#     region.save(pic_text_path)
#     print('[*] Picture Text Picture: {}'.format(pic_text_path))
#     return pic_path, pic_text_path

# >>> from pytesser import *
# >>> image = Image.open('fnord.tif')  # Open image object using PIL
# >>> print image_to_string(image)     # Run tesseract.exe on image
# fnord
# >>> print image_file_to_string('fnord.tif')
# fnord
# dict_list = {}
# count = 0
# for y in range(2):
#     for x in range(4):
#         count += 1
#         im2 = get_sub_img(pic_path, x, y)
#         result = baidu_stu_lookup(im2)
#         dict_list[count] = result
#         print (y,x), result

# import os
# PATH = lambda p: os.path.abspath(p)
#
# def screenshot():
#     path = PATH("%s/screenshot" %os.getcwd())
#     utils.shell("screencap -p /data/local/tmp/tmp.png").wait()
#     if not os.path.isdir(path):
#         os.makedirs(path)
#
#     utils.adb("pull /data/local/tmp/tmp.png %s" %PATH("%s/%s.png" %(path, utils.timestamp()))).wait()
#     utils.shell("rm /data/local/tmp/tmp.png")
#
# if __name__ == "__main__":
#     screenshot()
#     print "success"


############################获取图片验证码##########################################################################################################
# import urllib2
# import re
#
# try:
#   while True:
#     ipaddr = raw_input("Enter IP Or Domain Name:")
#     if ipaddr == "" or ipaddr == 'exit':
#       break
#     else:
#       url = "http://www.ip138.com/ips138.asp?ip=%s&action=2" % ipaddr
#       u = urllib2.urlopen(url)
#       s = u.read()
#       #Get IP Address
#       ip = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',s)
#       print "\n****** Below Result From IP138 Database *****"
#       print "IP Address:",ip[0]
#       #Get IP Address Location
#       result = re.findall(r'(<li>.*?</li>)',s)
#       for i in result:
#         print i[4:-5]
#       print "*"*45
#       print "\n"
#
# except:
#   print "Not Data Find"

# import win32clipboard as w
# import win32con
#
# def getText():
#     w.OpenClipboard()
#     d = w.GetClipboardData(win32con.CF_TEXT)
#     w.CloseClipboard()
#     return d
#
# def setText(aString):
#     w.OpenClipboard()
#     w.EmptyClipboard()
#     w.SetClipboardData(win32con.CF_TEXT, aString)
#     w.CloseClipboard()
#
# if __name__ == "__main__":
#     print(getText())


#######获取IP#################################################################################################################################
# -*- coding: utf-8 -*-
# import re
# import requests
# def getPublicIp():
#     r = requests.get('http://checkip.dyndns.com/')
#     ip = re.search(r'Address: (.{1,20})</body>', r.text)
#     if ip:
#         d = requests.get('http://ip.taobao.com/service/getIpInfo.php?ip=%s' % ip.group(1))
#         d.encoding('utf-8')
#         print(d.text)
#         with open('123.log', 'a') as f:
#                 f.write(d.text)
#         return ip.group(1)
#     else:
#         return None
#
# def checkip(ip):
#     URL = 'http://ip.taobao.com/service/getIpInfo.php'
#     try:
#         r = requests.get(URL, params=ip, timeout=3)
#     except requests.RequestException as e:
#         print(e)
#     else:
#         json_data = r.json()
#         if json_data[u'code'] == 0:
#             print('所在国家： ' + json_data[u'data'][u'country'].encode('utf-8'))
#             print('所在地区： ' + json_data[u'data'][u'area'].encode('utf-8'))
#             print('所在省份： ' + json_data[u'data'][u'region'].encode('utf-8'))
#             print('所在城市： ' + json_data[u'data'][u'city'].encode('utf-8'))
#             print('所属运营商：' + json_data[u'data'][u'isp'].encode('utf-8'))
#         else:
#             print('查询失败,请稍后再试！')
#     pass
# # print(getPublicIp())
# ip = {'ip': '113.64.47.52'}
# checkip(ip)


#######爬虫2#################################################################################################################################
# import requests
# import re
# import random
#
# getnum = 2
# WEB_URL = 'http://m.tduanzi.com/?page=%s' %random.randint(1, 200)
# while getnum:
#     getnum -= 1
#     try:
#         r = requests.get(WEB_URL)  # 发送请求
#         with open("pachong.txt", 'w') as fd:
#             fd.write(r.text)
#         with open("pachong.txt", 'r') as f:
#             a = f.readlines()
#         alen = a.__len__()
#         regrex = r'<span style="font-size: 16px;">(.{1,100})</span>'
#         while alen:
#             alen -= 1
#             msg = a[alen]
#             match = re.search(regrex, msg)
#             if match:
#                 print(match.group(1))
#                 with open("duanzi.txt", 'a', encoding='utf-8') as f:
#                     f.write(match.group(1)+'\n')
#     except:
#         pass
#     print(getnum)


################################备份还原移动008数据###################################################################
# from util import killapp
# from util import movefile, copyfile, removefile
# # copyfile("/sdcard/008backUp/*", "/sdcard/008backUp2/")
# # removefile("/sdcard/008backUp/*")
# copyfile("/sdcard/008backUp2/*__353163058488551", "/sdcard/008backUp/")
# removefile("/sdcard/008backUp2/*__353163058488551")

# movefile("/sdcard/008backUp/", "/sdcard/008backUp2/")
# killapp('com.iplay.assistant')
# /sdcard/1/name.txt


##################################弹框#################################################################
# import time
# try:
#     # import sl4a
#     import android
# except ImportError:
#     pass
# try:
#     while 1:
#         # droid = sl4a.Android()
#         droid = android.Android()
#         droid.makeToast('begin:%s,%s' % (time.localtime().tm_hour, time.localtime().tm_min))
#         time.sleep(1)
# except:
#     pass


###################################后台安装apk################################################################
# from util import install
# install('友寻02-241.apk')
# from util import shock
# import time
# for x in range(3):
#     print("5s alert:" + str(x))
#     time.sleep(5)
#     shock(1)


###################################查找内容################################################################
# import re
# import time
# with open("54.log", 'r', encoding='utf-8') as f:
#     a = f.read()
# match = re.findall(r'激活 %s.%s' % (time.localtime().tm_mon, time.localtime().tm_mday), a)
# print(match.__len__())


####################################后台剪贴板输入文字###############################################################
# from util import settext_clipboard
# import time
# time.sleep(5)
# settext_clipboard("asd")
# time.sleep(1)
# print("ok")


##############################知乎爬虫#####################################################################
# from pachong.pazhihu import ZhihuClient
#
# Cookies_File = 'cookies.json'
#
# client = ZhihuClient(Cookies_File)
#
# url = 'http://www.zhihu.com/question/24825703'
# question = client.question(url)
#
# print(question.title)
# print(question.answer_num)
# print(question.follower_num)
# print(question.topics)
#
# for answer in question.answers:
#     print(answer.author.name, answer.upvote_num)


#########################多部手机传文件##########################################################################
# import os
# import re
# def getPhoneInfo():
#     dviceUdid = []
#     os.system('adb devices > devices.txt')
#     fp = open('devices.txt', 'r+')
#     text = fp.readlines()
#     print(text)
#     for el in text[1:-1]:
#         list = re.split('\\t', el)
#         dviceUdid.append(list[0])
#     if len(dviceUdid) == 0:
#         return False
#
#     return dviceUdid
# getPhoneInfo()


#########################多部手机传文件##########################################################################
# public static void setLockPattern(AppiumDriver driver) throws Exception{
#     List<WebElement> view = Toolkit.waifForExistence("//android.view.View[contains(@resource-id,'view_lock_pattern')]",driver);
#     WebElement welem = view.get(0);
#     int startX = welem.getLocation().getX();
#     int startY = welem.getLocation().getY();
#     int height = welem.getSize().getHeight();
#     int width = welem.getSize().getWidth();
#     int yStep = height / 4;
#     int beginX = (2 * startX + width) / 2;
#     int beginY = startY + yStep;
#
#     //手势密码设置
#     logger.info("开始设置手势密码，中间垂直直线 上->下");
#     TouchAction touchAction1 = new TouchAction(driver);
#     touchAction1.press(beginX,beginY).moveTo(0,yStep).moveTo(0,yStep).release().perform();
#     Toolkit.wait(1);
#     logger.info("再次设置手势密码，中间垂直直线 上->下");
#     touchAction1.press(beginX,beginY).moveTo(0,yStep).moveTo(0,yStep).release().perform();
#     logger.info("手势密码设置完毕");
# }


#########################日期##########################################################################
# import time
# time.strftime('%Y%m%d')
# 获取了当前时间的年月日

# 获取昨天的时间datetime

# import datetime
# now_time = datetime.datetime.now()
# yes_time = now_time + datetime.timedelta(days=-1)
# a = yes_time.strftime('%h-%m-%s')

# begin_time = datetime.datetime.now()
# end_time = datetime.datetime.now()
# end_time2 = begin_time + datetime.timedelta(hours=8, minutes=45)
# end_time3 = begin_time + datetime.timedelta(hours=8, minutes=46)
# a = (end_time - begin_time).seconds


#########################图片验证码##########################################################################
# from PIL import Image
# import pytesseract
# image = Image.open('caca.png')
# print(image)
# print(pytesseract.image_to_string('caca1.png'))
# print(pytesseract.image_to_string(image))

# import pytesseract
# from PIL import Image

# image = Image.open('caca.png')
#
# vcode = pytesseract.image_to_string(image)
#
# print(vcode)


#########################文件移动##########################################################################
# import androidhelper
# import time
# import json
# import logging
# import subprocess
# from datetime import datetime
#
#
# def copyfile(file1, file2):
#     su = subprocess.Popen("su", stdin=subprocess.PIPE)
#     cmd = "/system/bin/cp -r %s %s" % (file1, file2)
#     print("***************************\n" + cmd)
#     su.communicate(cmd.encode())
#
# #删除文件
# def removefile(file):
#     su = subprocess.Popen("su", stdin=subprocess.PIPE)
#     cmd = "/system/bin/rm -r %s" % file
#     print("***************************\n" + cmd)
#     su.communicate(cmd.encode())
#
# # removefile("/sdcard/008backUp/*/*/lib")
# # copyfile("data/data/com.huajiao/", "/sdcard/")
# removefile("data/data/com.huajiao/")
# copyfile("sdcard/com.huajiao/", "data/data/")
# time.sleep(2)


#########################服务器##########################################################################

# from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
# import requests
# r = requests.get('http://m008.meiriq.com/phone')
# r.json()


#########################文件数量统计##########################################################################
# import os
#
# count = 0
# path = r'/sdcard/1/1touxiang/'
# for root, dirs, files in os.walk(path):
#     fileLength = len(files)
#     if fileLength != 0:
#         count = count + fileLength
#
# print("File number is: %d" % count)
# try:
#     from util import find_file_num
# except ImportError:
#     find_file_num = lambda: 1
#
# a = find_file_num("/sdcard/1/1touxiang")
# print(a)


#########################修改文本内容##########################################################################
# try:
#     with open('/sdcard/1/qq.txt', 'r', encoding='utf-8') as f:
#         tfile = "/sdcard/1/qq.txt"
#         strqq = f.read()
# except:
#     with open('D:/brush/slave/scripts/doc/qq.txt', 'r', encoding='utf-8') as f:
#         tfile = "D:/brush/slave/scripts/doc/qq.txt"
#         strqq = f.read()
# match = re.search(r'notuse,(\d+,[0-9a-zA-Z\_\@]+)', strqq)
# if match:
#     user = re.search(r'notuse,(\d+)', match.group(0))
#     pwd = re.search(r'notuse,\d+,([0-9a-zA-Z\_\@]+)', match.group(0))
#     try:
#         lines = open(tfile, 'r').readlines()
#         flen = len(lines)
#         for i in range(flen):
#             if match.group(0) in lines[i]:
#                 lines[i] = lines[i].replace(match.group(0), 'use,' + match.group(1))
#                 break
#         open(tfile, 'w').writelines(lines)
#         print("ok")
#     except Exception as e:
#         print(e)
# print(user.group(1))
# print(pwd.group(1))
# modify_txt("D:/brush/slave/scripts/doc/useranjuke2.log", a.group(0), 'use,' + a.group(1))


#########################文件数量统计##########################################################################
# class FoundException(Exception):
#     pass
# class aException(Exception):
#     pass
#
# try:
#     for i in range(5):
#         for j in range(5):
#             for k in range(5):
#                 print("i=%s, j=%s, k=%s" % (i, j, k))
#                 if i == 4 and j == 2 and k == 2:
#                     raise FoundException()
#                 if i == 2 and j == 2 and k == 2:
#                     raise aException()
# except FoundException:
#     print("exit")
# except aException:
#     print("b")
# else:
#     print ('not found')
#########################IP地址##########################################################################
# import requests
# import re
# import os
# WEB_URL = 'http://ip.chinaz.com/getip.aspx'
# # http://www.net.cn/static/customercare/yourip.asp
#
# r = requests.get(WEB_URL)
# print(r.text)
# regrex = r'ip:\'([0-9\.]+)\''
# match = re.search(r'ip:\'(.+)\'\,address:\'(.+)\'', r.text)
# if match:
#     print(match.group(1))
#     print(match.group(2))
#     ip = match.group(1)
#     addr = match.group(2)
#     if os.path.exists("/sdcard/1/ip.log"):
#         with open('/sdcard/1/ip.log', 'a') as f:
#             f.write('\n%s  %s' % (ip, addr))


#########################文本去重##########################################################################
# obuff = []
# for ln in open('D:/brush/slave/scripts/doc/gongsi.txt', encoding='utf-8'):
#     if ln in obuff:
#         continue
#     obuff.append(ln)
# with open('D:/brush/slave/scripts/doc/gongsi2.txt', 'w', encoding='utf-8') as handle:
#     handle.writelines(obuff)

#########################xpath##########################################################################

# from appium4droid import webdriver
# dr = webdriver.Remote()
# imei = dr.find_element_by_xpath("//android.widget.LinearLayout[@resource-id='com.meiriq.xposehook:id/til_device_id']/android.widget.EditText")
# print("imei:" + imei.text)

#########################修改QQ##########################################################################
# import time
# import re
# with open('D:/brush/slave/scripts/doc/qq.txt', 'r', encoding='utf-8') as f:
#     tfile = "D:/brush/slave/scripts/doc/qq.txt"
#     strqq = f.read()
# modify = "use,13108706974,92ar5j (time 10.25  11:15:23)"
# #修改标志QQ使用失败
# try:
#     lines = open(tfile, 'r').readlines()
#     flen = len(lines)
#     for i in range(flen):
#         if modify in lines[i]:
#             lines[i] = lines[i].replace(modify, modify + ',false')
#             break
#     open(tfile, 'w').writelines(lines)
#     print("ok")
# except Exception as e:
#     print(e)

#########################提取文档内容##########################################################################
# import re
# with open("D:/brush/slave/scripts/doc/ailezan.txt", 'r', encoding='utf-8') as f:
#     a = f.read()
# regrex = r'山东24小时----([0-9]+)'
# match = re.findall(regrex, a)
# if match:
#     print(match)
#     with open("D:/brush/slave/scripts/doc/211.txt", 'a', encoding='utf-8') as f:
#         for x in match:
#             f.write(x+'\n')

#########################手机号码归属地##########################################################################
# import re
# import requests
# a = ['15552692074']
# for phone in a:
#     print(phone)
#     WEB_URL = 'http://www.ip138.com:8080/search.asp?mobile=%s&action=mobile' %phone
#     # WEB_URL = 'http://haoma.baidu.com/search?m=%s&mobile=%s' % (phone, phone)
#     r = requests.get(WEB_URL)  # 发送请求
#     # print(r.text.encode('utf-8'))
#     with open("D:/brush/slave/scripts/doc/pachong.txt", 'w', encoding='utf-8') as fd:
#         fd.write(r.text)
    # r.text
    ######################################################################
    # regrex = r'target="_blank">(.{1,100}) </a></span>'
    # match = re.findall(regrex, r.text)
    # if match:
    #     print(match)
    #     with open("D:/brush/slave/scripts/doc/gongsi.txt", 'a', encoding='utf-8') as f:
    #         for x in match:
    #             f.write(x+'\n')

































