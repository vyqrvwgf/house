# coding: utf-8

from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from imagestore.qiniu_manager import upload, url
from web.models import (
    JointVenture,
    Permissions,
    JointVentureAccount,
)
from settings import BACK_PAGE_COUNT, DOMAIN


@staff_member_required
def venture_manage_list(request):
    page = request.GET.get('page', 0)
    clients = JointVentureAccount.objects.filter(joint_venture__isnull=False).order_by('-created')

    paginator = Paginator(clients, BACK_PAGE_COUNT)
    try:
        clients = paginator.page(page)
    except PageNotAnInteger:
        clients = paginator.page(1)
    except EmptyPage:
        clients = paginator.page(paginator.num_pages)

    context = {
        'module': 'joint_venture_account',
        'clients': clients,
        'page': page,
    }

    return render(request, 'super/settings/venture_manage/index.html', context)


@staff_member_required
def venture_manage_delete(request, account_id):
    page = request.GET.get('page', '')
    client = JointVentureAccount.objects.filter(pk=account_id).first()
    if client:
        client.delete()
    return HttpResponseRedirect(reverse('web:venture_manage_list')
        + '?page=' + page
    )


@staff_member_required
def venture_manage_create(request):

    permissionss = Permissions.objects.filter(is_del=False)
    joint_ventures = JointVenture.objects.filter(is_del=False)
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        joint_venture_id = request.POST.get('joint_venture_id', 0)
        permissions = request.POST.get('permissions', 0)
        joint_venture_account = JointVentureAccount()

        if joint_venture_id:
            joint_venture = JointVenture.objects.filter(pk=int(joint_venture_id)).first()
            joint_venture_account.joint_venture = joint_venture

        user = User()
        user.username = username
        user.is_staff = True
        user.set_password(password)
        user.groups = list(group_list)
        user.save()
        joint_venture_account.user = user

        if permissions:
            ps = Permissions.objects.filter(pk=permissions).first()
            joint_venture_account.permissions = ps
        joint_venture_account.save()

        return HttpResponseRedirect(reverse('web:venture_manage_list'))

    groups = Group.objects.all()
    context = {
        'module': 'joint_venture_account',
        'permissionss': permissionss,
        'joint_ventures': joint_ventures,
        'DOMAIN': DOMAIN,
        'groups': groups,
    }

    return render(request, 'super/settings/venture_manage/create.html', context)


@staff_member_required
def venture_manage_edit(request, account_id):
    page = request.GET.get('page', '')
    client = JointVentureAccount.objects.filter(pk=account_id).first()
    permissionss = Permissions.objects.filter(is_del=False)
    joint_ventures = JointVenture.objects.filter(is_del=False)
    if request.method == "POST":
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        joint_venture_id = request.POST.get('joint_venture_id', 0)
        permissions = request.POST.get('permissions', 0)
        group_id_list = request.POST.getlist('group_id', '')
        group_list = Group.objects.filter(id__in=group_id_list)

        if joint_venture_id:
            joint_venture = JointVenture.objects.filter(pk=int(joint_venture_id)).first()
            client.joint_venture = joint_venture
        else:
            client.joint_venture = None

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

        return HttpResponseRedirect(reverse('web:venture_manage_list')
            + '?page=' + page
        )

    groups = Group.objects.all()

    context = {
        'module': 'joint_venture_account',
        'client': client,
        'permissionss': permissionss,
        'joint_ventures': joint_ventures,
        'DOMAIN': DOMAIN,
        'page': page,
        'groups': groups,
    }
    return render(request, 'super/settings/venture_manage/create.html', context)


