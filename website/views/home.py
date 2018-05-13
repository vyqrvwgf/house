# coding: utf-8

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from captcha.image import ImageCaptcha
from django.db.models import Q, Avg
from django.template import loader

from django.contrib.auth import login, logout, authenticate
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from web.models import(
    Advertising,
    Profile,
    HousingResources,
    FeedBack,
    HousingEvaluation,
    RentHouse,
    RentHouseMeet,
    HousingResourcesMeet
)

from imagestore.qiniu_manager import (
    get_extension,
    handle_uploaded_file,
    upload
)

from utils import(
    send_v_code,
    check_v_code,
    md5_create,
    verify_mobile,
    jwt_token_gen,
    jwt_token_decode,
    get_xinxing,
    get_area,
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
    housingresources_list = HousingResources.obs.get_queryset().filter(audit_status=2, status=2)
    housingresources_list1 = housingresources_list.order_by('-updated')[:8]
    housingresources_list2 = housingresources_list.filter(quality=1).order_by('-updated')[:8]
    housingresources_list3 = housingresources_list.order_by('-click_count')[:8]

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
        audit_status=2, status=2).order_by('-updated')

    if keyword:
        housingresources_list = housingresources_list.filter(
            Q(community__icontains=keyword) | Q(address__icontains=keyword) | Q(content__icontains=keyword))

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

    housingresources_list = HousingResources.obs.get_queryset().filter(
        audit_status=2,
        status=2,
    )
    if request.method == 'POST':
        area = request.POST.get('area', '')
        price = request.POST.get('price', '')
        structure = request.POST.get('structure', '')
        waytorent = request.POST.get('waytorent', '')
        start_price = request.POST.get('start_price', '')
        end_price = request.POST.get('end_price', '')

        print request.POST
        if area and area != u'不限':
            housingresources_list = housingresources_list.filter(area__icontains=area)
        
        if start_price:
            housingresources_list = housingresources_list.filter(month_rent__gte=start_price)
        
        if end_price:
            housingresources_list = housingresources_list.filter(month_rent__lte=end_price)

        if not start_price and not end_price and price and price != u'不限':
            price_list = price.split('-')
            start_price = price_list[0]
            end_price = price_list[1] if len(price_list) > 1 else 0
            if not end_price:
                housingresources_list = housingresources_list.filter(month_rent__lte=int(start_price))
            else:
                housingresources_list = housingresources_list.filter(
                    month_rent__gte=int(start_price),
                    month_rent__lte=int(end_price),
                )  

        if structure and structure != u'不限':
            housingresources_list = housingresources_list.filter(category__icontains=structure)

        if waytorent == u'整租':
            housingresources_list = housingresources_list.filter(lease=0)
        elif waytorent == u'合租':
            housingresources_list = housingresources_list.filter(lease=1)

        tmp = loader.get_template('frontend/load-roomResource.html')
        html = tmp.render({'housingresources_list': housingresources_list})
        return JsonResponse({'html': html})

    housingresources_list = housingresources_list.filter(area__icontains=u'洪山')

    context = {
        'module': 'housing_resources',
        'housingresources_list': housingresources_list,
    }

    return render(request, 'frontend/02-1-roomResource-1.html', context)


def housing_resources_map_list(request):

    housingresources_list = HousingResources.obs.get_queryset().filter(audit_status=2, status=2)

    context = {
        'module': 'housing_resources',
        'qq_map_api_url': QQ_MAP_API_URL,
        'housingresources_list': housingresources_list,
    }

    return render(request, 'frontend/02-1-roomResource-2.html', context)


def housing_resources(request, housing_resources_id):

    housing_resources = HousingResources.objects.get(pk=housing_resources_id)
    housing_evaluations = HousingEvaluation.obs.get_queryset().filter(
        housing_resources=housing_resources).order_by('-created')

    # 增加点击量
    if request.user and not request.user.is_staff:
        housing_resources.click_count += 1
        housing_resources.save()

    for he in housing_evaluations:
        he.point_str = get_xinxing(he.point, 5)
        if not he.niming:
            he.user.username = he.user.username[
                0] + u'***' + he.user.username[-1]

    avg_point = housing_evaluations.aggregate(
        avg_point=Avg('point'))['avg_point']

    point_str = get_xinxing(avg_point, 5)

    # 同小区房源
    tongxiaoquhousing = HousingResources.obs.get_queryset().filter(
        community=housing_resources.community,
        audit_status=2,
        status=2
    )

    # 附近小区
    lat_scope, lng_scope = get_area(housing_resources.lat, housing_resources.lng, 10, 3)
    fujinxiaoqufangyuan = HousingResources.obs.get_queryset().filter(
        lat__in=lat_scope,
        lng__in=lng_scope,
        audit_status=2,
        status=2
    )

    context = {
        'module': 'housing_resources',
        'qq_map_api_url': QQ_MAP_API_URL,
        'housing_resources': housing_resources,
        'housing_evaluations': housing_evaluations,
        'tongxiaoquhousing': tongxiaoquhousing,
        'fujinxiaoqufangyuan': fujinxiaoqufangyuan,
        'point_str': point_str,
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
        img_code = request.POST.get('img_code', '')
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

                if not check_captcha(request, img_code):
                    return JsonResponse({'error_code': 1, 'error_msg': '图形验证码错误'})

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

                user = User.objects.create_user(phoneNum, email, md5_create(DB_PREFIX + password1))
                profile = Profile.objects.create(
                    user=user,
                    user_name=phoneNum,
                    mobile=phoneNum,
                    email=email,
                    password=md5_create(DB_PREFIX + password1)
                )

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


@csrf_exempt
def send_vcode(request):

    mobile = request.POST.get('mobile', '')
    if not mobile:
        return JsonResponse({'error_code': 3, 'error_msg': '手机号为空'})

    if not verify_mobile(mobile):
        return JsonResponse({'error_code': 2, 'error_msg': '手机号格式错误'})

    v_code = str(random.randint(1000, 9999))

    data = send_v_code(mobile, v_code, 2)
    if data:
        redis_conn.set('v_code_json', simplejson.dumps(
            {data['mobile']: data['v_code'], 'send_time': data['send_time']}, ensure_ascii=False)
        )
        return JsonResponse({'error_code': 0, 'error_msg': '验证码发送成功'})
    else:
        return JsonResponse({'error_code': 1, 'error_msg': '发送失败'})


@csrf_exempt
def send_vcode1(request):

    mobile = request.POST.get('mobile', '')
    if not mobile:
        return JsonResponse({'error_code': 3, 'error_msg': '手机号为空'})

    if not verify_mobile(mobile):
        return JsonResponse({'error_code': 2, 'error_msg': '手机号格式错误'})

    v_code = str(random.randint(1000, 9999))

    data = send_v_code(mobile, v_code, 2)
    if data:
        redis_conn.set('v_code_json', simplejson.dumps(
            {data['mobile']: data['v_code'], 'send_time': data['send_time']}, ensure_ascii=False)
        )
        return JsonResponse({'error_code': 0, 'error_msg': '验证码发送成功'})
    else:
        return JsonResponse({'error_code': 1, 'error_msg': '发送失败'})


@csrf_exempt
def housing_resources_meet_create(request):
    try:
        with transaction.atomic():
            c_user = request.session.get('c_user', {})
            profile = Profile.obs.get_queryset().filter(pk=c_user.get('id', 0)).first()

            housing_resources_id = request.POST.get('housing_resources_id', 0)
            select_date = request.POST.get('select_date', '')
            meet_time = datetime.datetime.strptime(select_date, "%Y-%m-%d")
            housing_resources = HousingResources.objects.get(pk=housing_resources_id)
            housing_resources_meet, _ = HousingResourcesMeet.objects.get_or_create(
                user=profile.user,
                housing_resources=housing_resources
            )
            housing_resources_meet.meet_time = meet_time
            housing_resources_meet.save()

    except Exception as e:
        logging.error(e)
        return JsonResponse({'error_code': 1, 'error_msg': '预约失败'})

    return JsonResponse({'error_code': 0, 'error_msg': '已接受预约工作人员会在一个工作日内协助完成预约。'})


def captcha(request):
    '''验证码
    '''
    from common.pil_verify_image import generate_verify_image

    mstream, strs = generate_verify_image(save_img=True)

    request.session['captcha_json'] = simplejson.dumps(
        {'img_code': strs}, ensure_ascii=False)
    print request.session['captcha_json']
    return HttpResponse('data:image/gif;base64,' + mstream.getvalue().encode('base64'))


def check_captcha(request, code):

    captcha_json = request.session.get('captcha_json', '')
    if not captcha_json:
        return False

    captcha_obj = simplejson.loads(captcha_json)
    s_code = captcha_obj['img_code'].strip().lower()
    t_code = code.strip().lower()

    if not s_code == t_code:
        return False

    return True
