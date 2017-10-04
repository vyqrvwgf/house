# coding: utf-8

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.template import loader
from django.contrib.auth import login, logout, authenticate
from django.contrib.admin.views.decorators import staff_member_required
from django.db import transaction
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from web.models import(
    Advertising,
    Profile,
    Infrastructure
)
from imagestore.qiniu_manager import(
    get_extension,
    handle_uploaded_file,
    upload,
    url
)

from utils import(
    send_v_code, check_v_code, md5_create,
    jwt_token_gen, jwt_token_decode, website_check_login
)

from settings import (
    DB_PREFIX,
    DOMAIN,
    QINIU_DOMAIN,
    UPLOAD_DIR,
)

import os
import datetime
import time
import random
import string
import redis
import logging


@website_check_login
def index(request):
	c_user = request.session.get('c_user', None)
	profile = Profile.objects.filter(is_del=False, pk=c_user['id']).first()
	infrastructures = Infrastructure.objects.filter(
		is_del=False,
		is_valid=True
	).order_by('-order_no')


	context = {
		'module': 'index',
		'sub_module': 'user_index',
		'client': profile,
		'infrastructures': infrastructures,
		'qiniu_domain': QINIU_DOMAIN,
	}

	return render(request, 'frontend/user/index.html', context)


@website_check_login
def housing_resource_create(request):
	c_user = request.session.get('c_user', None)
	profile = Profile.objects.filter(is_del=False, pk=c_user['id']).first()
	infrastructures = Infrastructure.objects.filter(
		is_del=False,
		is_valid=True
	).order_by('-order_no')


	context = {
		'module': 'index',
		'sub_module': 'housing_resource_create',
		'client': profile,
		'infrastructures': infrastructures,
		'qiniu_domain': QINIU_DOMAIN,
	}

	return render(request, 'frontend/user/housing_resource_create.html', context)


@website_check_login
def login_out(request):
	if request.session.get('c_user', None):
		del request.session['c_user']

	return HttpResponseRedirect(reverse('website:home_index'))


@csrf_exempt
def update_profile(request):
	c_user_id = request.POST.get('c_user_id', '')
	user_name = request.POST.get('user_name', '')
	gender = request.POST.get('gender', '')
	birbath = request.POST.get('birbath', '')
	mobile = request.POST.get('mobile', '')
	bank_acount = request.POST.get('bank_acount', '')
	id_card = request.POST.get('id_card', '')

	try:
		profile = Profile.objects.filter(is_del=False, pk=c_user_id).first()
		profile.user_name = user_name

		profile.gender = gender
		profile.birbath = birbath
		profile.mobile = mobile
		profile.bank_acount = bank_acount
		profile.id_card = id_card

		if request.FILES:
			if request.FILES.get('test-image-file', None):
				# 上传图片
				id_card_picture = request.FILES['test-image-file']

				ts = int(time.time())
				ext = get_extension(id_card_picture.name)
				key = 'id_card_picture_{}.{}'.format(ts, ext)
				handle_uploaded_file(id_card_picture, key)
				upload(key, os.path.join(UPLOAD_DIR, key))
				profile.id_card_picture = key

		profile.save()

	except Exception as e:
		logging.error(e)
		return JsonResponse({
			'error_code': 1,
			'error_msg': '保存失败',
		})

	return JsonResponse({
		'error_code': 0,
		'error_msg': '保存成功',
	})

