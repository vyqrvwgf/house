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
    RentHouse,
    RentHouseMeet,
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
    UPLOAD_DIR, QQ_MAP_API_URL
)

import os
import datetime
import time


@staff_member_required(login_url='/admin/login')
def list(request):
    context = {
        'module': 'wanted'
    }
    objs = RentHouse.obs.get_queryset().filter(
        audit_status=2
    ).order_by('-created')

    search_name = request.GET.get('search_name', '')
    if search_name:
        context['search_name'] = search_name
        objs = objs.filter(content__icontains=search_name)

    search_lease = request.GET.get('search_lease', -1)
    search_lease = int(search_lease) if search_lease else -1
    context['search_lease'] = search_lease
    if search_lease != -1:
        objs = objs.filter(lease=search_lease)

    search_status = request.GET.get('search_status', -1)
    search_status = int(search_status) if search_status else 0
    context['search_status'] = search_status
    if search_status != -1:
        objs = objs.filter(status=search_status)

    search_start = request.GET.get('search_start', '')
    if search_start:
        context['search_start'] = search_start
        start_date = datetime.datetime.strptime(search_start, '%Y-%m-%d')
        objs = objs.filter(created__gte=start_date)

    search_end = request.GET.get('search_end', '')
    if search_end:
        context['search_end'] = search_end
        end_date = datetime.datetime.strptime(search_end, '%Y-%m-%d')
        objs = objs.filter(created__lte=end_date)

    page = request.GET.get('page', 1)
    clients = paging_objs(
        object_list=objs,
        per_page=BACK_PAGE_COUNT,
        page=page)

    context['clients'] = clients

    return render(request, 'super/housing/wanted/list.html', context)


@staff_member_required(login_url='/admin/login')
def offline(request, renthouse_id):
    page = request.GET.get('page', '')

    client = RentHouse.objects.filter(pk=renthouse_id).first()
    if client:
        client.status = 1
        client.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@staff_member_required(login_url='/admin/login')
def online(request, renthouse_id):
    page = request.GET.get('page', '')
    client = RentHouse.objects.filter(pk=renthouse_id).first()
    if client:
        client.status = 2
        client.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@staff_member_required(login_url='/admin/login')
def delete(request, renthouse_id):
    page = request.GET.get('page', '')
    client = RentHouse.objects.filter(pk=renthouse_id).first()
    if client:
        client.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@staff_member_required(login_url='/admin/login')
def meet_list(request):
    context = {
        'module': 'wanted_meet'
    }
    objs = RentHouseMeet.obs.get_queryset().order_by('-created')

    search_start = request.GET.get('search_start', '')
    if search_start:
        context['search_start'] = search_start
        start_date = datetime.datetime.strptime(search_start, '%Y-%m-%d')
        objs = objs.filter(created__gte=start_date)

    search_end = request.GET.get('search_end', '')
    if search_end:
        context['search_end'] = search_end
        end_date = datetime.datetime.strptime(search_end, '%Y-%m-%d')
        objs = objs.filter(created__lte=end_date)

    page = request.GET.get('page', 1)
    clients = paging_objs(
        object_list=objs,
        per_page=BACK_PAGE_COUNT,
        page=page)

    context['clients'] = clients

    return render(request, 'super/housing/wanted/meet/list.html', context)


@staff_member_required(login_url='/admin/login')
def meet_complete(request, renthouse_meet_id):
    page = request.GET.get('page', '')
    client = RentHouseMeet.objects.filter(pk=renthouse_meet_id).first()
    if client:
        client.status = 1
        client.comp_meet_time = datetime.datetime.now()
        client.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@staff_member_required(login_url='/admin/login')
def meet_delete(request, renthouse_meet_id):
    page = request.GET.get('page', '')
    client = RentHouseMeet.objects.filter(pk=renthouse_meet_id).first()
    if client:
        client.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

