# coding: utf-8

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Q, Avg
from django.template import loader

from django.contrib.auth import login, logout, authenticate
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from web.models import(
    Profile,
    RentHouse,
    RentHouseMeet
)

from settings import (
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB,
    DB_PREFIX,
    UPLOAD_DIR,
    DOMAIN,
    QQ_MAP_API_URL
)

import os
import datetime
import time
import simplejson
import requests
import random
import string
import redis
import logging


def rent_house_list(request):

    rent_houses = RentHouse.obs.get_queryset().filter(status=2, audit_status=2)

    context = {
        'module': 'rent_house',
        'rent_houses': rent_houses,
    }

    return render(request, 'frontend/03-findToRent.html', context)


@csrf_exempt
def rent_house_meet_create(request):
    try:
        with transaction.atomic():
            c_user = request.session.get('c_user', {})
            profile = Profile.obs.get_queryset().filter(pk=c_user.get('id', 0)).first()

            rent_house_id = request.POST.get('rent_house_id', 0)
            rent_house = RentHouse.objects.get(pk=rent_house_id)

            RentHouseMeet.objects.get_or_create(
                user=profile.user,
                rent_house=rent_house,
            )
    except Exception as e:
        logging.error(e)
        return JsonResponse({'error_code': 1, 'error_msg': '预约失败'})

    return JsonResponse({'error_code': 0, 'error_msg': '已接受预约工作人员会在一个工作日内协助完成预约。'})

