# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf.urls import url

from wechatapi.views import (
    base,
)

urlpatterns = [
    # 发送验证码
    url(r'^0/send/sms_code/$', base.SendSmsCodeView.as_view(), name='sms_code'),
    url(r'^0/send/img_code/$', base.SendImgCodeView.as_view(), name='img_code'),

    # 租房需求
    url(r'^0/house/demand/$', base.HouseDemandView.as_view(), name='house_demand'),
]
