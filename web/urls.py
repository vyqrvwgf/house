# coding: utf-8

from django.conf.urls import url

from web.views import (
    index_view,
    auth,
    column,
    home,
)

# 管理后台
urlpatterns = [
    # 首页
    url(r'^$', index_view.index, name='admin_index'),
    # 登陆注册
    url(r'^login$', auth.login_view, name='admin_login'),
    url(r'^logout$', auth.logout_view, name='admin_logout'),
    # 轮播
    url(r'^advertising/list/$', home.advertising_list, name='advertising_list'),
    url(r'^advertising/create$', home.advertising_create, name='advertising_create'),
    url(r'^advertising/(?P<advertising_id>\d+)/edit$', home.advertising_edit, name='advertising_edit'),
    url(r'^advertising/(?P<advertising_id>\d+)/delete$', home.advertising_delete, name='advertising_delete'),
    url(r'^advertising/(?P<advertising_id>\d+)/up/$', home.advertising_up, name='advertising_up'),
    url(r'^advertising/(?P<advertising_id>\d+)/down/$', home.advertising_down, name='advertising_down'),
    # 栏目
    url(r'^column/list/$', column.list, name='column_list'),
    url(r'^column/create$', column.create, name='column_create'),
    url(r'^column/(?P<column_id>\d+)/edit$', column.edit, name='column_edit'),
    url(r'^column/(?P<column_id>\d+)/delete$', column.delete, name='column_delete'),
    url(r'^column/(?P<column_id>\d+)/up/$', column.up, name='column_up'),
    url(r'^column/(?P<column_id>\d+)/down/$', column.down, name='column_down'),
]
