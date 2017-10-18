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
        audit_status=0
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
        'module': 'listings_release',
        'clients': clients,
    }

    return render(request, 'super/release/listings/list.html', context)


@staff_member_required(login_url='/admin/login')
def offline(request, housingresources_id):
    page = request.GET.get('page', '')

    client = HousingResources.objects.filter(pk=housingresources_id).first()
    if client:
        client.status = 0
        client.save()

    return HttpResponseRedirect(reverse('web:listings_list')
        + '?page='+ str(page)
    )


@staff_member_required(login_url='/admin/login')
def online(request, housingresources_id):
    page = request.GET.get('page', '')
    client = HousingResources.objects.filter(pk=housingresources_id).first()
    if client:
        client.status = 1
        client.save()

    return HttpResponseRedirect(reverse('web:listings_list')
        + '?page='+ str(page)
    )

