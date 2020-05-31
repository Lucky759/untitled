from qcloudsms_py import SmsSingleSender
from qcloudsms_py.httpclient import HTTPError
import random
from utils.logging import logger


class TencentSMS(object):
    # 短信应用 SDK AppID
    appid = 1400266828  # SDK AppID 以1400开头
    # 短信应用 SDK AppKey
    appkey = "6a8a9fa9c388daf79b1f7117c1a33ffc"
    # 需要发送短信的手机号码
    # phone_numbers = ["15879067265", ]
    # 短信模板ID，需要在短信控制台中申请
    template_id = 438825  # NOTE: 这里的模板 ID`7839`只是示例，真实的模板 ID 需要在短信控制台中申请
    # 签名
    sms_sign = "小y的技术栈"  # NOTE: 签名参数使用的是`签名内容`，而不是`签名ID`。这里的签名"腾讯云"只是示例，真实的签名需要在短信控制台中申请

    ssender = SmsSingleSender(appid, appkey)

    def __init__(self, mobile):
        self.mobile = mobile

    def send_message(self, code, exp=5):
        params = [code, exp]  # 当模板没有参数时，`params = []`
        try:
            response = self.ssender.send_with_param(86, self.mobile,
                                                    self.template_id, params, sign=self.sms_sign, extend="", ext="")
        except Exception as e:
            logger.error(f'sms error: {e}')
            return False
        print(response)
        if response['result'] != 0:
            logger.error(f'sms result {response["result"]} error, msg is {response["errmsg"]}')
            return False
        return True

    def get_code(self):
        code = ''
        for i in range(4):
            code += str(random.randint(0, 9))
        return code
