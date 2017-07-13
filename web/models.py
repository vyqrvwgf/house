# coding: utf-8

from __future__ import unicode_literals

from django.db import models
from django.db.models import Count, Sum
from django.contrib.auth.models import User
from django.db.models import Q

from imagestore.qiniu_manager import url

import datetime


class BaseModelManager(models.Manager):
    def get_queryset(self):
        return super(BaseModelManager, self).get_queryset().filter(is_del=False)

class BaseModel(models.Model):

    class Meta:
        abstract = True

    is_del = models.BooleanField(default=False, verbose_name='是否删除')
    is_valid = models.BooleanField(default=True, verbose_name='是否可用')
    updated = models.DateTimeField(auto_now=True, blank=True, null=True, verbose_name='更新时间')
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True, verbose_name='创建时间')

    objects = models.Manager()  # The default manager.
    obs = BaseModelManager()  # A manager which will ignore the is_del objects.

    def delete(self, *args, **kwargs):
        self.is_del = True
        self.save()

    def kill(self, *args, **kwargs):
        """
        彻底删除对象
        """
        super(BaseModel, self).delete()

    def activate(self, *args, **kwargs):
        """
        更改状态为有效
        """
        self.is_valid = True
        self.save()

    def deactivate(self, *args, **kwargs):
        """
        更改状态为无效
        """
        self.is_valid = False
        self.save()


class Profile(BaseModel):

    class Meta(object):
        verbose_name = "用户信息"
        verbose_name_plural = "用户信息"

    USER_LOGIN_CHOICES = (
        (1, '手机用户'),
        (2, '微信用户'),
        (3, '微博用户'),
        (4, 'qq'),
    )

    GENDER_CHOICES = (
        (1, '男'),
        (2, '女')
    )

    user = models.ForeignKey(User, default=None, blank=True, null=True, verbose_name='用户')
    email = models.CharField(max_length=128, default='', blank=True, verbose_name='邮箱')
    user_name = models.CharField(max_length=128, default='', verbose_name='姓名')
    nickname = models.CharField(max_length=128, default='', verbose_name='昵称')
    password = models.CharField(max_length=255, default='', blank=True, verbose_name='密码')
    jwt_token = models.TextField(default='', null=True, blank=True, verbose_name='jwt_token')
    background = models.CharField(max_length=255, default='', blank=True, verbose_name='背景')
    openid = models.CharField(max_length=255, default='', verbose_name='openid')
    user_login_type = models.IntegerField(choices=USER_LOGIN_CHOICES, default=1, verbose_name="用户注册类型")
    gender = models.IntegerField(choices=GENDER_CHOICES, default=1, verbose_name='性别')
    age = models.IntegerField(default=0, verbose_name='年龄')
    bank_card = models.IntegerField(default=0, verbose_name='银行卡')
    id_card = models.CharField(max_length=128, default='', blank=True, verbose_name='身份证信息')
    id_card_picture = models.CharField(max_length=255, default='', blank=True, verbose_name='身份证')
    mobile = models.CharField(max_length=16, default='', blank=True, verbose_name='手机')
    avatar = models.CharField(max_length=300, default='', null=True, blank=True, verbose_name='头像')
    wx_unionid = models.CharField(max_length=300, default='', blank=True, verbose_name="微信id")
    weibo_uid = models.CharField(max_length=300, default='', blank=True, verbose_name="微博id")
    qq_uid = models.CharField(max_length=300, default='', blank=True, verbose_name="qqid")

    def get_user(self):
        try:
            if not self.user:
                username = self.mobile if self.mobile else self.email
                self.user = User.objects.create_user(
                    username,
                    self.email,
                    self.password
                )
                self.save()
        except Exception, e:
            print e

        return self.user

    def avatar_url(self):
        if not self.avatar:
            avatar_url = ''
        elif 'http' in self.avatar:
            avatar_url = self.avatar
        else:
            avatar_url = url(self.avatar)
        return avatar_url

    def id_card_picture_url(self):
        card_picture_url = url(self.id_card_picture)
        return card_picture_url

    def __unicode__(self):
        return self.nickname


class AdminLog(BaseModel):

    class Meta(object):
        verbose_name = "管理员登录记录"
        verbose_name_plural = "管理员登录记录"

    name = models.CharField(max_length=128, default='', verbose_name='管理员名称')
    ip = models.CharField(max_length=128, default='', verbose_name='管理员IP')
    admin_id = models.IntegerField(default=0, blank=True, null=True, verbose_name="管理员ID")

    def __unicode__(self):
        return self.name


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


class Words(BaseModel):

    class Meta(object):
        verbose_name = "敏感词"
        verbose_name_plural = "敏感词"

    content = models.TextField(default='', blank=True, verbose_name='内容')

    def __unicode__(self):
        return self.content


class JointVenture(BaseModel):

    class Meta(object):
        verbose_name = "合作企业"
        verbose_name_plural = "合作企业"

    name = models.CharField(default='', max_length=128, verbose_name="名称")
    mobile = models.CharField(default='', max_length=128, verbose_name="电话")
    address = models.CharField(default='', max_length=300, verbose_name="地址")
    cover = models.CharField(max_length=128, default='', verbose_name="头像")
    intro = models.TextField(default='', verbose_name="简介")
    balance = models.FloatField(default=0, null=True, verbose_name="余额")

    def __unicode__(self):
        return self.name

    def cover_url(self):
        return url(self.cover)


class Permissions(BaseModel):

    class Meta(object):
        verbose_name = "权限组"
        verbose_name_plural = "权限组"

    name = models.CharField(max_length=128, verbose_name="名称")
    menu_str = models.TextField(blank=True, default='', verbose_name="菜单id")
    menu_name_str = models.TextField(blank=True, default='', verbose_name="菜单名称")

    def __unicode__(self):
        return self.name


class JointVentureAccount(BaseModel):

    class Meta(object):
        verbose_name = "合作企业/管理员账号"
        verbose_name_plural = "合作企业/管理员账号"

    user = models.OneToOneField(User, default=None, null=True, blank=True, unique=True, verbose_name='用户')
    joint_venture = models.ForeignKey(JointVenture, blank=True, null=True, verbose_name="合作企业")
    permissions = models.ForeignKey(Permissions, blank=True, null=True, verbose_name="所属权限组")


class Setting(BaseModel):

    class Meta(object):
        verbose_name = '配置'
        verbose_name_plural = '配置'

    name = models.CharField(max_length=100, default='', verbose_name="字段")
    value = models.CharField(max_length=100, default='', verbose_name="值")
    detail = models.CharField(max_length=100, default='', verbose_name="描述")


class Withdrawal(BaseModel):

    class Meta(object):
        verbose_name = "提现"
        verbose_name_plural = "提现"

    STATUS_CHOICES = (
        (0, '未处理'),
        (1, '通过'),
        (2, '不通过')
    )

    join_tventure = models.ForeignKey(JointVenture, null=True, blank=True, verbose_name="合作企业")
    money = models.FloatField(default=0, null=True, verbose_name="金额")
    reason = models.CharField(default='', max_length=300, verbose_name="理由")
    status = models.IntegerField(choices=STATUS_CHOICES, default=0, verbose_name="状态")



