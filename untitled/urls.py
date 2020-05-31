"""untitled URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import xadmin
xadmin.autodiscover()
# xversion模块自动注册需要版本控制的 Model
from xadmin.plugins import xversion
xversion.register_models()

from django.urls import path, include, re_path
from django.views.static import serve
from django.conf import settings
from rest_framework.schemas import get_schema_view
from rest_framework_swagger.renderers import SwaggerUIRenderer, OpenAPIRenderer

schema_view = get_schema_view(title='API', public=True, renderer_classes=[OpenAPIRenderer, SwaggerUIRenderer])
urlpatterns = [
    path('xadmin/', xadmin.site.urls),
    path('user/', include('apps.user.urls')),
    path('test/', include('apps.tests.urls')),

    path('swagger/', schema_view, name='swagger'),
    re_path(r'media/(?P<path>.*)', serve, kwargs={'document_root': settings.MEDIA_ROOT})
]
