#! -*- coding=utf-8 -*-

import os
import sys
from PIL import Image

def getcaptchaim(imgfile, captchafile, box):
    try:
        im = Image.open(imgfile)
        imcaptcha = im.crop(box)
        imcaptcha.save(captchafile)
        print("success crop")
    except:
        print("error in crop")
        pass

if __name__ == '__main__':
    #
    box = (370, 558, 520, 618)
    getcaptchaim("/sdcard/screenshot.png", "/sdcard/captcha.png", box)


