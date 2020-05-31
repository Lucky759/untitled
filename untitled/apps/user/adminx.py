# xadmin全局配置
import xadmin
from xadmin import views
from . import models

class GlobalSettings(object):
    """xadmin的全局配置"""
    site_title = "仙女街"  # 设置站点标题
    site_footer = "Fairy_street"  # 设置站点的页脚
    menu_style = "accordion"  # 设置菜单折叠

xadmin.site.register(views.CommAdminView, GlobalSettings)
# xadmin.site.register(models.User)
xadmin.site.register(models.Wxuser)