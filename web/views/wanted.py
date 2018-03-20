# coding: utf-8

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from xlrd import xldate_as_tuple
from django.db.models import Q
from django.db import transaction
from django.db.models import Max, Min
from web.models import (
    RentHouse,
    RentHouseMeet,
    Infrastructure,
)

from imagestore.qiniu_manager import(
    get_extension,
    handle_uploaded_file,
    upload,
    url,
)

from utils import (
    paging_objs,
    excel_table
)

from settings import (
    BACK_PAGE_COUNT, FILED_CHECK_MSG,
    UPLOAD_DIR, QQ_MAP_API_URL
)

import os
import datetime
import time
import logging


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
        objs = objs.filter(phone__icontains=search_name)

    search_lease = request.GET.get('search_lease', -1)
    search_lease = int(search_lease) if search_lease else -1
    context['search_lease'] = search_lease
    if search_lease != -1:
        objs = objs.filter(lease=search_lease)

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


@staff_member_required(login_url='/admin/login')
def import_data(request):
    context = {}
    context['module'] = 'wanted'

    if request.method == 'POST':
        issue_time = request.POST.get('issue_time', '')

        while True:
            file = request.FILES.get('data', None)
            if not file:
                context['error1'] = '文件不能为空'
                break

            try:
                with transaction.atomic():
                    table = excel_table(file)
                    dataset = []
                    for row in table:
                        if row[0]:
                            rent_house = RentHouse()
                            rent_house.user = request.user
                            for r in RentHouse.RENT_CHOICES:
                                if r[1] == row[3]:
                                    rent_house.rent = r[0]

                            rent_house.description = row[10]
                            rent_house.province = row[4]
                            rent_house.city = row[5]
                            rent_house.area = row[6]
                            date = datetime.datetime(*xldate_as_tuple(row[7], 0))
                            rent_house.date = date.strftime("%Y/%m/%d")
                            rent_house.save()
                            for r in row[8].split(','):
                                infrastructure = Infrastructure.obs.get_queryset().filter(name__icontains=r).first()
                                if infrastructure:
                                    rent_house.infrastructure.add(infrastructure)

                            if row[9] == u'整租':
                                rent_house.lease = 1

                            rent_house.name = row[1]
                            rent_house.phone = str(int(row[2]))
                            rent_house.audit_status = 2

                            rent_house.save()

                return HttpResponseRedirect(reverse('web:wanted_list'))
            except Exception as e:
                logging.error(e)
                context['error1'] = '导入失败'
                break

            break

    return render(request, 'super/housing/wanted/import.html', context)

