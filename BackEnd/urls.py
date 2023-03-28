"""BackEnd URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include
from django.views import static
from django.views import static ##新增
from django.conf import settings ##新增
from django.conf.urls import url ##新增
from BackEnd import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    # 用户登录和验证的路由
    path('wechat/', include(('app01.urls', 'app01'), namespace='app01')),

    # 导航首页轮播路由
    path('header/', include(('app02.urls', 'app02'), namespace='app02')),

    # 全部文汇路由
    path('articles/', include(('app03.urls', 'app03'), namespace='app03')),

    # path('static/<path:path>', static.serve,{'document_root': settings.STATIC_ROOT}, name='static'),
    url(r'^static/(?P<path>.*)$', static.serve,
        {'document_root': settings.STATIC_ROOT}, name='static'),
]


