import re
import time
import requests

SENMA_URL = "http://api.iyylw.com"


class Senma(object):
    def __init__(self, account, pwd):
        self.token = None
        self.user = account
        self.pwd = pwd
        # self.dev_param = dev_param
        self.session = requests.session()
        # self.login()

    def login(self):
        params = {"user": self.user, "pwd": self.pwd}
        res = self.session.get(SENMA_URL + '/login', params=params, timeout=10)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        self.token = res.text.split('"')[3]
        print("login succeed!")
        print(self.token)


    def raise_api_exception(self, response):
         raise Exception(response.content.decode('utf-8'))

    # def getItems(self):
    #     res = self.session.get(FEIMA_URL + '/Api/GetItem', params={"token": self.token, "tp": "ut"}, timeout=10)
    #     if res.content.startswith('False'.encode()):
    #         self.raise_api_exception(res)
    #     items = res.content.decode('utf-8').split('\n')
    #     return items

    def addblack(self, pid, phone):
        params = {"token": self.token, "pid": str(pid), "mobile_list": str(pid)}
        res = self.session.get(SENMA_URL + '/add_black', params=params, timeout=10)
        print(res.text)

    def adv_release_all_mobile(self):
        #95f2de1919264757b8433365fcff0eb1
        res = self.session.get(SENMA_URL + '/adv_release_all_mobile', params={"token": self.token}, timeout=10)
        print(res.text)

    def getuserinfo(self):
        res = self.session.get(SENMA_URL + '/userinfo', params={"token": self.token}, timeout=10)
        print(res.text)

    def getPhone(self, pid):
        params = {"token": self.token, "pid": str(pid)}
        res = self.session.get(SENMA_URL + '/get_mobile', params=params, timeout=10)
        print(res.text)
        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        # result = res.text
        # return result
        return [p for p in res.text.split('"') if p]
        # return [res.text.split('"')[3]]

    def getMessage(self, pid, phone):
        params = {"token": self.token, "pid": pid, "mobile": phone}
        res = self.session.get(SENMA_URL + '/get_sms', params=params, timeout=20)
        print(res.text)

        if res.content.startswith('False'.encode()):
            self.raise_api_exception(res)
        return res.content.decode('utf-8')

    def waitForMessage(self, regrex, pid, phone, max_count=20, interval=3):
        count = 0
        while count <= max_count:
            msg = self.getMessage(pid, phone)
            # msg = msg.text.split('"')[3]
            # print(msg)
            match = re.search(regrex, msg)
            if match:
                return match.group(1)
            else:
                count += 1
                time.sleep(interval)
        else:
            print("poll timeout")
            return None

if __name__ == '__main__':
    # pass
    import time
    #95f2de1919264757b8433365fcff0eb1
    sm = Senma("xiaoxiaozhuan", "meiriq2014")
    sm.login()
    # sm.getPhone(1240)[0]
# re.search(r'您的验证码为：(\d+)\[End\]', mm).group(1)