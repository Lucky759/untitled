from .celery import app
from django.core.cache import cache
from apps.home import models, serializers

@app.task
def django_task(x, y):
    print(x, y)
    banner_query = models.Banner.objects.filter(is_show=True, is_delete=False).order_by('-order')
    banner_list_data = serializers.BannerModelSerializer(banner_query, many=True).data
    # print(banner_list_data)
    # 建立接口缓存
    cache.set('api_banner_list_data', banner_list_data)
    return '轮播图缓存更新完毕'





