from django.db import models
from django.contrib.auth.models import AbstractUser
from utils.model import BaseModel

# Create your models here.

# 仙女街用户表
class User(AbstractUser):
    gender_choice = (
        ('0', '男'),
        ('1', '女')
    )
    avatar = models.ImageField(upload_to='avatar', default='avatar/default.png', verbose_name='头像', help_text='60*60', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name='昵称')
    gender = models.CharField(choices=gender_choice, max_length=12, default='1', verbose_name='性别')
    mobile = models.CharField(max_length=11, null=True, blank=True, verbose_name='手机号码')
    wx_id = models.OneToOneField('Wxuser', on_delete=models.SET_NULL, null=True, blank=True, db_constraint=False,
                                 verbose_name='关联的微信id')

    class Meta:
        db_table = 'fairy_street_user'
        verbose_name = '用户表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 微信用户表
class Wxuser(BaseModel):
    id = models.AutoField(primary_key=True)
    openid = models.CharField(max_length=255)
    name = models.CharField(max_length=50, verbose_name='用户名')
    avatar = models.CharField(max_length=200, verbose_name='头像')
    language = models.CharField(max_length=50, verbose_name='语言')
    province = models.CharField(max_length=50, verbose_name='省')
    city = models.CharField(max_length=50, verbose_name='市')
    country = models.CharField(max_length=50, verbose_name='县')
    gender = models.CharField(max_length=50, verbose_name='性别')

    class Meta:
        db_table = 'wx_user'
        verbose_name = '微信用户表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.openid
