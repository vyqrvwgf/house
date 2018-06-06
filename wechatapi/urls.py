# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from wechatapi.views import (
    base,
    housing,
    rent_house,
)

urlpatterns = [
    # 发送验证码
    url(r'^0/send/sms_code/$', base.SendSmsCodeView.as_view(), name='sms_code'),
    url(r'^0/send/img_code/$', base.SendImgCodeView.as_view(), name='img_code'),

    # 租房需求
    url(r'^0/house/demand/$', base.HouseDemandView.as_view(), name='house_demand'),
    url(r'^0/wx_config/$', base.WxConfig.as_view(), name='wx_config'),

    # 房源
    url(r'^0/infres/$', housing.InfrastructureListView.as_view(), name='infres'),
    # url(r'^0/house/$', housing.HouseView.as_view(), name='house_add'),
    url(r'^0/houses/$', housing.HouseResourcesListView.as_view(), name='houses'),
    url(r'^0/house/$', housing.HouseResourceDetailView.as_view(), name='house'),
    # 求租
    url(r'^0/rent_houses/$', rent_house.RentHouseListView.as_view(), name='houses'),

]
