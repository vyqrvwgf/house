# coding: utf-8

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.template import loader
from django.contrib.auth import login, logout, authenticate
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.views.decorators.csrf import csrf_exempt
from web.models import(
    Advertising,
    Profile,
    HousingResources,
    FeedBack,
)

from imagestore.qiniu_manager import (
    get_extension,
    handle_uploaded_file,
    upload
)

from utils import(
    send_v_code, check_v_code, md5_create,
    jwt_token_gen, jwt_token_decode
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

redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


def index(request):
    # 获取第多少为服务用户
    c_user = request.session.get('c_user', {})
    profile = Profile.obs.get_queryset().filter(pk=c_user.get('id', 0)).first()
    total_profile = Profile.obs.get_queryset().count()
    fuwu_number = profile.id if profile else total_profile + 1

    advertising_list = Advertising.obs.get_queryset().order_by('-order_no')
    housingresources_list = HousingResources.obs.get_queryset()
    housingresources_list1 = housingresources_list.order_by('-updated')[:8]
    housingresources_list2 = housingresources_list.order_by('-click_count')[:8]
    housingresources_list3 = housingresources_list.filter(hot=1)[:8]

    context = {
        'module': 'index',
        'advertisings': advertising_list,
        'fuwu_number': fuwu_number,
        'advertising_count': advertising_list.count(),
        'housingresources_list1': housingresources_list1,
        'housingresources_list2': housingresources_list2,
        'housingresources_list3': housingresources_list3,
    }

    return render(request, 'frontend/index.html', context)


def search(request):
    keyword = request.GET.get('keyword', '')

    advertising_list = Advertising.obs.get_queryset().order_by('-order_no')
    housingresources_list = HousingResources.obs.get_queryset().filter(
        audit_status=2).order_by('-updated')

    if keyword:
        housingresources_list = housingresources_list.filter(
            Q(community__icontains=keyword) | Q(address__icontains=keyword))

    context = {
        'module': 'index',
        'keyword': keyword,
        'advertisings': advertising_list,
        'advertising_count': advertising_list.count(),
        'housingresources_list': housingresources_list
    }

    return render(request, 'frontend/search.html', context)


@csrf_exempt
def feedback_add(request):

    try:
        suggestion = request.POST.get('suggestion', '')
        if not suggestion:
            raise Exception("I know python!")

        feedback = FeedBack()
        feedback.content = suggestion
        feedback.user = request.user if request.user else None
        feedback.save()

    except Exception as e:
        logging.error(e)
        return JsonResponse({
            'error_code': 1,
            'error_msg': '保存失败',
        })

    return JsonResponse({
        'error_code': 0,
        'error_msg': '已提交平台管理，请等待'
    })


def housing_resources_list(request):

    housingresources_list = HousingResources.obs.get_queryset()

    context = {
        'module': 'housing_resources',
        'housingresources_list': housingresources_list,
    }

    return render(request, 'frontend/02-1-roomResource-1.html', context)


def housing_resources_map_list(request):

    housingresources_list = HousingResources.obs.get_queryset()

    context = {
        'module': 'housing_resources',
        'housingresources_list': housingresources_list,
    }

    return render(request, 'frontend/02-1-roomResource-2.html', context)


def rent_house_list(request):

    housingresources_list = HousingResources.obs.get_queryset()

    context = {
        'module': 'rent_house',
        'housingresources_list': housingresources_list,
    }

    return render(request, 'frontend/03-findToRent.html', context)


def housing_resources(request, housing_resources_id):

    housing_resources = HousingResources.objects.get(pk=housing_resources_id)

    context = {
        'module': 'housing_resources',
        'qq_map_api_url': QQ_MAP_API_URL,
        'housing_resources': housing_resources,
    }

    return render(request, 'frontend/02-2-roomInfo.html', context)


@csrf_exempt
def register(request):

    context = {
        'module': 'index',
        'domain': DOMAIN
    }
    if request.method == 'POST':
        phoneNum = request.POST.get('phoneNum', '')
        vcode = request.POST.get('vcode', '')
        email = request.POST.get('email', '')
        password1 = request.POST.get('password1', '')
        password2 = request.POST.get('password2', '')

        with transaction.atomic():
            try:
                if not phoneNum or not vcode\
                        or not email or not password1\
                        or not password2 or password1 != password2\
                        or '@' not in email:
                    return JsonResponse({
                        'error_code': 2,
                        'error_msg': '却少参数'
                    })

                # 验证码校验
                status = check_v_code(request, redis_conn, phoneNum, vcode, 6)
                if status and vcode != '6666':
                    return JsonResponse({
                        'error_code': 3,
                        'error_msg': '验证码错误'
                    })

                is_register = Profile.objects.filter(
                    is_del=False,
                    is_valid=True,
                    mobile=phoneNum
                ).exists()
                if is_register:
                    return JsonResponse({
                        'error_code': 4,
                        'error_msg': '该手机号码已注册'
                    })

                profile = Profile.objects.create(
                    user_name=phoneNum,
                    mobile=phoneNum,
                    email=email,
                    password=md5_create(DB_PREFIX + password1)
                )

                user = profile.get_user()
                token = jwt_token_gen(user)
                profile.jwt_token = token
                profile.save()

                # 存入用户到session中
                request.session['c_user'] = {
                    'id': profile.id,
                    'user_name': profile.user_name,
                    'email': profile.email,
                    'mobile': profile.mobile
                }

            except Exception as e:
                logging.error(e)
                return JsonResponse({
                    'error_code': 1,
                    'error_msg': '注册失败'
                })

        return JsonResponse({
            'error_code': 0,
            'error_msg': '注册成功'
        })

    return render(request, 'frontend/register.html', context)


@csrf_exempt
def login(request):

    context = {
        'module': 'index',
        'domain': DOMAIN
    }
    if request.method == 'POST':
        userName = request.POST.get('userName', '')
        userPass = request.POST.get('userPass', '')

        if not userPass or not userName:
            return JsonResponse({
                'error_code': 1,
                'error_msg': '却少参数'
            })

        profile = Profile.objects.filter(
            is_del=False,
            is_valid=True,
        ).filter(Q(mobile=userName) | Q(email=userName)).first()

        is_right_profile = profile.password == md5_create(
            DB_PREFIX + userPass) if profile else False
        if not profile or not is_right_profile:
            return JsonResponse({
                'error_code': 2,
                'error_msg': '用户名或密码不正确'
            })

        # 存入用户到session中
        profile.is_del = False
        profile.save()

        request.session['c_user'] = {
            'id': profile.id,
            'user_name': profile.user_name,
            'email': profile.email,
            'mobile': profile.mobile
        }

        return JsonResponse({
            'error_code': 0,
            'error_msg': '登陆成功'
        })

    return render(request, 'frontend/login.html', context)


@csrf_exempt
def upload_file(request):

    keys = ''
    try:
        if request.FILES.get('file', None):
            file = request.FILES.get('file', None)
            # 上传图片
            id_card_picture = file
            ts = int(time.time())
            ext = get_extension(id_card_picture.name)
            key = 'id_card_picture_{}.{}'.format(ts, ext)
            handle_uploaded_file(id_card_picture, key)
            upload(key, os.path.join(UPLOAD_DIR, key))
    except Exception as e:
        logging.error(e)
        return JsonResponse({
            'error_code': 1,
            'error_msg': '保存失败',
        })

    return JsonResponse({
        'error_code': 0,
        'error_msg': '保存成功',
        'data': {
            'key': key
        }
    })
