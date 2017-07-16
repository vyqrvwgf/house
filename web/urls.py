# coding: utf-8

from django.conf.urls import url

from web.views import (
    index_view,
    auth,
    column,
    home,
    venture_manage,
    permissions,
    operating,
    infrastructure,
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
    # 基础设施
    url(r'^infrastructure/list/$', infrastructure.list, name='infrastructure_list'),
    url(r'^infrastructure/create$', infrastructure.create, name='infrastructure_create'),
    url(r'^infrastructure/(?P<infrastructure_id>\d+)/edit$', infrastructure.edit, name='infrastructure_edit'),
    url(r'^infrastructure/(?P<infrastructure_id>\d+)/delete$', infrastructure.delete, name='infrastructure_delete'),
    url(r'^infrastructure/(?P<infrastructure_id>\d+)/up/$', infrastructure.up, name='infrastructure_up'),
    url(r'^infrastructure/(?P<infrastructure_id>\d+)/down/$', infrastructure.down, name='infrastructure_down'),
    # 商家管理员
    url(r'^venture_manage/list$', venture_manage.venture_manage_list, name='venture_manage_list'),
    url(r'^venture_manage/create$', venture_manage.venture_manage_create, name='venture_manage_create'),
    url(r'^venture_manage/(?P<account_id>\d+)/edit$', venture_manage.venture_manage_edit, name='venture_manage_edit'),
    url(r'^venture_manage/(?P<account_id>\d+)/delete$', venture_manage.venture_manage_delete, name='venture_manage_delete'),
    # 权限组
    url(r'^permissions/list$', permissions.permissions_list, name='permissions_list'),
    url(r'^permissions/create$', permissions.permissions_create, name='permissions_create'),
    url(r'^permissions/(?P<permissions_id>\d+)/edit$', permissions.permissions_edit, name='permissions_edit'),
    url(r'^permissions/(?P<permissions_id>\d+)/delete$', permissions.permissions_delete, name='permissions_delete'),
    # 系统管理员
    url(r'^operating/list$', operating.operating_list, name='operating_list'),
    url(r'^operating/create$', operating.operating_create, name='operating_create'),
    url(r'^operating/(?P<operating_id>\d+)/edit$', operating.operating_edit, name='operating_edit'),
    url(r'^operating/(?P<operating_id>\d+)/delete$', operating.operating_delete, name='operating_delete'),
    # 上传文件
    url(r'^ckeditor_upload$', index_view.ckeditor_upload, name='admin_upload'),
    url(r'^ckeditor_many_upload$', index_view.ckeditor_many_upload, name='admin_many_upload'),
]
