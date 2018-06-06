# coding: utf-8

from __future__ import unicode_literals

from django.db import models
from django.db.models import Count, Sum
from django.contrib.auth.models import User, Permission
from django.db.models import Q

from imagestore.qiniu_manager import url, o_url

import datetime


class BaseModelManager(models.Manager):

    def get_queryset(self):
        return super(
            BaseModelManager,
            self).get_queryset().filter(
            is_del=False, is_valid=True)


class BaseModel(models.Model):

    class Meta:
        abstract = True

    is_del = models.BooleanField(default=False, verbose_name='是否删除')
    is_valid = models.BooleanField(default=True, verbose_name='是否可用')
    updated = models.DateTimeField(
        auto_now=True,
        blank=True,
        null=True,
        verbose_name='更新时间')
    created = models.DateTimeField(
        auto_now_add=True,
        blank=True,
        null=True,
        verbose_name='创建时间')

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

    CARD_CHOICES = (
        (0, '未认证'),
        (1, '已认证')
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.CharField(
        max_length=128,
        default='',
        blank=True,
        verbose_name='邮箱')
    user_name = models.CharField(max_length=128, default='', verbose_name='姓名')
    nickname = models.CharField(max_length=128, default='', verbose_name='昵称')
    password = models.CharField(
        max_length=255,
        default='',
        blank=True,
        verbose_name='密码')
    jwt_token = models.TextField(
        default='',
        null=True,
        blank=True,
        verbose_name='jwt_token')
    openid = models.CharField(
        max_length=255,
        default='',
        verbose_name='openid')
    user_login_type = models.IntegerField(
        choices=USER_LOGIN_CHOICES,
        default=1,
        verbose_name="用户注册类型")
    gender = models.IntegerField(
        choices=GENDER_CHOICES,
        default=1,
        verbose_name='性别')
    age = models.IntegerField(default=0, verbose_name='年龄')
    id_card = models.CharField(
        max_length=128,
        default='',
        blank=True,
        verbose_name='身份证信息')
    id_card_status = models.IntegerField(
        choices=CARD_CHOICES, default=1, verbose_name='身份认证信息')
    bank_acount = models.CharField(
        max_length=128,
        default='',
        blank=True,
        verbose_name='银行卡信息')
    id_card_picture = models.CharField(
        max_length=255,
        default='',
        blank=True,
        verbose_name='身份证')
    mobile = models.CharField(
        max_length=16,
        default='',
        blank=True,
        verbose_name='手机')
    avatar = models.CharField(
        max_length=300,
        default='',
        null=True,
        blank=True,
        verbose_name='头像')
    birbath = models.DateField(default=datetime.date.today, verbose_name="生日")
    wx_unionid = models.CharField(
        max_length=300,
        default='',
        blank=True,
        verbose_name="微信id")
    weibo_uid = models.CharField(
        max_length=300,
        default='',
        blank=True,
        verbose_name="微博id")
    qq_uid = models.CharField(
        max_length=300,
        default='',
        blank=True,
        verbose_name="qqid")
    promo_code = models.CharField(
        max_length=300,
        default='',
        blank=True,
        verbose_name="动态码")
    employe = models.CharField(
        max_length=300,
        default='',
        blank=True,
        verbose_name="工作单位")

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
        except Exception as e:
            print e

        return self.user

    def avatar_url(self):
        if 'http' in self.avatar:
            avatar_url = self.avatar
        else:
            avatar_url = o_url(self.avatar)
        return avatar_url

    def id_card_picture_url(self):
        card_picture_url = url(self.id_card_picture)
        return card_picture_url

    def __unicode__(self):
        return self.nickname


class ACL(BaseModel):

    class Meta(object):

        verbose_name = "访问控制列表"
        verbose_name_plural = "访问控制列表"

        permissions = (
            ('view_module', '查看'),
            ('add_module', '添加'),
            ('edit_module', '编辑'),
            ('delete_module', '删除'),
            ('active_module', '启用禁用'),
            ('move_module', '上移下移'),
        )

    module = models.CharField(max_length=255, default='', verbose_name="模块名称")
    module_cn = models.CharField(
        max_length=255,
        default='',
        verbose_name="模块中文名称")
    permission_ids = models.CharField(
        max_length=255, default='', verbose_name="权限选项")

    def __unicode__(self):
        return self.module

    def permission_options(self):
        ids = self.permission_ids.split('#')
        return Permission.objects.filter(id__in=ids)


class AdminLog(BaseModel):

    class Meta(object):
        verbose_name = "管理员登录记录"
        verbose_name_plural = "管理员登录记录"

    name = models.CharField(max_length=128, default='', verbose_name='管理员名称')
    ip = models.CharField(max_length=128, default='', verbose_name='管理员IP')
    admin_id = models.IntegerField(
        default=0,
        blank=True,
        null=True,
        verbose_name="管理员ID")

    def __unicode__(self):
        return self.name


class Advertising(BaseModel):

    class Meta(object):
        verbose_name = "轮播图"
        verbose_name_plural = "轮播图"

    name = models.CharField(max_length=128, verbose_name="名称")
    order_no = models.IntegerField(default=0, verbose_name="排序号")
    img = models.CharField(
        max_length=1024,
        default='',
        blank=True,
        verbose_name="图片")
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
    cover = models.CharField(
        max_length=1024,
        default='',
        blank=True,
        verbose_name="图片")

    def cover_url(self):
        return url(self.cover)


class Infrastructure(BaseModel):

    class Meta(object):
        verbose_name = '基础设施'
        verbose_name_plural = '基础设施'

    name = models.CharField(max_length=128, verbose_name='名称')
    order_no = models.IntegerField(default=0, verbose_name='排序号')
    cover = models.CharField(
        max_length=1024,
        default='',
        blank=True,
        verbose_name="图片")

    @property
    def cover_url(self):
        return url(self.cover)


class RentHouse(BaseModel):

    class Meta(object):
        verbose_name = '求租发布'
        verbose_name_plural = '求租发布'

    RENT_CHOICES = (
        (0, '0-500'),
        (1, '500-1000'),
        (2, '1000-1500'),
        (3, '1500-2000'),
        (4, '2000-2500'),
        (5, '2500-3000'),
        (6, '3000-3500'),
        (7, '3500-4000'),
        (8, '4000以上'),
        (9, '不限')
    )

    LEASE_CHOICES = (
        (0, '合租'),
        (1, '整租')
    )

    MALE_CHOICES = (
        (0, '1'),
        (1, '2'),
        (2, '3'),
        (3, '4')
    )

    FEMALE_CHOICES = (
        (0, '1'),
        (1, '2'),
        (2, '3'),
        (3, '4')
    )

    TOTAL_CHOICES = (
        (0, '1'),
        (1, '2'),
        (2, '3'),
        (3, '4'),
        (4, '5'),
        (5, '6')
    )

    ACCEPT_CHOICES = (
        (0, '白领'),
        (1, '学生'),
        (2, '不限')
    )

    RELATION_CHOICES = (
        (0, '朋友'),
        (1, '情侣'),
        (2, '同学'),
        (3, '亲戚'),
        (4, '陌生人'),
        (5, '其他')
    )

    STATUS_CHOICES = (
        (0, ''),
        (1, '下线'),
        (2, '上线'),
    )

    AUDIT_STATUS_CHOICES = (
        (0, '待审核'),
        (1, '审核不通过'),
        (2, '审核通过'),
    )

    user = models.ForeignKey(
        User,
        default=None,
        null=True,
        blank=True,
        verbose_name='用户')
    rent = models.IntegerField(
        choices=RENT_CHOICES,
        default=0,
        verbose_name='租金')
    description = models.CharField(
        max_length=1024,
        blank=True,
        default='',
        verbose_name='补充说明')
    province = models.CharField(
        max_length=32,
        default='',
        blank=True,
        null=True,
        verbose_name='省')
    city = models.CharField(
        max_length=32,
        default='',
        blank=True,
        null=True,
        verbose_name='市')
    area = models.CharField(
        max_length=32,
        default='',
        blank=True,
        null=True,
        verbose_name='区')
    date = models.CharField(
        max_length=32,
        default='',
        blank=True,
        null=True,
        verbose_name='最迟入住日期')
    infrastructure = models.ManyToManyField(
        Infrastructure, verbose_name="基础设施")
    lease = models.IntegerField(
        choices=LEASE_CHOICES,
        default=0,
        verbose_name='租赁方式')
    male_count = models.IntegerField(
        choices=MALE_CHOICES,
        default=0,
        null=True,
        blank=True,
        verbose_name='男性人数')
    female_count = models.IntegerField(
        choices=FEMALE_CHOICES,
        default=0,
        null=True,
        blank=True,
        verbose_name='女性人数')
    relationship = models.IntegerField(
        choices=RELATION_CHOICES,
        default=0,
        null=True,
        blank=True,
        verbose_name='关系')
    total_count = models.IntegerField(
        choices=TOTAL_CHOICES,
        default=0,
        null=True,
        blank=True,
        verbose_name='总人数')
    accept = models.IntegerField(
        choices=ACCEPT_CHOICES,
        default=0,
        null=True,
        blank=True,
        verbose_name='能接受的合租对象')
    name = models.CharField(
        max_length=32,
        blank=True,
        default='',
        verbose_name='姓名')
    phone = models.CharField(
        max_length=120,
        blank=True,
        default='',
        verbose_name='手机')
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=0,
        verbose_name='状态')
    audit_status = models.IntegerField(
        choices=AUDIT_STATUS_CHOICES,
        default=0,
        verbose_name='审核状态')

    @property
    def get_profile(self):
        profile = Profile.obs.get_queryset().filter(user=self.user).first()
        return profile


class RentHouseMeet(BaseModel):

    class Meta(object):
        verbose_name = '求租预约'
        verbose_name_plural = '求租预约'

    STATUS_CHOICES = (
        (0, '待看房'),
        (1, '已看房'),
    )

    user = models.ForeignKey(
        User,
        default=None,
        null=True,
        blank=True,
        verbose_name='用户')
    rent_house = models.ForeignKey(
        RentHouse,
        default=None,
        null=True,
        blank=True,
        verbose_name='求租')
    meet_time = models.DateTimeField(
        default=None,
        blank=True,
        null=True,
        verbose_name="预约时间")
    comp_meet_time = models.DateTimeField(
        default=None,
        blank=True,
        null=True,
        verbose_name="已预约时间")
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=0,
        verbose_name='状态')


class HousingResources(BaseModel):

    class Meta(object):
        verbose_name = '房源发布'
        verbose_name_plural = '房源发布'

    LEASE_CHOICES = (
        (0, '整租'),
        (1, '合租')
    )

    DEPOSIT_CHOICES = (
        (0, '押一付三'),
        (1, '押一付一')
    )

    DIRECTION_CHOICES = (
        (0, '东'),
        (1, '南'),
        (2, '西'),
        (3, '北'),
    )

    SITTING_ROOM_CHOICES = (
        (0, '有'),
        (1, '无'),
    )

    VAILD_CHOICES = (
        (0, '否'),
        (1, '是'),
    )

    STATUS_CHOICES = (
        (0, ''),
        (1, '下线'),
        (2, '上线'),
    )

    AUDIT_STATUS_CHOICES = (
        (0, '待审核'),
        (1, '审核不通过'),
        (2, '审核通过'),
    )

    ACCEPT_CHOICES = (
        (0, '白领'),
        (1, '学生'),
        (2, '不限')
    )

    user = models.ForeignKey(
        User,
        default=None,
        null=True,
        blank=True,
        verbose_name='用户')
    infrastructure = models.ManyToManyField(
        Infrastructure, verbose_name="基础设施")
    cover = models.CharField(
        max_length=1024,
        default='',
        blank=True,
        verbose_name="图片")
    house_pcover = models.CharField(
        max_length=1024,
        default='',
        blank=True,
        verbose_name="房产证")
    hall = models.CharField(
        max_length=1024,
        default='',
        blank=True,
        verbose_name="大厅图片")
    peripheral = models.TextField(
        default='',
        null=True,
        blank=True,
        verbose_name='配套设施')
    lease = models.IntegerField(
        choices=LEASE_CHOICES,
        default=0,
        verbose_name='租赁方式')
    month_rent = models.FloatField(default=0, verbose_name='月租金')
    bet = models.FloatField(default=0, verbose_name='押')
    pay = models.FloatField(default=0, verbose_name='付')
    direction = models.IntegerField(
        choices=DIRECTION_CHOICES,
        default=0,
        verbose_name='楼层朝向')
    sitting_room = models.IntegerField(
        choices=SITTING_ROOM_CHOICES,
        default=0,
        verbose_name='有无客厅')
    sitting_room_area = models.FloatField(
        default=0, blank=True, verbose_name="客厅面积")
    sitting_room_complete = models.CharField(
        max_length=1024, default='', blank=True, verbose_name="客厅配套")
    layer = models.IntegerField(default=0, verbose_name='层数')
    province = models.CharField(
        max_length=32,
        default='',
        blank=True,
        null=True,
        verbose_name='省')  # 如何多级选择?
    city = models.CharField(
        max_length=32,
        default='',
        blank=True,
        null=True,
        verbose_name='市')
    area = models.CharField(
        max_length=32,
        default='',
        blank=True,
        null=True,
        verbose_name='区')
    total_layer = models.IntegerField(default=0, verbose_name='总层数')
    category = models.CharField(
        max_length=1024,
        default='',
        blank=True,
        verbose_name="房屋类型")
    community = models.CharField(
        max_length=1024,
        default='',
        blank=True,
        verbose_name="小区名称")
    address = models.CharField(
        max_length=1024,
        default='',
        blank=True,
        verbose_name="详细地址")
    bus = models.CharField(
        max_length=1024,
        default='',
        blank=True,
        verbose_name="公交")
    subway = models.CharField(
        max_length=1024,
        default='',
        blank=True,
        verbose_name="地铁")
    buy = models.CharField(
        max_length=1024,
        default='',
        blank=True,
        verbose_name="购物")
    content = models.TextField(
        default='',
        null=True,
        blank=True,
        verbose_name='房屋描述')
    quality = models.IntegerField(
        choices=VAILD_CHOICES,
        default=0,
        verbose_name='是否为品质房源')
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=0,
        verbose_name='状态')
    audit_status = models.IntegerField(
        choices=AUDIT_STATUS_CHOICES,
        default=0,
        verbose_name='审核状态')
    click_count = models.IntegerField(
        default=0,
        verbose_name='点击量')
    hot = models.IntegerField(
        choices=VAILD_CHOICES,
        default=0,
        verbose_name='最热')
    lng = models.FloatField(default=0, verbose_name='经度')
    lat = models.FloatField(default=0, verbose_name='纬度')

    @property
    def cover_url(self):
        if not self.cover:
            return self.get_pictures()[0] if self.get_pictures() else ''
        return url(self.cover)

    def hall_url(self):
        return url(self.hall)

    def house_pcover_url(self):
        return url(self.house_pcover)

    def get_pictures(self):
        '''获取房屋图片
        '''
        housing_pictures = HousingPicture.obs.get_queryset().filter(
            housing_resources=self
        )
        pictures = [h.picture_url() for h in housing_pictures]

        return pictures

    @property
    def complete_address(self):
        '''获取房源地址
        '''
        return self.province + self.city + self.area + self.address

    @property
    def bedrooms(self):
        '''获取卧室
        '''
        return Bedroom.obs.get_queryset().filter(housing_resources=self)

    @property
    def bedroom_count(self):
        '''获取卧室数量
        '''
        return Bedroom.obs.get_queryset().filter(housing_resources=self).count()


class HousingResourcesMeet(BaseModel):

    class Meta(object):
        verbose_name = '房源预约'
        verbose_name_plural = '房源预约'

    STATUS_CHOICES = (
        (0, '待看房'),
        (1, '已看房'),
    )

    user = models.ForeignKey(
        User,
        default=None,
        null=True,
        blank=True,
        verbose_name='用户')
    housing_resources = models.ForeignKey(
        HousingResources,
        default=None,
        null=True,
        blank=True,
        verbose_name='房源发布')
    meet_time = models.DateTimeField(
        default=None,
        blank=True,
        null=True,
        verbose_name="预约时间")
    comp_meet_time = models.DateTimeField(
        default=None,
        blank=True,
        null=True,
        verbose_name="已预约时间")
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=0,
        verbose_name='状态')


class HousingResourcesComment(BaseModel):

    class Meta(object):
        verbose_name = '房源审核评论'
        verbose_name_plural = '房源审核评论'

    housing_resources = models.ForeignKey(
        HousingResources, null=True, blank=True, verbose_name="房源")
    content = models.TextField(
        default='',
        null=True,
        blank=True,
        verbose_name='房屋描述')


class HousingPicture(BaseModel):

    class Meta(object):
        verbose_name = '房屋图片'
        verbose_name_plural = '房屋图片'

    order_no = models.IntegerField(default=0, verbose_name="排序号")
    housing_resources = models.ForeignKey(
        HousingResources, null=True, blank=True, verbose_name="房源")
    picture = models.CharField(
        max_length=1024,
        default='',
        blank=True,
        verbose_name="图片")

    def picture_url(self):
        return url(self.picture)


class HouseConfig(BaseModel):

    class Meta(object):
        verbose_name = '房间配置'
        verbose_name_plural = '房间配置'

    order_no = models.IntegerField(default=0, verbose_name="排序号")
    name = models.CharField(
        max_length=1024,
        default='',
        blank=True,
        verbose_name="名称")


class Bedroom(BaseModel):

    class Meta(object):
        verbose_name = '房屋卧室'
        verbose_name_plural = '房屋卧室'

    STATUS_CHOICES = (
        (0, '未出租'),
        (1, '已出租'),
    )

    housing_resources = models.ForeignKey(
        HousingResources, null=True, blank=True, verbose_name="房源")
    area = models.FloatField(default=0, blank=True, verbose_name="面积")
    house_config = models.ManyToManyField(
        HouseConfig, verbose_name="房间配置")
    cover = models.CharField(
        max_length=1024,
        default='',
        blank=True,
        verbose_name="图片")
    intro = models.TextField(
        default='',
        null=True,
        blank=True,
        verbose_name='卧室简介')
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=0,
        verbose_name='状态')

    def cover_url(self):
        return url(self.cover)


class HousingEvaluation(BaseModel):

    class Meta(object):
        verbose_name = '房源评价'
        verbose_name_plural = '房源评价'

    NIMING_CHOICES = (
        (0, '匿名'),
        (1, '正常'),
    )

    user = models.ForeignKey(
        User,
        default=None,
        null=True,
        blank=True,
        verbose_name='用户')
    housing_resources = models.ForeignKey(
        HousingResources, null=True, blank=True, verbose_name="房源")
    content = models.TextField(default='', verbose_name="评论内容")
    point = models.FloatField(default=0, null=True, verbose_name="评分")
    niming = models.IntegerField(
        choices=NIMING_CHOICES,
        default=0,
        verbose_name="匿名")

    def imgs(self):
        housing_evaluationimgs = HousingEvaluationImg.obs.get_queryset().filter(
            housing_evaluation=self)

        return [h.img_url() for h in housing_evaluationimgs]


class HousingEvaluationImg(BaseModel):

    class Meta(object):
        verbose_name = '房源评价图片'
        verbose_name_plural = '房源评价图片'

    housing_evaluation = models.ForeignKey(
        HousingEvaluation, null=True, blank=True, verbose_name="房源评价")
    img = models.CharField(
        max_length=1024,
        default='',
        blank=True,
        verbose_name="图片")

    def img_url(self):
        return url(self.img)


class FeedBack(BaseModel):

    class Meta(object):
        verbose_name = '意见反馈'
        verbose_name_plural = '意见反馈'

    user = models.ForeignKey(
        User,
        default=None,
        null=True,
        blank=True,
        verbose_name='用户')
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
    menu_name_str = models.TextField(
        blank=True, default='', verbose_name="菜单名称")

    def __unicode__(self):
        return self.name


class JointVentureAccount(BaseModel):

    class Meta(object):
        verbose_name = "合作企业/管理员账号"
        verbose_name_plural = "合作企业/管理员账号"

    user = models.OneToOneField(
        User,
        default=None,
        null=True,
        blank=True,
        unique=True,
        verbose_name='用户')
    joint_venture = models.ForeignKey(
        JointVenture,
        blank=True,
        null=True,
        verbose_name="合作企业")
    permissions = models.ForeignKey(
        Permissions,
        blank=True,
        null=True,
        verbose_name="所属权限组")


class Setting(BaseModel):

    class Meta(object):
        verbose_name = '配置'
        verbose_name_plural = '配置'

    name = models.CharField(max_length=100, default='', verbose_name="字段")
    value = models.CharField(max_length=100, default='', verbose_name="值")
    code = models.CharField(max_length=100, default='', verbose_name="code")


class HousingResourcesOrder(BaseModel):

    class Meta(object):
        verbose_name = "发布房源订单"
        verbose_name_plural = "发布房源订单"

    PAY_CHOICES = (
        (0, '支付宝PC网站支付'),
        (1, '微信App支付'),
        (2, '支付宝移动支付'),
        (3, '支付宝手机网站支付'),
    )

    STATUS_CHOICES = (
        (0, '待下单'),
        (1, '等待付款'),
        (2, '付款成功'),
        (3, '订单取消'),
        (4, '已完成'),
        (5, '退款申请中'),
        (6, '退款中'),
        (7, '退款成功'),
    )

    order_num = models.CharField(
        max_length=128,
        default='',
        blank=True,
        verbose_name="唯一订单号")
    user = models.ForeignKey(
        User,
        default=None,
        null=True,
        blank=True,
        verbose_name='用户')
    total_fee = models.FloatField(default=0, blank=True, verbose_name="总计金额")
    real_fee = models.FloatField(default=0, blank=True, verbose_name="实际付款")
    pay_way = models.IntegerField(
        choices=PAY_CHOICES,
        default=0,
        verbose_name="支付方式")
    pay_time = models.DateTimeField(auto_now=True, verbose_name="支付时间")
    charge_id = models.CharField(
        max_length=300,
        default='',
        blank=True,
        verbose_name="ping++支付id")
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=0,
        verbose_name="状态")


class Withdrawal(BaseModel):

    class Meta(object):
        verbose_name = "提现"
        verbose_name_plural = "提现"

    STATUS_CHOICES = (
        (0, '未处理'),
        (1, '通过'),
        (2, '不通过')
    )

    join_tventure = models.ForeignKey(
        JointVenture,
        null=True,
        blank=True,
        verbose_name="合作企业")
    money = models.FloatField(default=0, null=True, verbose_name="金额")
    reason = models.CharField(default='', max_length=300, verbose_name="理由")
    status = models.IntegerField(
        choices=STATUS_CHOICES,
        default=0,
        verbose_name="状态")


class HouseDemand(BaseModel):

    class Meta(object):
        verbose_name = "租房需求"
        verbose_name_plural = "租房需求"

    mobile = models.CharField(default='', max_length=300, verbose_name="手机号")
    content = models.CharField(default='', max_length=300, verbose_name="需求")
