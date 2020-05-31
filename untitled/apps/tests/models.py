from django.db import models
from utils.model import BaseModel
from ..user.models import User


# Create your models here.
# 测试
class Test(BaseModel):
    name = models.CharField(max_length=50, verbose_name='昵称')

    class Meta:
        db_table = 'tests'
        verbose_name = '测试表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
