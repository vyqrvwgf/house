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
    Infrastructure,
    HousingResources,
    HousingPicture,
    Bedroom,
    HouseConfig,
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
        'module': 'listings'
    }
    objs = HousingResources.obs.get_queryset().filter(
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

    return render(request, 'super/housing/listings/list.html', context)


@staff_member_required(login_url='/admin/login')
def create(request):
    context = {
        'module': 'listings',
        'qq_map_api_url': QQ_MAP_API_URL
    }

    infrastructures = Infrastructure.obs.get_queryset().order_by('-order_no')
    context['infrastructures'] = infrastructures

    if request.method == 'POST':
        error = {}
        content = request.POST.get('content', '')
        lease = request.POST.get('lease', 0)
        category = request.POST.get('category', '')
        province = request.POST.get('province', '')
        city = request.POST.get('city', '')
        area = request.POST.get('area', '')
        bet = request.POST.get('bet', 0)
        month_rent = request.POST.get('month_rent', 0)
        pay = request.POST.get('pay', 0)
        direction = request.POST.get('direction', 0)
        layer = request.POST.get('layer', 0)
        total_layer = request.POST.get('total_layer', 0)
        community = request.POST.get('community', '')
        address = request.POST.get('address', '')
        bus = request.POST.get('bus', '')
        subway = request.POST.get('subway', '')
        buy = request.POST.get('buy', '')
        sitting_room = request.POST.get('sitting_room', 0)
        sitting_room_area = request.POST.get('sitting_room_area', 0)
        sitting_room_complete = request.POST.getlist(
            'sitting_room_complete', [])
        infrastructure_id = request.POST.getlist('infrastructure_id', [])
        lng = request.POST.get('lng', 0)
        lat = request.POST.get('lat', 0)

        flag = True
        housing_resources = HousingResources()

        if not len(content):
            flag = False
            error['content_msg'] = FILED_CHECK_MSG
        else:
            housing_resources.content = content

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
                    housing_resources.cover = key

                if request.FILES.get('house_pcover', None):
                    # 上传图片
                    img = request.FILES['house_pcover']
                    ts = int(time.time())
                    ext = get_extension(img.name)
                    key = 'house_pcover_{}.{}'.format(ts, ext)
                    handle_uploaded_file(img, key)
                    upload(key, os.path.join(UPLOAD_DIR, key))
                    housing_resources.house_pcover = key

            # 获取基础设施
            infrastructure_id = [int(i) for i in infrastructure_id]
            if infrastructure_id:
                infrastructures = Infrastructure.objects.filter(
                    pk__in=infrastructure_id)
                housing_resources.infrastructure = infrastructures

            if sitting_room_complete:
                housing_resources.sitting_room_complete = ','.join(
                    sitting_room_complete)

            housing_resources.lease = lease
            housing_resources.category = category
            housing_resources.month_rent = month_rent
            housing_resources.lat = lat
            housing_resources.lng = lng
            housing_resources.bet = bet
            housing_resources.pay = pay
            housing_resources.direction = direction
            housing_resources.sitting_room = sitting_room
            housing_resources.layer = layer
            housing_resources.total_layer = total_layer
            housing_resources.community = community
            housing_resources.bus = bus
            housing_resources.subway = subway
            housing_resources.buy = buy
            housing_resources.province = province
            housing_resources.city = city
            housing_resources.area = area
            housing_resources.address = address
            housing_resources.sitting_room_area = sitting_room_area
            housing_resources.status = 2
            housing_resources.audit_status = 2
            housing_resources.save()
            return HttpResponseRedirect(reverse('web:listings_list'))
        else:
            context['client'] = housing_resources
            context['error'] = error

    return render(request, 'super/housing/listings/create.html', context)


@staff_member_required(login_url='/admin/login')
def edit(request, housingresources_id):
    housing_resources = HousingResources.objects.filter(
        id=housingresources_id).first()
    context = {
        'client': housing_resources,
        'module': 'listings',
        'qq_map_api_url': QQ_MAP_API_URL
    }

    infrastructures = Infrastructure.obs.get_queryset().order_by('-order_no')
    context['infrastructures'] = infrastructures

    if request.method == 'POST':
        error = {}
        content = request.POST.get('content', '')
        lease = request.POST.get('lease', 0)
        category = request.POST.get('category', '')
        province = request.POST.get('province', '')
        city = request.POST.get('city', '')
        area = request.POST.get('area', '')
        bet = request.POST.get('bet', 0)
        month_rent = request.POST.get('month_rent', 0)
        pay = request.POST.get('pay', 0)
        direction = request.POST.get('direction', 0)
        layer = request.POST.get('layer', 0)
        total_layer = request.POST.get('total_layer', 0)
        community = request.POST.get('community', '')
        address = request.POST.get('address', '')
        bus = request.POST.get('bus', '')
        subway = request.POST.get('subway', '')
        buy = request.POST.get('buy', '')
        sitting_room = request.POST.get('sitting_room', 0)
        sitting_room_area = request.POST.get('sitting_room_area', 0)
        sitting_room_complete = request.POST.getlist(
            'sitting_room_complete', [])
        infrastructure_id = request.POST.getlist('infrastructure_id', [])
        lng = request.POST.get('lng', 0)
        lat = request.POST.get('lat', 0)

        flag = True

        if not len(content):
            flag = False
            error['content_msg'] = FILED_CHECK_MSG
        else:
            housing_resources.content = content

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
                    housing_resources.cover = key

                if request.FILES.get('house_pcover', None):
                    # 上传图片
                    img = request.FILES['house_pcover']
                    ts = int(time.time())
                    ext = get_extension(img.name)
                    key = 'house_pcover_{}.{}'.format(ts, ext)
                    handle_uploaded_file(img, key)
                    upload(key, os.path.join(UPLOAD_DIR, key))
                    housing_resources.house_pcover = key

            # 获取基础设施
            housing_resources.infrastructure = []
            infrastructure_id = [int(i) for i in infrastructure_id]
            if infrastructure_id:
                infrastructures = Infrastructure.objects.filter(
                    pk__in=infrastructure_id)
                housing_resources.infrastructure = infrastructures

            housing_resources.sitting_room_complete = ','.join(
                sitting_room_complete)

            housing_resources.lease = lease
            housing_resources.category = category
            housing_resources.month_rent = month_rent
            housing_resources.lat = lat
            housing_resources.lng = lng
            housing_resources.bet = bet
            housing_resources.pay = pay
            housing_resources.direction = direction
            housing_resources.sitting_room = sitting_room
            housing_resources.layer = layer
            housing_resources.total_layer = total_layer
            housing_resources.community = community
            housing_resources.bus = bus
            housing_resources.subway = subway
            housing_resources.buy = buy
            housing_resources.province = province
            housing_resources.city = city
            housing_resources.area = area
            housing_resources.address = address
            housing_resources.sitting_room_area = sitting_room_area
            housing_resources.save()
            return HttpResponseRedirect(reverse('web:listings_list'))
        else:
            context['client'] = housing_resources
            context['error'] = error

    return render(request, 'super/housing/listings/create.html', context)


@staff_member_required(login_url='/admin/login')
def offline(request, housingresources_id):
    page = request.GET.get('page', '')

    client = HousingResources.objects.filter(pk=housingresources_id).first()
    if client:
        client.status = 1
        client.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@staff_member_required(login_url='/admin/login')
def online(request, housingresources_id):
    page = request.GET.get('page', '')
    client = HousingResources.objects.filter(pk=housingresources_id).first()
    if client:
        client.status = 2
        client.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@staff_member_required(login_url='/admin/login')
def delete(request, housingresources_id):
    page = request.GET.get('page', '')
    client = HousingResources.objects.filter(pk=housingresources_id).first()
    if client:
        client.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@staff_member_required(login_url='/admin/login')
def bedroom_list(request, housingresources_id):
    context = {
        'module': 'listings',
        'housingresources_id': housingresources_id,
    }

    objs = Bedroom.objects.filter(
        housing_resources__pk=housingresources_id).order_by('-created')

    page = request.GET.get('page', 1)
    clients = paging_objs(
        object_list=objs,
        per_page=BACK_PAGE_COUNT,
        page=page)

    context['clients'] = clients

    return render(request, 'super/housing/listings/bedroom/list.html', context)


@staff_member_required(login_url='/admin/login')
def bedroom_create(request, housingresources_id):
    context = {
        'module': 'listings'
    }

    housing_resources = HousingResources.objects.get(pk=housingresources_id)
    context['housing_resources'] = housing_resources
    house_configs = HouseConfig.obs.get_queryset()
    context['house_configs'] = house_configs

    if request.method == 'POST':
        error = {}
        intro = request.POST.get('intro', '')
        area = request.POST.get('area', 0)
        status = request.POST.get('status', 0)
        house_config = request.POST.getlist('house_config', [])

        bedroom = Bedroom()

        if request.FILES:
            if request.FILES.get('cover', None):
                # 上传图片
                img = request.FILES['cover']
                ts = int(time.time())
                ext = get_extension(img.name)
                key = 'cover_{}.{}'.format(ts, ext)
                handle_uploaded_file(img, key)
                upload(key, os.path.join(UPLOAD_DIR, key))
                bedroom.cover = key

        bedroom.housing_resources = housing_resources
        bedroom.intro = intro
        bedroom.area = area
        bedroom.status = status
        bedroom.save()

        house_config = [int(h) for h in house_config]
        for h in house_config:
            house_config = HouseConfig.objects.get(pk=h)
            bedroom.house_config.add(house_config)

        bedroom.save()

        return HttpResponseRedirect(
            reverse(
                'web:listings_bedroom_list', kwargs={
                    'housingresources_id': housingresources_id}))

    return render(request, 'super/housing/listings/bedroom/create.html', context)


@staff_member_required(login_url='/admin/login')
def bedroom_edit(request, bedroom_id):
    bedroom = Bedroom.objects.get(pk=bedroom_id)
    context = {
        'client': bedroom,
        'module': 'listings',
    }

    house_configs = HouseConfig.obs.get_queryset()
    context['house_configs'] = house_configs

    if request.method == 'POST':
        error = {}

        error = {}
        intro = request.POST.get('intro', '')
        area = request.POST.get('area', 0)
        status = request.POST.get('status', 0)
        house_config = request.POST.getlist('house_config', [])

        if request.FILES:
            if request.FILES.get('cover', None):
                # 上传图片
                img = request.FILES['cover']
                ts = int(time.time())
                ext = get_extension(img.name)
                key = 'cover_{}.{}'.format(ts, ext)
                handle_uploaded_file(img, key)
                upload(key, os.path.join(UPLOAD_DIR, key))
                bedroom.cover = key

        bedroom.intro = intro
        bedroom.area = area
        bedroom.status = status
        bedroom.save()

        bedroom.house_config = []
        house_config = [int(h) for h in house_config]
        for h in house_config:
            house_config = HouseConfig.objects.get(pk=h)
            bedroom.house_config.add(house_config)

        bedroom.save()

        return HttpResponseRedirect(
            reverse(
                'web:listings_bedroom_list', kwargs={
                    'housingresources_id': bedroom.housing_resources.id}))

    return render(request, 'super/housing/listings/bedroom/create.html', context)


@staff_member_required(login_url='/admin/login')
def bedroom_delete(request, bedroom_id):
    page = request.GET.get('page', '')
    client = Bedroom.objects.filter(pk=bedroom_id).first()
    if client:
        client.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@staff_member_required(login_url='/admin/login')
def bedroom_offline(request, bedroom_id):
    page = request.GET.get('page', '')

    client = Bedroom.objects.filter(pk=bedroom_id).first()
    if client:
        client.is_valid = False
        client.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@staff_member_required(login_url='/admin/login')
def bedroom_online(request, bedroom_id):
    page = request.GET.get('page', '')
    client = Bedroom.objects.filter(pk=bedroom_id).first()
    if client:
        client.is_valid = True
        client.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@staff_member_required(login_url='/admin/login')
def picture_list(request, housingresources_id):
    context = {
        'module': 'listings',
        'housingresources_id': housingresources_id,
    }
    objs = HousingPicture.obs.get_queryset().filter(
        housing_resources__pk=housingresources_id).order_by('-order_no')

    page = request.GET.get('page', 1)
    clients = paging_objs(
        object_list=objs,
        per_page=BACK_PAGE_COUNT,
        page=page)

    context['clients'] = clients

    return render(request, 'super/housing/listings/img/list.html', context)


@staff_member_required(login_url='/admin/login')
def picture_create(request, housingresources_id):
    context = {
        'module': 'listings'
    }

    housing_resources = HousingResources.objects.get(pk=housingresources_id)
    context['housing_resources'] = housing_resources

    if request.method == 'POST':
        error = {}

        housing_picture = HousingPicture()

        if request.FILES:
            if request.FILES.get('picture', None):
                # 上传图片
                img = request.FILES['picture']
                ts = int(time.time())
                ext = get_extension(img.name)
                key = 'picture_{}.{}'.format(ts, ext)
                handle_uploaded_file(img, key)
                upload(key, os.path.join(UPLOAD_DIR, key))
                housing_picture.picture = key

        housing_picture.housing_resources = housing_resources
        housing_picture.save()
        housing_picture.order_no = housing_picture.id
        housing_picture.save()
        return HttpResponseRedirect(
            reverse(
                'web:listings_picture_list', kwargs={
                    'housingresources_id': housingresources_id}))

    return render(request, 'super/housing/listings/img/create.html', context)


@staff_member_required(login_url='/admin/login')
def picture_edit(request, housingpicture_id):
    housing_picture = HousingPicture.objects.get(pk=housingpicture_id)
    context = {
        'client': housing_picture,
        'module': 'listings',
    }

    if request.method == 'POST':
        error = {}

        if request.FILES:
            if request.FILES.get('picture', None):
                # 上传图片
                img = request.FILES['picture']
                ts = int(time.time())
                ext = get_extension(img.name)
                key = 'picture_{}.{}'.format(ts, ext)
                handle_uploaded_file(img, key)
                upload(key, os.path.join(UPLOAD_DIR, key))
                housing_picture.picture = key

        housing_picture.save()
        return HttpResponseRedirect(
            reverse(
                'web:listings_picture_list', kwargs={
                    'housingresources_id': housing_picture.housing_resources.id}))

    return render(request, 'super/housing/listings/img/create.html', context)


@staff_member_required(login_url='/admin/login')
def picture_delete(request, housingpicture_id):
    page = request.GET.get('page', '')
    client = HousingPicture.objects.filter(pk=housingpicture_id).first()
    if client:
        client.delete()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@staff_member_required(login_url='/admin/login')
def picture_up(request, housingpicture_id):
    page = request.GET.get('page', '')

    housing_picture = HousingPicture.objects.filter(
        pk=housingpicture_id).first()
    if housing_picture:
        before_housing_pictures = HousingPicture.obs.get_queryset().filter(
            order_no__gt=housing_picture.order_no,
        ).order_by('order_no')

        if before_housing_pictures:
            # 旧
            before_housing_picture = before_housing_pictures[0]
            old_order_no = housing_picture.order_no
            housing_picture.order_no = before_housing_picture.order_no
            housing_picture.save()
            # 新
            before_housing_picture.order_no = old_order_no
            before_housing_picture.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))


@staff_member_required(login_url='/admin/login')
def picture_down(request, housingpicture_id):
    page = request.GET.get('page', '')
    housing_picture = HousingPicture.objects.filter(
        pk=housingpicture_id).first()

    if housing_picture:
        after_housing_pictures = HousingPicture.obs.get_queryset().filter(
            order_no__lt=housing_picture.order_no
        ).order_by('-order_no')

        if after_housing_pictures:
            # 旧
            after_housing_picture = after_housing_pictures[0]
            old_order_no = housing_picture.order_no
            housing_picture.order_no = after_housing_picture.order_no
            housing_picture.save()
            # 新
            after_housing_picture.order_no = old_order_no
            after_housing_picture.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
