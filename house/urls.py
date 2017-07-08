
# coding: utf-8

from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    url(r'^superadmin/', admin.site.urls),
    # 默认后台
    url(r'^admin/', include('web.urls', namespace='web')),
]
