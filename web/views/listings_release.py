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
    HousingResources
)

from imagestore.qiniu_manager import(
    get_extension,
    handle_uploaded_file,
    upload,
    url,
)

from utils import (
    paging_objs,
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

    objs = HousingResources.obs.get_queryset().order_by('-created')

    page = request.GET.get('page', 1)
    clients = paging_objs(
        object_list=objs,
        per_page=BACK_PAGE_COUNT,
        page=page)

    context = {
        'module': 'listings_release',
        'clients': clients,
    }

    return render(request, 'super/release/listings/list.html', context)


@staff_member_required(login_url='/admin/login')
def offline(request, housingresources_id):
    page = request.GET.get('page', '')

    client = HousingResources.objects.filter(pk=housingresources_id).first()
    if client:
        client.audit_status = 1
        client.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@staff_member_required(login_url='/admin/login')
def online(request, housingresources_id):
    page = request.GET.get('page', '')
    client = HousingResources.objects.filter(pk=housingresources_id).first()
    if client:
        client.audit_status = 2
        client.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
