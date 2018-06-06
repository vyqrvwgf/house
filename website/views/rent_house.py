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

    rent_house_list = RentHouse.obs.get_queryset().filter(status=2, audit_status=2)

    if request.method == 'POST':
        area = request.POST.get('area', '')
        price = request.POST.get('price', '')
        waytorent = request.POST.get('waytorent', '')
        start_price = request.POST.get('start_price', '')
        end_price = request.POST.get('end_price', '')

        print request.POST
        if area and area != u'不限':
            rent_house_list = rent_house_list.filter(area__icontains=area)
        
        if start_price:
            rent_house_list = rent_house_list.filter(rent__gte=start_price)
        
        if end_price:
            rent_house_list = rent_house_list.filter(rent__lte=end_price)

        if not start_price and not end_price and price and price != u'不限':
            price_list = price.split('-')
            start_price = price_list[0]
            end_price = price_list[1] if len(price_list) > 1 else 0
            if not end_price:
                rent_house_list = rent_house_list.filter(rent__lte=int(start_price))
            else:
                rent_house_list = rent_house_list.filter(
                    rent__gte=int(start_price),
                    rent__lte=int(end_price),
                )
        if waytorent == u'整租':
            rent_house_list = rent_house_list.filter(lease=0)
        elif waytorent == u'合租':
            rent_house_list = rent_house_list.filter(lease=1)
        print rent_house_list
        tmp = loader.get_template('frontend/load-findToRent.html')
        html = tmp.render({'rent_houses': rent_house_list})
        return JsonResponse({'html': html})

    context = {
        'module': 'rent_house',
        'rent_houses': rent_house_list,
    }

    return render(request, 'frontend/03-findToRent.html', context)


@csrf_exempt
def rent_house_meet_create(request):
    try:
        with transaction.atomic():
            c_user = request.session.get('c_user', {})
            profile = Profile.obs.get_queryset().filter(pk=c_user.get('id', 0)).first()

            rent_house_id = request.POST.get('rent_house_id', 0)
            select_date = request.POST.get('select_date', '')
            meet_time = datetime.datetime.strptime(select_date, "%Y-%m-%d")
            rent_house = RentHouse.objects.get(pk=rent_house_id)
            rent_house_meet, _ = RentHouseMeet.objects.get_or_create(
                user=profile.user,
                rent_house=rent_house
            )
            rent_house_meet.meet_time = meet_time
            rent_house_meet.save()

    except Exception as e:
        logging.error(e)
        return JsonResponse({'error_code': 1, 'error_msg': '预约失败'})

    return JsonResponse({'error_code': 0, 'error_msg': '已接受预约工作人员会在一个工作日内协助完成预约。'})

