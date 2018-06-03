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
    HousingResources
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


class InfrastructureListView(APIView):
    """基础设施
    """
    permission_classes = (AllowAny, )

    def get(self, request):

        try:
            infrastructures = []
            infrastructure_list = Infrastructure.obs.get_queryset().order_by('-order_no')
            for i in infrastructure_list:
                infrastructures.append({
                    'infrastructure_id': i.id,
                    'name': i.name,
                    'cover': i.cover_url,
                })
        except Exception as e:
            logging.error(e)
            logging.error("----------------InfrastructureView-----------------")
            return JsonResponse({'error_code': 1, 'error_msg': '获取失败'})

        return JsonResponse({
            'error_code': 0,
            'error_msg': '请求成功',
            'data': {
                'infrastructures': infrastructures
            }
        })


class HouseView(APIView):
    """房源
    """
    permission_classes = (AllowAny, )

    def get(self, request):

        try:
            pass

        except Exception as e:
            logging.error(e)
            logging.error("----------------HouseView----get-------------")
            return JsonResponse({'error_code': 1, 'error_msg': '参数错误'})

        return JsonResponse({
            'error_code': 0,
            'error_msg': '请求成功',
        })

    def post(self, request):

        content = request.data.get('content', '')
        lease = request.data.get('lease', 0)
        category = request.data.get('category', '')
        province = request.data.get('province', '')
        city = request.data.get('city', '')
        area = request.data.get('area', '')
        bet = request.data.get('bet', 0)
        month_rent = request.data.get('month_rent', 0)
        pay = request.data.get('pay', 0)
        direction = request.data.get('direction', 0)
        layer = request.data.get('layer', 0)
        total_layer = request.data.get('total_layer', 0)
        community = request.data.get('community', '')
        address = request.data.get('address', '')
        bus = request.data.get('bus', '')
        subway = request.data.get('subway', '')
        buy = request.data.get('buy', '')
        sitting_room = request.data.get('sitting_room', 0)
        sitting_room_area = request.data.get('sitting_room_area', 0)
        sitting_room_complete = request.data.getlist(
            'sitting_room_complete', [])
        infrastructure_id = request.data.getlist('infrastructure_id', [])

        try:
            # 验证码校验
            housing_resources = HousingResources()
            if content:
                housing_resources.content = content
            if lease:
                housing_resources.lease = lease
            if profile:
                housing_resources.user = profile.get_user()
            if category:
                housing_resources.category = category
            if province:
                housing_resources.province = province
            if bet:
                housing_resources.bet = bet
            if pay:
                housing_resources.pay = pay
            if direction:
                housing_resources.direction = direction
            if layer:
                housing_resources.layer = layer
            if total_layer:
                housing_resources.total_layer = total_layer
            if community:
                housing_resources.community = community
            if month_rent:
                housing_resources.month_rent = month_rent
            if address:
                housing_resources.address = address
            if bus:
                housing_resources.bus = bus
            if subway:
                housing_resources.subway = subway
            if buy:
                housing_resources.buy = buy
            if sitting_room_area:
                housing_resources.sitting_room_area = float(
                    sitting_room_area) if sitting_room_area else 0
            
            housing_resources.save()

        except Exception as e:
            logging.error(e)
            logging.error("----------------HouseDemandView------post-----------")
            return JsonResponse({'error_code': 1, 'error_msg': '参数错误'})

        return JsonResponse({
            'error_code': 0,
            'error_msg': '请求成功',
        })


class HouseResourcesListView(APIView):
    """房源列表
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

            housingresources_list = HousingResources.obs.get_queryset().filter(
                audit_status=2,
                status=2,
            )
            if keywords:
                housingresources_list = housingresources_list.filter(
                    Q(community__icontains=keyword) | Q(address__icontains=keyword) | Q(content__icontains=keyword))

            if area and area != u'不限':
                housingresources_list = housingresources_list.filter(area__icontains=area)
            
            if start_price:
                start_price = int(start_price)
                if start_price <= 500 and not end_price:
                    housingresources_list = housingresources_list.filter(month_rent__lte=start_price)
                else:
                    housingresources_list = housingresources_list.filter(month_rent__lte=start_price)
            
            if end_price:
                end_price = int(end_price)
                if end_price >= 4000 and not start_price:
                    housingresources_list = housingresources_list.filter(month_rent__gte=end_price)
                else:
                    housingresources_list = housingresources_list.filter(month_rent__lte=end_price)

            if waytorent == u'整租':
                housingresources_list = housingresources_list.filter(lease=0)
            elif waytorent == u'合租':
                housingresources_list = housingresources_list.filter(lease=1)

            housing_resources = []
            housingresources_count = housingresources_list.count()
            for h in housingresources_list[(page-1)*page_size:page*page_size]:
                housing_resources.append({
                    'housing_resources_id': h.id,
                    'content': h.content,
                    'cover': h.cover_url,
                    'lease': h.get_lease_display(),
                    'month_rent': h.month_rent,
                    'community': h.community,
                })


        except Exception as e:
            logging.error(e)
            logging.error("----------------HouseView----get-------------")
            return JsonResponse({'error_code': 1, 'error_msg': '参数错误'})

        return JsonResponse({
            'error_code': 0,
            'error_msg': '请求成功',
            'data': {
                'housing_resources': housing_resources,
                'housingresources_count': housingresources_count,
                'page': page,
                'page_size': page_size,
            }
        })


class HouseResourceDetailView(APIView):
    """房源详情
    """
    permission_classes = (AllowAny, )

    def get(self, request):

        housing_resources_id = request.query_params.get('housing_resources_id', 0)
        try:
            housing_resources = HousingResources.objects.get(pk=housing_resources_id)
            infrastructures = []
            for i in housing_resources.infrastructure.all():
                infrastructures.append({
                    'infrastructure_id': i.id,
                    'name': i.name,
                    'cover': i.cover_url,
                })

            house = {
                'housing_resources_id': housing_resources.id,
                'content': housing_resources.content,
                'cover': housing_resources.cover_url,
                'lease': housing_resources.get_lease_display(),
                'month_rent': housing_resources.month_rent,
                'community': housing_resources.community,
                'category': housing_resources.category,
                'direction': housing_resources.get_direction_display(),
                'layer': housing_resources.layer,
                'total_layer': housing_resources.total_layer,
                'sitting_room_area': housing_resources.sitting_room_area,
                'area': housing_resources.area,
                'infrastructures': infrastructures,
                'subway': housing_resources.subway,
                'bus': housing_resources.bus,
                'buy': housing_resources.buy,
                'address': housing_resources.address,
                'pictures': housing_resources.get_pictures(),
            }
        except Exception as e:
            logging.error(e)
            logging.error("----------------HouseResourceDetailView-----------------")
            return JsonResponse({'error_code': 1, 'error_msg': '获取失败'})

        return JsonResponse({
            'error_code': 0,
            'error_msg': '请求成功',
            'data': {
                'house': house
            }
        })
