import requests
import re
import random
from random import choice

getnum = 1
while getnum:
    getnum -= 1
    try:
        # 段子
        #######################################################################
        # WEB_URL = 'http://m.tduanzi.com/?page=%s' % random.randint(1, 1500)
        # WEB_URL = 'http://www.askzhen.com/?c-33/all/%s.html' %getnum
        WEB_URL = 'http://www.39ask.net/category/view/232/2/%s.html' % getnum
        # WEB_URL = 'https://www.zhihu.com/question/20070537'
        r = requests.get(WEB_URL)  # 发送请求
        # print(r.text.encode('utf-8'))
        # b = r.text.decode('utf-8')
        # print(b)
        ######################################################################
        with open("D:/brush/slave/scripts/doc/pachong.txt", 'w', encoding='utf-8') as fd:
            fd.write(r.text)
        # with open("D:/brush/slave/scripts/doc/pachong.txt", 'r', encoding='utf-8') as f:
        #     a = f.readlines()
        # alen = a.__len__()
        # regrex = r'<span style="font-size: 16px;">(.{1,100})</span>'
        # while alen:
        #     alen -= 1
        #     msg = a[alen]
        #     match = re.search(regrex, msg)
        #     if match:
        #         print(match.group(1))
        #         with open("D:/brush/slave/scripts/doc/duanzi3.txt", 'a', encoding='utf-8') as f:
        #             f.write(match.group(1)+'\n')
        # with open("D:/brush/slave/scripts/doc/pachong.txt", 'r', encoding='utf-8') as f:
        #     a = f.read()
        ##################################################################
        regrex = r'target="_blank" title="(.{1,100})</a>&nbsp;<span class="cate">'
        regrex = r'target="_blank">(.{1,100})</a></div>'
        match = re.findall(regrex, r.text)
        if match:
            print(match)
            with open("D:/brush/slave/scripts/doc/营养科.txt", 'a', encoding='utf-8') as f:
                for x in match:
                    f.write(x+'\n')
        ####################################################################
        #交友信息
        # WEB_URL = 'http://www.idomarry.com/SearchResult.asp?sex=%s&min_age=18&max_age=40&Curpage=%s' % (choice(['f', 'm']), random.randint(1, 750))
        # # WEB_URL = 'http://www.idomarry.com/Recomment.asp?sexN=%s&Curpage=%s' % (random.randint(1, 3), random.randint(1, 50))
        # print(WEB_URL)
        # r = requests.get(WEB_URL)  # 发送请求
        # with open("pachong.txt", 'w', encoding='utf-8') as fd:
        #     fd.write(r.text)
        # with open("pachong.txt", 'r', encoding='utf-8') as f:
        #     a = f.readlines()
        # alen = a.__len__()
        # regrex = r'</strong> (.{1,100})<br />'
        # # regrex = r'</span><br /><font color="#777777">(.{1,100})...</font>'
        # while alen:
        #     alen -= 1
        #     msg = a[alen]
        #     match = re.search(regrex, msg)
        #     # match = re.findall(regrex, msg)
        #     if match:
        #         print(match.group(1))
        #         with open("duanzi2.txt", 'a', encoding='utf-8') as f:
        #             f.write(match.group(1)+'\n')
    except Exception as e:
        print(e)
    print(getnum)