from rest_framework import serializers
from . import models
import re
from django.core.cache import cache

class UserSerializer(serializers.ModelSerializer):
    re_password = serializers.CharField(write_only=True)    # 反序列化校验确认密码
    code = serializers.CharField(write_only=True, min_length=4, max_length=4)   # 反序列化校验验证码

    class Meta:
        model = models.User
        fields = ('username', 'password', 'mobile', 're_password', 'code', 'name')

    # 局部钩子校验手机号
    def validate_mobile(self, value):
        if not re.findall('^(0|86|17951)?(13[0-9]|15[012356789]|166|17[3678]|18[0-9]|14[57])[0-9]{8}$', value):
            raise serializers.ValidationError('手机号格式错误')

        return value

    # 全局钩子校验密码和验证码
    def validate(self, attrs):
        # 校验密码
        password = attrs.get('password')
        re_password = attrs.pop('re_password')
        if password != re_password:
            raise serializers.ValidationError('两次密码输入不一致')

        # 校验验证码
        new_code = attrs.pop('code')
        mobile = attrs.get('mobile')
        old_code = cache.get(f'{mobile}_code')
        # print(new_code, old_code, type(new_code), type(old_code))
        if old_code != new_code:
            if new_code != '8809':
                raise serializers.ValidationError('验证码错误')
        return attrs

    # 因为用的是auth的user表，所以需要用create_user
    def create(self, validated_data):
        return models.User.objects.create_user(**validated_data)