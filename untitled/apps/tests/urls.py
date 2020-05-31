
from django.urls import path,re_path
from . import views

urlpatterns = [
    # 获取分类信息以及该分类下的品牌信息
    path("test/",views.TestAPIView.as_view({'get': 'retrieve'})),
    # re_path('brands/(?P<pk>\d+)/$', views.BrandAPIView.as_view()),
]
