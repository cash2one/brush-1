import time
import threading

from appium4droid import webdriver
from bootstrap import setup_boostrap

bootstrap = threading.Thread(target=setup_boostrap)
bootstrap.start()
time.sleep(1)

dr = webdriver.Remote()
dr.press_keycode(63)


# sh /data/data/com.hipipal.qpy3/files/bin/qpython.sh  /sdcard/com.hipipal.qpyplus/scripts3/slave/scripts/imei.py
