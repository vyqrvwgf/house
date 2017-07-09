# coding: utf-8

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.template import loader
from django.contrib.auth import login, logout, authenticate
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.urlresolvers import reverse
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

from imagestore.qiniu_manager import(
    get_extension,
    handle_uploaded_file,
    upload,
    url,
)

from web.models import(
	Advertising
)
from settings import(
    BACK_PAGE_COUNT, FILED_CHECK_MSG,
    UPLOAD_DIR
)
import os
import datetime
import time
import simplejson
import re
import requests


@staff_member_required(login_url='/admin/login')
def index(request):

    context = {
        'module': 'home',
    }
    return render(request, 'super/index.html', context)


@staff_member_required(login_url='/admin/login')
def advertising_list(request):

    clients = Advertising.objects.filter(is_del=False).order_by('order_no')

    paginator = Paginator(clients, BACK_PAGE_COUNT)
    page = request.GET.get('page', '')

    try:
        clients = paginator.page(page)
    except PageNotAnInteger:
        clients = paginator.page(1)
    except EmptyPage:
        clients = paginator.page(paginator.num_pages)

    context = {
        'module': 'homepage',
        'clients': clients,
    }
    return render(request, 'super/index/advertising/list.html', context)


@staff_member_required(login_url='/admin/login')
def advertising_create(request):
    context = {
        'module': 'homepage',
    }

    if request.method == 'POST':
        error = {}
        name = request.POST.get('name', '')
        target_url = request.POST.get('target_url', '')

        flag = True
        advertising = Advertising()

        if not len(name):
            flag = False
            error['name_msg'] = FILED_CHECK_MSG
        else:
            advertising.name = name

        # 进行类型判断
        advertising.target_url = target_url

        if flag:

            if request.FILES:
                if request.FILES.get('img', None):
                    # 上传图片
                    img = request.FILES['img']
                    ts = int(time.time())
                    ext = get_extension(img.name)
                    key = 'logo_{}.{}'.format(ts, ext)
                    handle_uploaded_file(img, key)
                    upload(key, os.path.join(UPLOAD_DIR, key))
                    advertising.img = key

            advertising.save()
            # 序号
            advertising.order_no = advertising.id
            advertising.save()

            return HttpResponseRedirect(reverse('web:advertising_list'))
        else:
            context['client'] = advertising
            context['error'] = error

    return render(request, 'super/index/advertising/create.html', context)


@staff_member_required(login_url='/admin/login')
def advertising_edit(request, advertising_id):

    advertising = Advertising.objects.filter(id=advertising_id).first()
    context = {
        'client': advertising,
        'module': 'homepage',
    }

    if request.method == 'POST':
        error = {}
        name = request.POST.get('name', '')
        target_url = request.POST.get('target_url', '')

        flag = True

        if not len(name):
            flag = False
            error['name_msg'] = FILED_CHECK_MSG
        else:
            advertising.name = name

        # 进行类型判断
        advertising.target_url = target_url

        if flag:

            if request.FILES:
                if request.FILES.get('img', None):
                    # 上传图片
                    img = request.FILES['img']
                    ts = int(time.time())
                    ext = get_extension(img.name)
                    key = 'logo_{}.{}'.format(ts, ext)
                    handle_uploaded_file(img, key)
                    upload(key, os.path.join(UPLOAD_DIR, key))
                    advertising.img = key

            advertising.save()

            return HttpResponseRedirect(reverse('web:advertising_list'))
        else:
            context['error'] = error

    return render(request, 'super/index/advertising/create.html', context)


@staff_member_required(login_url='/admin/login')
def advertising_delete(request, advertising_id):
    advertising = Advertising.objects.filter(pk=advertising_id).first()
    if advertising:
        advertising.delete()
    return HttpResponseRedirect(reverse('web:advertising_list'))


@staff_member_required(login_url='/admin/login')
def advertising_up(request, advertising_id):
    advertising = Advertising.objects.filter(pk=advertising_id).first()
    if advertising:
        before_advertisings = Advertising.objects.filter(
            Q(order_no__lt=advertising.order_no) & ~Q(is_del=True)
        ).order_by('-order_no')
        if before_advertisings:
            # 旧
            before_advertising = before_advertisings[0]
            old_order_no = advertising.order_no
            advertising.order_no = before_advertising.order_no
            advertising.save()
            # 新
            before_advertising.order_no = old_order_no
            before_advertising.save()
    return HttpResponseRedirect(reverse('web:advertising_list'))


@staff_member_required(login_url='/admin/login')
def advertising_down(request, advertising_id):
    advertising = Advertising.objects.filter(pk=advertising_id).first()
    if advertising:
        after_advertisings = Advertising.objects.filter(
            Q(order_no__gt=advertising.order_no) & ~Q(is_del=True)
        ).order_by('order_no')

        if after_advertisings:
            # 旧
            after_advertising = after_advertisings[0]
            old_order_no = advertising.order_no
            advertising.order_no = after_advertising.order_no
            advertising.save()
            # 新
            after_advertising.order_no = old_order_no
            after_advertising.save()
    return HttpResponseRedirect(reverse('web:advertising_list'))


@csrf_exempt
def ckeditor_upload(request):
    if request.FILES:
        ts = int(time.time())
        img_file = request.FILES.get('upload', '')

        checkNum = request.GET.get('CKEditorFuncNum', '')
        ext = get_extension(request.FILES['upload'].name)
        key = 'ckeditor_{}.{}'.format(ts, ext)

        handle_uploaded_file(img_file, key)
        # 上传图片到qiniu
        upload(key, os.path.join(UPLOAD_DIR, key))
        return HttpResponse("<script type='text/javascript'>window.parent.CKEDITOR.tools.callFunction(\
            '"+checkNum+"','"+url(key)+"','')</script>")
