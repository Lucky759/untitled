from rest_framework import serializers
from . import models

# 测试序列化
class TestsSerializer(serializers.ModelSerializer):
    number = serializers.SerializerMethodField() # 获取图片url

    def get_number(self, obj):
        if not obj.number:
            number = 0
        else:
            number = obj.number
        return number

    class Meta:
        model = models.Test
        fields = ('number', 'name', 'id')