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

from settings import (
    BACK_PAGE_COUNT, FILED_CHECK_MSG,
    UPLOAD_DIR,
)

import os
import datetime
import time


@staff_member_required(login_url='/admin/login')
def list(request):

    clients = HousingResources.objects.filter(
        is_del=False,
        is_valid=True,
        audit_status=2
    ).order_by('-created')

    paginator = Paginator(clients, BACK_PAGE_COUNT)
    page = request.GET.get('page', '')

    try:
        clients = paginator.page(page)
    except PageNotAnInteger:
        clients = paginator.page(1)
    except EmptyPage:
        clients = paginator.page(paginator.num_pages)

    context = {
        'module': 'listings',
        'clients': clients,
    }

    return render(request, 'super/housing/listings/list.html', context)


@staff_member_required(login_url='/admin/login')
def create(request):
    context = {
        'module': 'listings'
    }

    if request.method == 'POST':
        error = {}
        name = request.POST.get('name', '')
        flag = True
        infrastructure = Infrastructure()

        if not len(name):
            flag = False
            error['name_msg'] = FILED_CHECK_MSG
        else:
            infrastructure.name = name

        if flag:
            if request.FILES:
                if request.FILES.get('cover', None):
                    # 上传图片
                    img = request.FILES['cover']
                    ts = int(time.time())
                    ext = get_extension(img.name)
                    key = 'cover_{}.{}'.format(ts, ext)
                    handle_uploaded_file(img, key)
                    upload(key, os.path.join(UPLOAD_DIR, key))
                    infrastructure.cover = key

            infrastructure.save()
            infrastructure.order_no = infrastructure.id
            infrastructure.save()
            return HttpResponseRedirect(reverse('web:infrastructure_list'))
        else:
            context['client'] = infrastructure
            context['error'] = error

    return render(request, 'super/housing/listings/create.html', context)


@staff_member_required(login_url='/admin/login')
def edit(request, infrastructure_id):
    page = request.GET.get('page', '')
    client = Infrastructure.objects.filter(id=infrastructure_id).first()
    context = {
        'client': client,
        'module': 'listings',
        'page': page,
    }

    if request.method == 'POST':
        error = {}
        name = request.POST.get('name', '')

        flag = True

        if not len(name):
            flag = False
            error['name_msg'] = FILED_CHECK_MSG
        else:
            client.name = name

        if flag:
            if request.FILES:
                if request.FILES.get('cover', None):
                    # 上传图片
                    img = request.FILES['cover']
                    ts = int(time.time())
                    ext = get_extension(img.name)
                    key = 'cover_{}.{}'.format(ts, ext)
                    handle_uploaded_file(img, key)
                    upload(key, os.path.join(UPLOAD_DIR, key))
                    client.cover = key

            client.save()
            return HttpResponseRedirect(reverse('web:infrastructure_list')
                + '?page=' + page
            )
        else:
            context['error'] = error

    return render(request, 'super/housing/listings/create.html', context)


@staff_member_required(login_url='/admin/login')
def offline(request, housingresources_id):
    page = request.GET.get('page', '')

    client = HousingResources.objects.filter(pk=housingresources_id).first()
    if client:
        client.status = 1
        client.save()

    return HttpResponseRedirect(reverse('web:listings_list')
        + '?page='+ str(page)
    )


@staff_member_required(login_url='/admin/login')
def online(request, housingresources_id):
    page = request.GET.get('page', '')
    client = HousingResources.objects.filter(pk=housingresources_id).first()
    if client:
        client.status = 2
        client.save()

    return HttpResponseRedirect(reverse('web:listings_list')
        + '?page='+ str(page)
    )


@staff_member_required(login_url='/admin/login')
def delete(request, housingresources_id):
    page = request.GET.get('page', '')
    client = HousingResources.objects.filter(pk=housingresources_id).first()
    if client:
        client.delete()
    return HttpResponseRedirect(reverse('web:listings_list')
        + '?page=' + page
    )
