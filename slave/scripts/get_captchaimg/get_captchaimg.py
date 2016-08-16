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
    #善林宝
    # box = (501, 427, 696, 487)
    #凤凰新闻
    # box = (377, 394, 571, 462)
    #投融家
    box = (470, 167, 720, 245)
    getcaptchaim("/sdcard/screenshot.png", "/sdcard/captcha.png", box)


