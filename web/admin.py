# coding: utf-8

from django.contrib import admin
from django.contrib.auth.models import User
from web.models import (
    Profile, AdminLog, Advertising, Column,
    FeedBack, Words, JointVenture, Permissions,
    JointVentureAccount, Setting, Withdrawal
)


admin.site.register(Profile)
admin.site.register(AdminLog)
admin.site.register(Advertising)
admin.site.register(Column)
admin.site.register(FeedBack)
admin.site.register(Words)
admin.site.register(JointVenture)
admin.site.register(Permissions)
admin.site.register(JointVentureAccount)
admin.site.register(Setting)
admin.site.register(Withdrawal)

