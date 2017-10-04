# coding: utf-8

from django.conf.urls import url

from website.views import (
    home,
    user,
)

# 管理后台
urlpatterns = [
    # 首页
    url(r'^$', home.index, name='home_index'),
    url(r'^register$', home.register, name='home_register'),
    url(r'^login$', home.login, name='home_login'),

    # 用户
    url(r'^user$', user.index, name='user_index'),
    url(r'^hr_create$', user.housing_resource_create, name='housing_resource_create'),
    url(r'^user/update_profile$', user.update_profile, name='update_profile'),
    url(r'^login_out$', user.login_out, name='login_out'),
]
