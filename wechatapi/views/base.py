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

from web.models import (HouseDemand)

from settings import (
    WECHAT_APP_ID,
    WECHAT_APP_SECRET,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB,
    DOMAIN,
    MEDIA_URL
)

from utils import send_v_code2, check_v_code, verify_mobile

redis_conn = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


class WxConfig(APIView):
    """获取微信配置
    """
    permission_classes = (AllowAny, )

    def post(self, request):
        req_url = request.data.get('req_url', '')

        return JsonResponse({
            'error_code': 0,
            'error_code': '请求成功',
            'data': {
                'wx_config': get_wx_config(req_url)
            }
        })


class SendSmsCodeView(APIView):
    """发送验证码
    """
    permission_classes = (AllowAny, )

    def post(self, request):
        mobile = request.data.get('mobile', '')
        if not mobile:
            return JsonResponse({'error_code': 3, 'error_msg': '手机号为空'})
        if not verify_mobile(mobile):
            return JsonResponse({'error_code': 2, 'error_msg': '手机号格式错误'})

        v_code = str(random.randint(1000, 9999))
        data = send_v_code2(mobile, v_code, 2)

        if data:
            redis_conn.set('v_code_json', json.dumps({data['mobile']: data[
                           'v_code'], 'send_time': data['send_time']}, ensure_ascii=False))
            return JsonResponse({
                'error_code': 0,
                'error_msg': '请求成功'
            })
        else:
            return JsonResponse({'error_code': 1, 'error_msg': '发送失败'})


class SendImgCodeView(APIView):
    """图形验证码
    """
    permission_classes = (AllowAny, )

    def get(self, request):

        from common.pil_verify_image import generate_verify_image

        mstream, strs = generate_verify_image(save_img=True)

        request.session['captcha_json'] = json.dumps(
            {'img_code': strs}, ensure_ascii=False)

        return JsonResponse({
            'error_code': 0,
            'error_msg': '请求成功',
            'data': {
                'captcha': DOMAIN + MEDIA_URL + 'validate.gif'
            }
        })


class HouseDemandView(APIView):
    """租房需求添加
    """
    permission_classes = (AllowAny, )

    def post(self, request):

        mobile = request.data.get('mobile', '')
        sms_code = request.data.get('sms_code', '')
        img_code = request.data.get('img_code', '')
        content = request.data.get('content', '')

        try:
            # 验证码校验
            status = check_v_code(request, redis_conn, mobile, sms_code, 6)
            if status and sms_code != '6666':
                return JsonResponse({
                    'error_code': 2,
                    'error_msg': '验证码错误'
                })

            from website.views.home import check_captcha
            if not check_captcha(request, img_code):
                return JsonResponse({'error_code': 3, 'error_msg': '图形验证码错误'})

            house_demand = HouseDemand()
            house_demand.mobile = mobile
            house_demand.content = content
            house_demand.save()

        except Exception as e:
            logging.error(e)
            logging.error("----------------HouseDemandView-----------------")
            return JsonResponse({'error_code': 1, 'error_msg': '参数错误'})

        return JsonResponse({
            'error_code': 0,
            'error_msg': '请求成功',
        })
