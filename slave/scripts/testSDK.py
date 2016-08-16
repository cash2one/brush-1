import time

from jiema.jiumaSDK import Jiuma
from jiema.feimaSDK import Feima
from jiema.yamaSDK import Yama
from jiema.ailezanSDK import Ailezan
from jiema.jimaSDK import Jima
from jiema.shenhuaSDK import Shenhua
from jiema.yimaSDK import Yima

# code = Jiuma("xiaoxiaozhuan", "meiriq2014", 17564)
# code = Feima("xiaoxiaozhuan", "meiriq2014", 2055)
# code = Yama("xiaoxiaozhuan", "meiriq2014", 599)
code = Ailezan("api-4tuoz9od", "meiriq2014", 22223)
# code = Jima("xiaoxiaozhuan", "meiriq2014", 170)
# code = Shenhua("xiaoxiaozhuan", "meiriq2014", 45947)
# code = Yima("xiaoxiaozhuan", "meiriq2014", 26)

code.login()
time.sleep(1)
phone_num = code.getPhone("13151050704")
print("手机号码是:" + str(phone_num))
time.sleep(5)
# captcha = code.waitForMessage(r'验证码(\d+)', phone_num)
# print("验证码是:" + str(captcha))
code.releasePhone(phone_num)
code.addblackPhone(phone_num)
# code.exit()





