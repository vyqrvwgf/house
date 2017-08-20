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
    Profile
)

from utils import(
    send_v_code, check_v_code, md5_create,
    jwt_token_gen, jwt_token_decode, website_check_login
)

from settings import (
    DB_PREFIX,
    DOMAIN,
    QINIU_DOMAIN
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
	context = {
		'module': 'index',
		'client': profile,
		'qiniu_domain': QINIU_DOMAIN
	}

	return render(request, 'frontend/user/index.html', context)


@website_check_login
def login_out(request):
	if request.session.get('c_user', None):
		del request.session['c_user']

	return HttpResponseRedirect(reverse('website:home_index'))

