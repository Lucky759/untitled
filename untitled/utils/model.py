from django.db import models

class BaseModel(models.Model):
    is_delete = models.BooleanField(verbose_name='逻辑删除', default=False)
    is_show = models.BooleanField(verbose_name='是否上架', default=False)
    create_time = models.DateTimeField(verbose_name='添加时间', auto_now_add=True, null=True, blank=True)
    update_time = models.DateTimeField(verbose_name='更新时间', auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True