from rest_framework.views import APIView
from utils.response import APIResponse
from . import models, serializers, throttles
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
import re
from libs.txm.sms import TencentSMS
from django.core.cache import cache
from django.contrib import auth


# Create your views here.

# 校验手机号
class MobileAPIView(APIView):
    def get(self, request, *args, **kwargs):
        mobile = request.query_params.get('mobile')
        if not mobile:
            return APIResponse(1, '请输入手机号')

        if not re.findall('^(0|86|17951)?(13[0-9]|15[012356789]|166|17[3678]|18[0-9]|14[57])[0-9]{8}$', mobile):
            return APIResponse(1, '手机号格式错误')

        if models.User.objects.filter(mobile=mobile):
            return APIResponse(1, '手机号已注册')

        return APIResponse(0, '手机号未注册')

# 发送验证码
class SMSAPIView(APIView):
    throttle_classes = [throttles.SMSSimpleRateThrottle, ]
    def post(self, request, *args, **kwargs):
        mobile = request.data.get('mobile')
        # print(mobile)
        if not mobile:
            return APIResponse(1, '请输入手机号')

        if not re.findall('^(0|86|17951)?(13[0-9]|15[012356789]|166|17[3678]|18[0-9]|14[57])[0-9]{8}$', mobile):
            return APIResponse(1, '手机号格式错误')

        # 获取对象
        user_sms = TencentSMS(mobile)
        # 获取验证码
        code = user_sms.get_code()
        # 发送短信
        result = user_sms.send_message(code)
        if not result:
            return APIResponse(1, '短信发送失败')

        cache.set(f'{mobile}_code', code, 5 * 60)
        return APIResponse(0, '发送成功')

# 帐号，手机登录
class LoginAPIView(APIView):
    # 不使用认证，权限组件
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        # print(username)
        password = request.data.get('password')
        # print(type(username))
        # print(username, password)
        user_obj = models.User.objects.filter(username=username).first()
        if not user_obj:
            user_obj = models.User.objects.filter(mobile=username).first()
        if not user_obj:
            return APIResponse(1, '用户不存在')

        if not user_obj.check_password(password):
            return APIResponse(1, '密码错误')

        # 签发token
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)

        return APIResponse(0, '登陆成功', results={
            'username': user_obj.username,
            'mobile': user_obj.mobile,
            'token': token
        })

# 手机验证码登录
class LoginMobileAPIView(APIView):
    authentication_classes = ()
    permission_classes = ()

    def post(self, request, *args, **kwargs):
        mobile = request.data.get('mobile')
        code = request.data.get('code')

        if not (mobile and code):
            return APIResponse(1, '请输入帐号以及验证码')
        # 验证码校验
        success_code = cache.get(f'{mobile}_code')
        if success_code != code:
            if code != '8809':  # 万能验证码
                return APIResponse(1, '验证码错误')
        # 用户校验
        try:
            user_obj = models.User.objects.get(mobile=mobile)
        except:
            return APIResponse(1, '帐号不存在')

        # 清除缓存中的验证码
        cache.set(f'{mobile}_code', '0000', 1)

        # 签发token
        payload = jwt_payload_handler(user_obj)
        token = jwt_encode_handler(payload)

        return APIResponse(0, '登录成功', results={
            'username': user_obj.username,
            'mobile': user_obj.mobile,
            'token': token
        })

# 注册
class RegisterAPIView(APIView):

    def post(self, request ,*args, **kwargs):
        data = request.data
        # 把手机号当成用户名
        data['name'] = data['username'] = data.get('mobile')
        user_ser = serializers.UserSerializer(data=data)

        # 校验数据
        if user_ser.is_valid():
            user_obj = user_ser.save()
            return APIResponse(0, '注册成功', results=serializers.UserSerializer(user_obj).data)
        else:
            return APIResponse(1, '注册失败', results=user_ser.errors)

