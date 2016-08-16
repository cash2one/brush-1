import re
import time
import requests

THEWOLF_URL = "http://thewolf.lannuonet.com/index.php"

class Thewolf(object):
    def __init__(self, account, pwd):
        self.token = None
        self.user = account
        self.pwd = pwd
        self.session = requests.session()
        # self.login()

    def login(self):
        print("login thewolf")
        params = {"username": self.user, "password": self.pwd}
        res = self.session.get(THEWOLF_URL + "/reg/login", params=params, timeout=10)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        print(res.text)
        self.token = res.text.split('|')[0]
        print("login succeed!")
        # print(self.token)

    def get_user(self):
        print("login yima")
        params = {"action": "getaccountinfo", "token": self.token}
        res = self.session.get(THEWOLF_URL, params=params, timeout=10)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        print(res.text)
        # self.token = res.text.split('|')[1]
        # print("login succeed!")

    def raise_api_exception(self, response):
        raise Exception(response.content.decode('utf-8'))

    def exit(self):
        params = {"action": "logout", "token": self.token}
        res = self.session.get(THEWOLF_URL, params=params, timeout=10)
        print("yima exit")
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)

    def getPhone(self, item_id, phone=None):
        print("获取号码")
        params = {"action": "getmobile", "itemid": str(item_id), "token": self.token}
        if phone:
            params["mobile"] = phone
        res = self.session.get(THEWOLF_URL, params=params, timeout=10)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        # result = res.text
        print(res.text)
        return res.text.split('|')

    def releasePhone(self, item_id, phone=None):
        print("释放号码号码")
        if phone:
            params = {"action": "release", "itemid": str(item_id), "mobile": phone, "token": self.token}
            res = self.session.get(THEWOLF_URL, params=params, timeout=10)
        else:
            params = {"action": "releaseall", "token": self.token}
            res = self.session.get(THEWOLF_URL, params=params, timeout=10)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        # result = res.text
        print(res.text)

    def getMessage(self, item_id, phone):
        params = {"action": "getsms", "token": self.token, "itemid": str(item_id), "mobile": phone, "release": 1}
        res = self.session.get(THEWOLF_URL, params=params, timeout=10)
        # print(res.text)
        if res.content.startswith('False'.encode()):
            # self.raise_api_exception(res)
            return 'NULL'
        return res.content.decode('utf-8')

    def waitForMessage(self, regrex, item_id, phone, max_count=20, interval=3):
        count = 0
        while count <= max_count:
            msg = self.getMessage(item_id, phone)
            print(msg)
            match = re.search(regrex, msg)
            if match:
                # print("waitfor:%s" % match.group(1))
                return match.group(1)
            else:
                count += 1
                time.sleep(interval)
        else:
            print("poll timeout")
            return None

if __name__ == '__main__':
    import time
    fm = Thewolf("xiaoxiaozhuan", "meiriq2014")
    fm.login()

# re.search(r'您的验证码为：(\d+)\[End\]', mm).group(1)