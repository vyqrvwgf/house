# coding: utf-8

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from imagestore.qiniu_manager import upload, url
from web.models import (
    Permissions,
    JointVentureAccount,
    JointVenture
)
from django.contrib.auth.models import User, Group
from settings import BACK_PAGE_COUNT, UPLOAD_DIR, DOMAIN

import urllib


@staff_member_required
def operating_list(request):
    page = request.GET.get('page', 0)
    clients = JointVentureAccount.objects.filter(joint_venture__isnull=True)

    paginator = Paginator(clients, BACK_PAGE_COUNT)
    try:
        clients = paginator.page(page)
    except PageNotAnInteger:
        clients = paginator.page(1)
    except EmptyPage:
        clients = paginator.page(paginator.num_pages)

    context = {
        'module': 'operating',
        'page': page,
        'clients': clients,
    }
    return render(request, 'super/settings/operating/index.html', context)


@staff_member_required
def operating_delete(request, operating_id):
    page = request.GET.get('page', '')
    joint_venture_account = JointVentureAccount.objects.filter(pk=operating_id).first()
    if joint_venture_account:
        joint_venture_account.delete()
    return HttpResponseRedirect(reverse('web:operating_list')
        + '?page=' + page
    )


@staff_member_required
def operating_create(request):

    permissionss = Permissions.objects.filter(is_del=False)
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        permissions = request.POST.get('permissions', 0)
        joint_venture_account = JointVentureAccount()
        group_id_list = request.POST.getlist('group_id', '')
        group_list = Group.objects.filter(id__in=group_id_list)

        user = User()
        user.username = username
        user.set_password(password)
        user.is_staff = True
        user.groups = list(group_list)
        user.save()
        joint_venture_account.user = user

        if permissions:
            ps = Permissions.objects.filter(pk=permissions).first()
            joint_venture_account.permissions = ps
        joint_venture_account.save()

        return HttpResponseRedirect(reverse('web:operating_list'))

    groups = Group.objects.all()
    context = {
        'module': 'operating',
        'permissionss': permissionss,
        'DOMAIN': DOMAIN,
        'groups': groups,
    }
    return render(request, 'super/settings/operating/create.html', context)


@staff_member_required
def operating_edit(request, operating_id):
    page = request.GET.get('page', '')
    client = JointVentureAccount.objects.filter(is_del=False, pk=operating_id).first()
    permissionss = Permissions.objects.all()
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        permissions = request.POST.get('permissions', 0)
        group_id_list = request.POST.getlist('group_id', '')
        group_list = Group.objects.filter(id__in=group_id_list)

        user = client.user
        user.username = username
        if password:
            user.set_password(password)
        user.groups = list(group_list)
        user.save()
        client.user = user

        if permissions:
            ps = Permissions.objects.filter(pk=permissions).first()
            client.permissions = ps
        client.save()

        return HttpResponseRedirect(reverse('web:operating_list')
            + '?page' + page
        )

    groups = Group.objects.all()
    context = {
        'module': 'operating',
        'client': client,
        'permissionss': permissionss,
        'DOMAIN': DOMAIN,
        'page': page,
        'groups': groups,
    }
    return render(request, 'super/settings/operating/create.html', context)
