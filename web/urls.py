# coding: utf-8

from django.conf.urls import url

from web.views import (
    index_view,
    auth,
)

# 管理后台
urlpatterns = [
    # 首页
    url(r'^$', index_view.index, name='admin_index'),
    # 登陆注册
    url(r'^login$', auth.login_view, name='admin_login'),
    url(r'^logout$', auth.logout_view, name='admin_logout'),

]
