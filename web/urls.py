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
    user,
    flush_view,
    listings,
    wanted,
    listings_release,
    wanted_release
)

# 管理后台
urlpatterns = [
    # 首页
    url(r'^$', index_view.index, name='admin_index'),
    # 登陆注册
    url(r'^login$', auth.login_view, name='admin_login'),
    url(r'^logout$', auth.logout_view, name='admin_logout'),
    url(r'^uptoken/$', index_view.uptoken, name='admin_uptoken'),

    url(r'^flush/setting/$', flush_view.setting, name='flush_setting'),

    # 轮播
    url(r'^advertising/list/$', home.advertising_list, name='advertising_list'),
    url(r'^advertising/create$',
        home.advertising_create,
        name='advertising_create'),
    url(r'^advertising/(?P<advertising_id>\d+)/edit$',
        home.advertising_edit, name='advertising_edit'),
    url(r'^advertising/(?P<advertising_id>\d+)/delete$',
        home.advertising_delete, name='advertising_delete'),
    url(r'^advertising/(?P<advertising_id>\d+)/up/$',
        home.advertising_up, name='advertising_up'),
    url(r'^advertising/(?P<advertising_id>\d+)/down/$',
        home.advertising_down, name='advertising_down'),

    # 栏目
    url(r'^column/list/$', column.list, name='column_list'),
    url(r'^column/create$', column.create, name='column_create'),
    url(r'^column/(?P<column_id>\d+)/edit$', column.edit, name='column_edit'),
    url(r'^column/(?P<column_id>\d+)/delete$',
        column.delete, name='column_delete'),
    url(r'^column/(?P<column_id>\d+)/up/$', column.up, name='column_up'),
    url(r'^column/(?P<column_id>\d+)/down/$', column.down, name='column_down'),

    # 用户管理
    url(r'^user/list/$', user.list, name='user_list'),
    url(r'^user/(?P<profile_id>\d+)/online/$',
        user.online, name='user_online'),
    url(r'^user/(?P<profile_id>\d+)/offline/$',
        user.offline, name='user_offline'),

    # 基础设施
    url(r'^infrastructure/list/$',
        infrastructure.list,
        name='infrastructure_list'),
    url(r'^infrastructure/create$',
        infrastructure.create,
        name='infrastructure_create'),
    url(r'^infrastructure/(?P<infrastructure_id>\d+)/edit$',
        infrastructure.edit, name='infrastructure_edit'),
    url(r'^infrastructure/(?P<infrastructure_id>\d+)/delete$',
        infrastructure.delete, name='infrastructure_delete'),
    url(r'^infrastructure/(?P<infrastructure_id>\d+)/up/$',
        infrastructure.up, name='infrastructure_up'),
    url(r'^infrastructure/(?P<infrastructure_id>\d+)/down/$',
        infrastructure.down, name='infrastructure_down'),

    # 房源列表
    url(r'^listings/list/$', listings.list, name='listings_list'),
    url(r'^listings/create/$',
        listings.create, name='listings_create'),
    url(r'^listings/(?P<housingresources_id>\d+)/edit/$',
        listings.edit, name='listings_edit'),
    url(r'^listings/(?P<housingresources_id>\d+)/online$',
        listings.online, name='listings_online'),
    url(r'^listings/(?P<housingresources_id>\d+)/offline$',
        listings.offline, name='listings_offline'),
    url(r'^listings/(?P<housingresources_id>\d+)/onquality$',
        listings.onquality, name='listings_onquality'),
    url(r'^listings/(?P<housingresources_id>\d+)/offquality$',
        listings.offquality, name='listings_offquality'),

    # 房源预约
    url(r'^listings/meet/list/$', listings.meet_list, name='listings_meet_list'),
    url(r'^listings/meet/(?P<housingresources_meet_id>\d+)/delete$', listings.meet_delete, name='listings_meet_delete'),
    url(r'^listings/meet/(?P<housingresources_meet_id>\d+)/complete$', listings.meet_complete, name='listings_meet_complete'),

    url(r'^listings/(?P<housingresources_id>\d+)/delete$',
        listings.delete, name='listings_delete'),
    # 房源图片
    url(r'^listings/(?P<housingresources_id>\d+)/picture/list/$',
        listings.picture_list,
        name='listings_picture_list'),
    url(r'^listings/(?P<housingresources_id>\d+)/picture/create/$',
        listings.picture_create, name='listings_picture_create'),
    url(r'^listings/picture/(?P<housingpicture_id>\d+)/edit/$',
        listings.picture_edit, name='listings_picture_edit'),
    url(r'^listings/picture/(?P<housingpicture_id>\d+)/delete$',
        listings.picture_delete, name='listings_picture_delete'),
    url(r'^listings/picture/(?P<housingpicture_id>\d+)/up$',
        listings.picture_up, name='listings_picture_up'),
    url(r'^listings/picture/(?P<housingpicture_id>\d+)/down$',
        listings.picture_down, name='listings_picture_down'),
    # 房源卧室
    url(r'^listings/(?P<housingresources_id>\d+)/bedroom/list/$',
        listings.bedroom_list,
        name='listings_bedroom_list'),
    url(r'^listings/(?P<housingresources_id>\d+)/bedroom/create/$',
        listings.bedroom_create, name='listings_bedroom_create'),
    url(r'^listings/bedroom/(?P<bedroom_id>\d+)/edit/$',
        listings.bedroom_edit, name='listings_bedroom_edit'),
    url(r'^listings/bedroom/(?P<bedroom_id>\d+)/delete$',
        listings.bedroom_delete, name='listings_bedroom_delete'),
    url(r'^listings/bedroom/(?P<bedroom_id>\d+)/online$',
        listings.bedroom_online, name='listings_bedroom_online'),
    url(r'^listings/bedroom/(?P<bedroom_id>\d+)/offline$',
        listings.bedroom_offline, name='listings_bedroom_offline'),


    # 房源发布
    url(r'^listings_release/list/$',
        listings_release.list,
        name='listings_release_list'),
    url(r'^listings_release/(?P<housingresources_id>\d+)/online/$',
        listings_release.online, name='listings_release_online'),
    url(r'^listings_release/(?P<housingresources_id>\d+)/offline/$',
        listings_release.offline, name='listings_release_offline'),

    # 求租列表
    url(r'^wanted/list/$', wanted.list, name='wanted_list'),
    url(r'^wanted/(?P<renthouse_id>\d+)/online$',
        wanted.online, name='wanted_online'),
    url(r'^wanted/(?P<renthouse_id>\d+)/offline$',
        wanted.offline, name='wanted_offline'),
    url(r'^wanted/(?P<renthouse_id>\d+)/delete$',
        wanted.delete, name='wanted_delete'),
    url(r'^wanted/import_data$', wanted.import_data, name='wanted_import_data'),
    # 求租预约
    url(r'^wanted/meet/list/$', wanted.meet_list, name='wanted_meet_list'),
    url(r'^wanted/meet/(?P<renthouse_meet_id>\d+)/delete$', wanted.meet_delete, name='wanted_meet_delete'),
    url(r'^wanted/meet/(?P<renthouse_meet_id>\d+)/complete$', wanted.meet_complete, name='wanted_meet_complete'),

    # 求租发布审核
    url(r'^wanted_release/list/$',
        wanted_release.list,
        name='wanted_release_list'),
    url(r'^wanted_release/(?P<renthouse_id>\d+)/online/$',
        wanted_release.online, name='wanted_release_online'),
    url(r'^wanted_release/(?P<renthouse_id>\d+)/offline/$',
        wanted_release.offline, name='wanted_release_offline'),

    # 商家管理员
    url(r'^venture_manage/list$',
        venture_manage.venture_manage_list,
        name='venture_manage_list'),
    url(r'^venture_manage/create$',
        venture_manage.venture_manage_create,
        name='venture_manage_create'),
    url(r'^venture_manage/(?P<account_id>\d+)/edit$',
        venture_manage.venture_manage_edit,
        name='venture_manage_edit'),
    url(r'^venture_manage/(?P<account_id>\d+)/delete$',
        venture_manage.venture_manage_delete,
        name='venture_manage_delete'),

    # 权限组
    url(r'^permissions/list$',
        permissions.permissions_list,
        name='permissions_list'),
    url(r'^permissions/create$',
        permissions.permissions_create,
        name='permissions_create'),
    url(r'^permissions/(?P<permissions_id>\d+)/edit$',
        permissions.permissions_edit, name='permissions_edit'),
    url(r'^permissions/(?P<permissions_id>\d+)/delete$',
        permissions.permissions_delete, name='permissions_delete'),

    # 系统管理员
    url(r'^operating/list$', operating.operating_list, name='operating_list'),
    url(r'^operating/create$',
        operating.operating_create,
        name='operating_create'),
    url(r'^operating/(?P<operating_id>\d+)/edit$',
        operating.operating_edit, name='operating_edit'),
    url(r'^operating/(?P<operating_id>\d+)/delete$',
        operating.operating_delete, name='operating_delete'),

    # 上传文件
    url(r'^ckeditor_upload$', index_view.ckeditor_upload, name='admin_upload'),
    url(r'^ckeditor_many_upload$',
        index_view.ckeditor_many_upload,
        name='admin_many_upload'),
]
