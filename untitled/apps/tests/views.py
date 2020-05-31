from django.shortcuts import render

# Create your views here.
# 分类
from rest_framework.generics import ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from apps.tests import models, serializers, authentications

from django.core.cache import cache

from utils.response import APIResponse


class TestAPIView(ModelViewSet):
    queryset = models.Test.objects.filter(is_show=True, is_delete=False).order_by('-order')
    serializer_class = serializers.TestsSerializer
    # 重写get方法是为了增加缓存功能
    def get(self, request, *args, **kwargs):
        '''
        如果缓存中有，直接返回，没有就调用原本的list方法获取到返回值再返回
        '''
        data = cache.get('category_list')
        if data:
            return Response(data)
        data = self.list(request, *args, **kwargs)
        cache.set('category_list', data.data)
        print('分类品牌查了数据库')
        return data

# 地址
class AddressListAPIView(ListAPIView):
    # 认证类：判断是否登录
    authentication_classes = [authentications.JWTAuthentication]
    # authentication_classes = []
    # 权限类：游客只能使用get接口，登录后才能使用Post接口
    permission_classes = [IsAuthenticated]
    # permission_classes = []
    queryset = models.Test.objects.filter(is_show=True, is_delete=False).order_by('-id')
    serializer_class = serializers.TestsSerializer

    # 额外加入筛选用户的参数
    def get(self, request, *args, **kwargs):
        data = request.data
        data['is_show'] = True
        data['user'] = request.user.id
        self.queryset = models.Test.objects.filter(is_show=True, is_delete=False, id=request.id).order_by('-id')
        return self.list(request, *args, **kwargs)

    # 增加is_show=True，不然默认值为False
    def post(self, request, *args, **kwargs):
        data = request.data
        # print(request.data)
        data['is_show'] = True
        data['user'] = request.user.id
        print(data)
        test_ser = serializers.TestsSerializer(data=data)
        if test_ser.is_valid():
            test_obj = test_ser.save()
            print(test_obj)
            return APIResponse(0, 'ok', results=serializers.TestsSerializer(test_obj).data)
        return APIResponse(1, '添加失败', results=test_ser.errors)

    def delete(self, request, *args, **kwargs):
        address_id = request.data.get('address_id')
        user_id = request.user.id
        if not (address_id, user_id):
            return APIResponse(1, '数据不全')
        result = models.Test.objects.filter(user_id=user_id, id=address_id).delete()
        if result:
            return APIResponse(0, '删除成功')
        return APIResponse(1, '删除失败')

    def patch(self, request, *args, **kwargs):
        data = request.data
        address_query = models.Test.objects.filter(id=data.get('id')).first()
        # print(address_query)
        if not address_query:
            return APIResponse(1, '信息错误')

        address_ser = serializers.TestsSerializer(data=data, instance=address_query, partial=True)
        if address_ser.is_valid():
            address_obj = address_ser.save()
            print(address_obj)
            return APIResponse(0, '修改成功')
        return APIResponse(1, '修改失败', results=address_ser.errors)
