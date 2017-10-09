# coding: utf-8

SETTING_CONFIG = [
    {
        'name':'房源发布支付金额',
        'value':'0',
        'code':'housing_resources_pay'
    },
]

MENU_LIST = [
             {'module': 'home', 'name': '首页'},
                {'module': 'advertising', 'name': '轮播图管理', 'parent_module': 'home'},
                {'module': 'news', 'name': '最新资讯', 'parent_module': 'home'},
             {'module': 'column', 'name': '栏目管理'},
             {'module': 'user', 'name': '用户管理'},
             {'module': 'joint_venture', 'name': '服务商管理'},
             {'module': 'rent_house', 'name': '租房管理'},
                {'module': 'infrastructure', 'name': '基础设施', 'parent_module': 'rent_house'},
                {'module': 'listings', 'name': '房源列表', 'parent_module': 'rent_house'},
                {'module': 'wanted', 'name': '求租列表', 'parent_module': 'rent_house'},
             {'module': 'work_approval', 'name': '流程审批'},
                {'module': 'authentication', 'name': '身份认证', 'parent_module': 'work_approval'},
                {'module': 'wanted_release', 'name': '求租发布', 'parent_module': 'work_approval'},
                {'module': 'listings_release', 'name': '房源发布', 'parent_module': 'work_approval'},
             {'module': 'information', 'name': '信息中心'},
                {'module': 'market_feedback', 'name': '市场反馈', 'parent_module': 'information'},
                {'module': 'complaints', 'name': '投诉管理', 'parent_module': 'information'},
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

