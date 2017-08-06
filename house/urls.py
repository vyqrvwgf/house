
# coding: utf-8

from django.conf.urls import url, include
from django.contrib import admin
from website.views import home

urlpatterns = [
    # 首页
	url(r'^', include('website.urls', namespace='website')),
	# 管理员后台
	url(r'^admin/', include('web.urls', namespace='web')),
	# 超级后台
	url(r'^superadmin/', admin.site.urls),
]
