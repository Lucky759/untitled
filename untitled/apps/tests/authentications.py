
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
import jwt
from rest_framework_jwt.authentication import BaseJSONWebTokenAuthentication
from rest_framework_jwt.authentication import jwt_decode_handler
from utils.logging import logger

class JWTAuthentication(BaseJSONWebTokenAuthentication):
    # 自定义认证类，重写authenticate方法
    def authenticate(self, request):
        # 认证通过，返回user，auth
        # 认证失败，返回None，游客
        auth = request.META.get('HTTP_AUTHORIZATION')
        # print(auth)
        print('进入认证类')
        print(auth)
        if not auth:
            return None
        try:
            payload = jwt_decode_handler(auth)
        # 出现jwt解析异常，直接抛出异常，代表非法用户，也可以返回None，作为游客处理
        except jwt.ExpiredSignature:
            logger.error('token已过期')
            raise AuthenticationFailed('token已过期')
        except:
            logger.error('token非法')
            raise AuthenticationFailed('token非法')

        user = self.authenticate_credentials(payload)
        print('通过认证类')
        return (user, auth)




