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
    Column
)
from imagestore.qiniu_manager import(
    get_extension,
    handle_uploaded_file,
    upload,
    url,
)
from settings import (
    BACK_PAGE_COUNT, FILED_CHECK_MSG,
    UPLOAD_DIR, COLUMN_NOT_LIST,
    COLUMN_IS_ADD, COLUMN_IS_EDIT,
)
import os
import datetime
import time


@staff_member_required(login_url='/admin/login')
def list(request):

    columns = Column.objects.filter(is_del=False).order_by('order_no')

    paginator = Paginator(columns, BACK_PAGE_COUNT)
    page = request.GET.get('page', '')

    try:
        columns = paginator.page(page)
    except PageNotAnInteger:
        columns = paginator.page(1)
    except EmptyPage:
        columns = paginator.page(paginator.num_pages)

    context = {
        'module': 'column',
        'columns': columns,
        'flag': COLUMN_IS_ADD,
        'edit_flag': COLUMN_IS_EDIT,
    }

    return render(request, 'super/column/list.html', context)


@staff_member_required(login_url='/admin/login')
def create(request):
    columns = Column.objects.filter(
        is_del=False
    )

    context = {
        'module': 'column',
        'columns': columns,
        'flag': COLUMN_IS_ADD,
        'edit_flag': COLUMN_IS_EDIT,
    }

    if request.method == 'POST':
        error = {}
        name = request.POST.get('name', '')
        parent = int(request.POST.get('parent', 0))
        slug = request.POST.get('slug', '')

        flag = True
        column = Column()

        if not len(name):
            flag = False
            error['name_msg'] = FILED_CHECK_MSG
        else:
            column.name = name

        if not len(slug):
            flag = False
            error['slug_msg'] = FILED_CHECK_MSG
        else:
            column.slug = slug

        if flag:
            column.save()
            column.order_no = column.id
            column.save()
            return HttpResponseRedirect(reverse('web:column_list'))
        else:
            context['client'] = column
            context['error'] = error

    return render(request, 'super/column/create.html', context)


@staff_member_required(login_url='/admin/login')
def edit(request, column_id):
    columns = Column.objects.filter(
        is_del=False
    )

    column = Column.objects.filter(id=column_id).first()
    context = {
        'column': column,
        'module': 'column',
        'columns': columns,
        'flag': COLUMN_IS_ADD,
        'edit_flag': COLUMN_IS_EDIT,
    }

    if request.method == 'POST':
        error = {}
        name = request.POST.get('name', '')
        parent = int(request.POST.get('parent', 0))
        slug = request.POST.get('slug', '')

        flag = True

        if not len(name):
            flag = False
            error['name_msg'] = FILED_CHECK_MSG
        else:
            column.name = name

        if not len(slug):
            flag = False
            error['slug_msg'] = FILED_CHECK_MSG
        else:
            column.slug = slug

        if flag:
            column.save()
            return HttpResponseRedirect(reverse('web:column_list'))
        else:
            context['error'] = error

    return render(request, 'super/column/create.html', context)


@staff_member_required(login_url='/admin/login')
def delete(request, column_id):
    column = Column.objects.filter(pk=column_id).first()
    if column:
        column.delete()
    return HttpResponseRedirect(reverse('web:column_list'))


@staff_member_required(login_url='/admin/login')
def up(request, column_id):
    column = Column.objects.filter(pk=column_id).first()
    if column:
        before_columns = Column.objects.filter(
            order_no__lt=column.order_no,
            is_del=False,
        ).order_by('-order_no')
        if before_columns:
            # 旧
            before_column = before_columns[0]
            old_order_no = column.order_no
            column.order_no = before_column.order_no
            column.save()
            # 新
            before_column.order_no = old_order_no
            before_column.save()
    return HttpResponseRedirect(reverse('web:column_list'))


@staff_member_required(login_url='/admin/login')
def down(request, column_id):
    column = Column.objects.filter(pk=column_id).first()
    if column:
        after_columns = Column.objects.filter(
            order_no__gt=column.order_no,
            is_del=False,
        ).order_by('order_no')

        if after_columns:
            # 旧
            after_column = after_columns[0]
            old_order_no = column.order_no
            column.order_no = after_column.order_no
            column.save()
            # 新
            after_column.order_no = old_order_no
            after_column.save()
    return HttpResponseRedirect(reverse('web:column_list'))
