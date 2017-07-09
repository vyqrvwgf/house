# coding: utf-8

from __future__ import unicode_literals

from django.db import models
from django.db.models import Q

from imagestore.qiniu_manager import url

import datetime


class BaseModel(models.Model):

    class Meta:
        abstract = True

    is_del = models.BooleanField(default=False, verbose_name='是否删除')
    updated = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='更新时间')
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='创建时间')

    def delete(self, *args, **kwargs):
        self.is_del = True
        self.save()

class Advertising(BaseModel):

    class Meta(object):
        verbose_name = "轮播图"
        verbose_name_plural = "轮播图"

    name = models.CharField(max_length=128, verbose_name="名称")
    order_no = models.IntegerField(default=0, verbose_name="排序号")
    img = models.CharField(max_length=1024, default='', blank=True, verbose_name="图片")
    target_url = models.CharField(max_length=300, verbose_name="链接地址")
    intro = models.TextField(default='', blank=True, verbose_name="简介")

    def img_url(self):
        return url(self.img)

class Column(BaseModel):

    class Meta(object):
        verbose_name = '栏目'
        verbose_name_plural = '栏目'

    name = models.CharField(max_length=128, verbose_name='名称')
    order_no = models.IntegerField(default=0, verbose_name='排序号')
    slug = models.CharField(max_length=128, default='', verbose_name='slug')
    cover = models.CharField(max_length=1024, default='', blank=True, verbose_name="图片")

    def cover_url(self):
        return url(self.cover)


class FeedBack(BaseModel):

    class Meta(object):
        verbose_name = '意见反馈'
        verbose_name_plural = '意见反馈'

    name = models.CharField(max_length=128, verbose_name="姓名")
    phone = models.CharField(max_length=128, verbose_name="联系方式")
    content = models.TextField(default='', verbose_name="反馈内容")

