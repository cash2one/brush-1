import re
import datetime
from email.mime.text import MIMEText
from email.header import Header
from smtplib import SMTP_SSL
import time


yes_time = datetime.datetime.now() + datetime.timedelta(days=-1)
date = yes_time.strftime('20%y-%m-%d')
with open("/sdcard/kind/%s" % date, 'r', encoding='utf-8') as f:
    data_local = f.read()
with open("/sdcard/1/timeshanghai.log", 'r', encoding='utf-8') as f:
    data_run = f.read()
with open("/sdcard/1/timeshanghai2.log", 'r', encoding='utf-8') as f:
    data_run2 = f.read()
with open("/sdcard/1/usershanghai.log", 'r', encoding='utf-8') as f:
    data_sign = f.read()
with open("/sdcard/device.txt", 'r', encoding='utf-8') as f:
    selectuser = f.read()
match_local = re.findall(r'DEVICE', data_local)
match_run = re.findall(r'%s.%s' % (str(int(yes_time.strftime('%m'))), str(int(yes_time.strftime('%d')))), data_run)
match_run2 = re.findall(r'%s.%s' % (str(int(yes_time.strftime('%m'))), str(int(yes_time.strftime('%d')))), data_run2)
match_sign = re.findall(r'%s.%s' % (str(int(yes_time.strftime('%m'))), str(int(yes_time.strftime('%d')))), data_sign)
device_num = re.search(r'(\d+)', selectuser).group(1)
biaoti = "上海观察" + str(device_num)
neirong = yes_time.strftime('%m/%d,') + "本地:" + str(len(match_local)) + "注册:" + str(len(match_sign)) + "体验激活:" + str(len(match_run)) +"体验留存:" + str(len(match_run2))
mail_Info = {
            "from": "493831130@qq.com",
            "to": "825433138@qq.com",
            "hostName": "smtp.qq.com",
            "userName": "493831130@qq.com",
            "password": "qvoaqcjoxucwbghi",
            "mailSubject": "%s" % biaoti,
            "mailText": "%s" % neirong,
            "mailEncoding": "utf-8"
            }
smtp = SMTP_SSL(mail_Info["hostName"])
#ssl登录
smtp.set_debuglevel(1)
smtp.ehlo(mail_Info["hostName"])
smtp.login(mail_Info["userName"], mail_Info["password"])

msg = MIMEText(mail_Info["mailText"], "html", mail_Info["mailEncoding"])
msg["Subject"] = Header(mail_Info["mailSubject"], mail_Info["mailEncoding"])
msg["From"] = mail_Info["from"]
msg["To"] = mail_Info["to"]
smtp.sendmail(mail_Info["from"], mail_Info["to"], msg.as_string())
smtp.quit()