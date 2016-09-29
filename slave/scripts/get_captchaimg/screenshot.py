#! -*- coding=utf-8 -*-

import time
import subprocess


print("ready")
time.sleep(5)

path = "/sdcard/screenshot.png"
su = subprocess.Popen("su", stdin=subprocess.PIPE)
cmd = "/system/bin/screencap -p %s" % path
print("***************************\n" + cmd)
su.communicate(cmd.encode())

print("ok")