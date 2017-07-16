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
    Infrastructure
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

    clients = Infrastructure.objects.filter(is_del=False).order_by('order_no')

    paginator = Paginator(clients, BACK_PAGE_COUNT)
    page = request.GET.get('page', '')

    try:
        clients = paginator.page(page)
    except PageNotAnInteger:
        clients = paginator.page(1)
    except EmptyPage:
        clients = paginator.page(paginator.num_pages)

    context = {
        'module': 'infrastructure',
        'clients': clients,
    }

    return render(request, 'super/housing/infrastructure/list.html', context)


@staff_member_required(login_url='/admin/login')
def create(request):
    context = {
        'module': 'infrastructure'
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

    return render(request, 'super/housing/infrastructure/create.html', context)


@staff_member_required(login_url='/admin/login')
def edit(request, infrastructure_id):
    page = request.GET.get('page', '')
    client = Infrastructure.objects.filter(id=infrastructure_id).first()
    context = {
        'client': client,
        'module': 'infrastructure',
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

    return render(request, 'super/housing/infrastructure/create.html', context)


@staff_member_required(login_url='/admin/login')
def delete(request, infrastructure_id):
    page = request.GET.get('page', '')
    client = Infrastructure.objects.filter(pk=infrastructure_id).first()
    if client:
        client.delete()
    return HttpResponseRedirect(reverse('web:infrastructure_list')
        + '?page=' + page
    )


@staff_member_required(login_url='/admin/login')
def up(request, infrastructure_id):
    page = request.GET.get('page', '')
    infrastructure = Infrastructure.objects.filter(pk=infrastructure_id).first()
    if infrastructure:
        before_infrastructures = Infrastructure.objects.filter(
            order_no__lt=infrastructure.order_no,
            is_del=False,
        ).order_by('-order_no')
        if before_infrastructures:
            # 旧
            before_infrastructure = before_infrastructures[0]
            old_order_no = infrastructure.order_no
            infrastructure.order_no = before_infrastructure.order_no
            infrastructure.save()
            # 新
            before_infrastructure.order_no = old_order_no
            before_infrastructure.save()
    return HttpResponseRedirect(reverse('web:infrastructure_list')
        + '?page=' + page
    )


@staff_member_required(login_url='/admin/login')
def down(request, infrastructure_id):
    page = request.GET.get('page', '')
    infrastructure = Infrastructure.objects.filter(pk=infrastructure_id).first()
    if infrastructure:
        after_infrastructures = Infrastructure.objects.filter(
            order_no__gt=infrastructure.order_no,
            is_del=False,
        ).order_by('order_no')

        if after_infrastructures:
            # 旧
            after_infrastructure = after_infrastructures[0]
            old_order_no = infrastructure.order_no
            infrastructure.order_no = after_infrastructure.order_no
            infrastructure.save()
            # 新
            after_infrastructure.order_no = old_order_no
            after_infrastructure.save()

    return HttpResponseRedirect(reverse('web:infrastructure_list')
        + '?page=' + page
    )

