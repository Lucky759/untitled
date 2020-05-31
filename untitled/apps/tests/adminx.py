# xadmin全局配置
import xadmin
from xadmin import views
from . import models

xadmin.site.register(models.Test)