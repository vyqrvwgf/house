# coding: utf-8

from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from web.models import (
    Setting,
)
from common.lookup import SETTING_CONFIG as setting_config
import datetime


@staff_member_required(login_url='/admin/login')
def setting(request):
    for c in setting_config:
        setting, _ = Setting.objects.get_or_create(
        	value=c['value'],
        	code=c['code']
        )
        setting.name = c['name']
        setting.save()

    return render(request, 'super/flush.html')
