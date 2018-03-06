# coding: utf-8

from django.conf.urls import url

from website.views import (
    home,
    user,
    rent_house,
)

# 管理后台
urlpatterns = [
    # 首页
    url(r'^$', home.index, name='home_index'),
    url(r'^search$', home.search, name='home_search'),
    url(r'^register$', home.register, name='home_register'),
    url(r'^login$', home.login, name='home_login'),
    url(r'^feedback/add$', home.feedback_add, name='home_feedback_add'),
    url(r'^upload_file$', home.upload_file, name='upload_file'),
    url(r'^send/vcode$', home.send_vcode, name='send_vcode'),
    url(r'^send/vcode1$', home.send_vcode1, name='send_vcode1'),

    # 房源
    url(r'^housing_resources$',
        home.housing_resources_list, name='housing_resources_list'),
    url(r'^housing_resources_map$',
        home.housing_resources_map_list, name='housing_resources_map_list'),
    url(r'^housing_resources/(?P<housing_resources_id>\d+)$',
        home.housing_resources, name='housing_resources'),

    # 求租
    url(r'^rent_house$',
        rent_house.rent_house_list, name='rent_house_list'),
    url(r'^rent_house/meet/create$',
        rent_house.rent_house_meet_create, name='rent_house_meet_create'),

    # 用户
    url(r'^user$', user.index, name='user_index'),
    url(r'^user/update_profile$', user.update_profile, name='update_profile'),
    url(r'^user/update_avatar$', user.update_avatar, name='update_avatar'),
    url(r'^login_out$', user.login_out, name='login_out'),
    url(r'^reset/pwd$', user.reset_pwd, name='reset_pwd'),

    # 房源发布
    url(r'^housing_resources/create$',
        user.housing_resource_create,
        name='housing_resource_create'),
    url(r'^housing_resources/(?P<housing_resources_id>\d+)/edit$',
        user.housing_resource_edit, name='housing_resource_edit'),
    url(r'^user/housing_resources$',
        user.housing_resources,
        name='user_housing_resources'),
    url(r'^housing_resources/(?P<housing_resources_id>\d+)/offline$',
        user.housing_resource_offline, name='housing_resource_offline'),
    url(r'^housing_resources/(?P<housing_resources_id>\d+)/online$',
        user.housing_resource_online, name='housing_resource_online'),

    # 求租发布
    url(r'^rent_house/create$',
        user.rent_house_create,
        name='rent_house_create'),
    url(r'^rent_house/(?P<rent_house_id>\d+)/edit$',
        user.rent_house_edit, name='rent_house_edit'),
    url(r'^user/rent_houses$',
        user.rent_house,
        name='user_rent_house'),
]
