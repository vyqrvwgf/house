# coding: utf-8

from django.contrib import admin
from django.contrib.auth.models import User
from web.models import (
    Profile, AdminLog, Advertising, Column,
    FeedBack, Words, JointVenture, Permissions,
    JointVentureAccount, Setting, Withdrawal,
    Infrastructure, HousingResources, HousingPicture,
    Bedroom, HousingResourcesOrder, HousingResourcesComment,
    HouseConfig, HousingEvaluation, HousingEvaluationImg,
    RentHouse, RentHouseMeet, HousingResourcesMeet, ACL
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
admin.site.register(Infrastructure)
admin.site.register(HousingResources)
admin.site.register(HousingPicture)
admin.site.register(Bedroom)
admin.site.register(HousingResourcesOrder)
admin.site.register(HousingResourcesComment)
admin.site.register(HouseConfig)
admin.site.register(HousingEvaluation)
admin.site.register(HousingEvaluationImg)
admin.site.register(RentHouse)
admin.site.register(RentHouseMeet)
admin.site.register(HousingResourcesMeet)
admin.site.register(ACL)