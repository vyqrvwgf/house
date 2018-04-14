# coding: utf-8

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.db.models import Max, Min
from web.models import (
    HouseDemand
)
from imagestore.qiniu_manager import(
    get_extension,
    handle_uploaded_file,
    upload,
    url,
)
from settings import (
    BACK_PAGE_COUNT, FILED_CHECK_MSG,
    UPLOAD_DIR,
)
import os
import datetime
import time


@staff_member_required(login_url='/admin/login')
def list(request):
    page = request.GET.get('page', 1)
    param_mobile = request.GET.get('param_mobile', '')

    clients = HouseDemand.objects.filter(is_del=False).order_by('-created')
    # 筛选结果集
    if param_mobile:
        clients = clients.filter(mobile__icontains=param_mobile)

    paginator = Paginator(clients, BACK_PAGE_COUNT)

    try:
        clients = paginator.page(page)
    except PageNotAnInteger:
        clients = paginator.page(1)
    except EmptyPage:
        clients = paginator.page(paginator.num_pages)

    context = {
        'module': 'house_demand',
        'clients': clients,
        'page': page,
        'param_mobile': param_mobile,
    }
    template = loader.get_template('super/house_demand/list.html')
    return HttpResponse(template.render(context, request))
