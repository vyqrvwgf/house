# coding: utf-8

SETTING_CONFIG = [
	{'name': 'course_zeng_song', 'value': '', 'detail': '课程海囤币'},
	{'name': 'course_diyong_price', 'value': '', 'detail': '课程抵用金额'},
	{'name': 'goods_zeng_song', 'value': '', 'detail': '商品海囤币'},
	{'name': 'goods_diyong_price', 'value': '', 'detail': '商品抵用金额'},
	{'name': 'integral_auto', 'value': '', 'detail': '积分消费'},
]

MENU_LIST = [
             {'module': 'home', 'name': '首页'},
                {'module': 'advertising', 'name': '轮播图管理', 'parent_module': 'home'},
             {'module': 'column', 'name': '栏目管理'},
             {'module': 'joint_venture', 'name': '合作企业'},
             {'module': 'wanted', 'name': '求租列表'},
             {'module': 'listings', 'name': '房源列表'},
             {'module': 'work_approval', 'name': '流程审批'},
                {'module': 'authentication', 'name': '身份认证', 'parent_module': 'work_approval'},
                {'module': 'wanted_release', 'name': '求租发布', 'parent_module': 'work_approval'},
                {'module': 'listings_release', 'name': '房源发布', 'parent_module': 'work_approval'},
             {'module': 'information', 'name': '信息中心'},
                {'module': 'market_feedback', 'name': '市场反馈', 'parent_module': 'information'},
             {'module': 'activity', 'name': '活动管理'},
             {'module': 'bill', 'name': '财务明细'},
             {'module': 'join', 'name': '合作管理'},
             {'module': 'settings', 'name': '系统管理'},
                {'module': 'sms', 'name': '短信', 'parent_module': 'settings'},
                {'module': 'feedback', 'name': '意见反馈', 'parent_module': 'settings'},
                {'module': 'joint_venture_account', 'name': '合作企业管理员', 'parent_module': 'settings'},
                {'module': 'operating', 'name': '系统管理员', 'parent_module': 'settings'},
                {'module': 'permissions', 'name': '权限组', 'parent_module': 'settings'}
            ]

