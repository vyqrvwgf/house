# -*- coding: utf-8 -*-

import redis
import simplejson as json
import logging
import random

from django.db import transaction
from django.contrib.auth.models import User
from wechat.wx_config import get_wx_config
from django.db.models import Q
from rest_framework.views import APIView
from django.http import JsonResponse
from rest_framework.permissions import AllowAny

from web.models import (
    Infrastructure,
    RentHouse
)

from settings import (
    WECHAT_APP_ID,
    WECHAT_APP_SECRET,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB,
    DOMAIN,
    MEDIA_URL
)


class RentHouseListView(APIView):
    """求租列表
    """
    permission_classes = (AllowAny, )

    def get(self, request):

        page = request.query_params.get('page', 0)
        page_size = request.query_params.get('page_size', 5)
        keywords = request.query_params.get('keywords', '')
        area = request.query_params.get('area', '')
        start_price = request.query_params.get('start_price', 0)
        end_price = request.query_params.get('end_price', 0)
        waytorent = request.query_params.get('waytorent', '')

        try:
            page = int(page)
            page = 1 if not page else page
            page_size = int(page_size)

            rent_house_list = RentHouse.obs.get_queryset().filter(status=2, audit_status=2)

            if keywords:
                rent_house_list = rent_house_list.filter(
                    Q(description__icontains=keywords))

            if area and area != u'不限':
                rent_house_list = rent_house_list.filter(area__icontains=area)
            
            if start_price:
                start_price = int(start_price)
                if start_price <= 500 and not end_price:
                    rent_house_list = rent_house_list.filter(rent__lte=start_price)
                else:
                    rent_house_list = rent_house_list.filter(rent__lte=start_price)
            
            if end_price:
                end_price = int(end_price)
                if end_price >= 4000 and not start_price:
                    rent_house_list = rent_house_list.filter(rent__gte=end_price)
                else:
                    rent_house_list = rent_house_list.filter(rent__gte=end_price)

            if waytorent == u'整租':
                rent_house_list = rent_house_list.filter(lease=0)
            elif waytorent == u'合租':
                rent_house_list = rent_house_list.filter(lease=1)

            rent_houses = []
            rent_house_count = rent_house_list.count()
            for rh in rent_house_list[(page-1)*page_size:page*page_size]:
                infrastructures = []
                for i in rh.infrastructure.all():
                    infrastructures.append({
                        'infrastructure_id': i.id,
                        'name': i.name,
                    })

                rent_houses.append({
                    'rent_house_id': rh.id,
                    'avatar': rh.get_profile.avatar_url() if rh.get_profile else '',
                    'name': rh.name,
                    'rent': rh.rent,
                    'description': rh.description,
                    'infrastructures': infrastructures,
                })

        except Exception as e:
            logging.error(e)
            logging.error("----------------RentHouseListView----get-------------")
            return JsonResponse({'error_code': 1, 'error_msg': '参数错误'})

        return JsonResponse({
            'error_code': 0,
            'error_msg': '请求成功',
            'data': {
                'rent_houses': rent_houses,
                'rent_house_count': rent_house_count,
                'page': page,
                'page_size': page_size,
            }
        })
