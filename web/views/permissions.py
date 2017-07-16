# coding: utf-8

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from imagestore.qiniu_manager import upload, url
from web.models import (
    Permissions
)
from django.contrib.auth.models import User
from settings import BACK_PAGE_COUNT, UPLOAD_DIR, QINIU_DOMAIN, BUCKET_NAME
from common.lookup import MENU_LIST as menu_list

import os, datetime
import simplejson as json
import urllib


@staff_member_required
def permissions_list(request):
    page = request.GET.get('page', 0)
    clients = Permissions.objects.filter(is_del=0).order_by('-created')

    paginator = Paginator(clients, BACK_PAGE_COUNT)
    try:
        clients = paginator.page(page)
    except PageNotAnInteger:
        clients = paginator.page(1)
    except EmptyPage:
        clients = paginator.page(paginator.num_pages)

    context = {
        'module': 'permissions',
        'clients': clients,
        'page': page
    }
    return render(request, 'super/settings/permissions/index.html', context)


@staff_member_required
def permissions_delete(request, permissions_id):
    page = request.GET.get('page', '')
    permissions = Permissions.objects.filter(pk=permissions_id).first()
    if permissions:
        permissions.delete()
    return HttpResponseRedirect(reverse('web:permissions_list')
        + '?page' + page
    )


@staff_member_required
def permissions_create(request):

    menu1 = []
    menu2 = []
    for m in menu_list:
        if m.get('parent_module', ''):
            menu2.append(m)
        else:
            menu1.append(m)

    context = {
        'module': 'permissions',
        'menu1': menu1,
        'menu2': menu2,
    }
    if request.method == 'POST':
        name = request.POST.get('name', '')
        menu_str = request.POST.get('menu_str', '')
        menu_name_str = ''
        menu_s = menu_str.split(',')
        for x in menu_list:
            if x['module'] in menu_s:
                menu_name_str += x['name'] + ','

        permissions = Permissions()
        permissions.name = name
        permissions.menu_str = menu_str.rstrip(',')
        permissions.menu_name_str = menu_name_str.rstrip(',')
        permissions.save()
        return HttpResponseRedirect(reverse('web:permissions_list'))

    return render(request, 'super/settings/permissions/create.html', context)


@staff_member_required
def permissions_edit(request, permissions_id):
    page = request.GET.get('page', '')
    client = Permissions.objects.filter(pk=permissions_id).first()
    if request.method == 'POST':
        name = request.POST.get('name', '')
        menu_str = request.POST.get('menu_str', '')
        menu_name_str = ''
        menu_s = menu_str.split(',')
        for x in menu_list:
            if x['module'] in menu_s:
                menu_name_str += x['name'] + ','

        client.name = name
        client.menu_str = menu_str.rstrip(',')
        client.menu_name_str = menu_name_str.rstrip(',')
        client.save()
        return HttpResponseRedirect(reverse('web:permissions_list')
            + '?page=' + page
        )

    menu1 = []
    menu2 = []
    for m in menu_list:
        if m.get('parent_module', ''):
            menu2.append(m)
        else:
            menu1.append(m)

    context = {
        'module': 'permissions',
        'menu1': menu1,
        'menu2': menu2,
        'client': client,
        'page': page,
    }

    return render(request, 'super/settings/permissions/create.html', context)


