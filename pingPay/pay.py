# -*- coding: utf-8 -*-

'''
  Ping++ Server SDK 说明：
  以下代码只是为了方便商户测试而提供的样例代码，商户可根据自己网站需求按照技术文档编写, 并非一定要使用该代码。
  接入支付流程参考开发者中心：https://www.pingxx.com/docs/server/charge ，文档可筛选后端语言和接入渠道。
  该代码仅供学习和研究 Ping++ SDK 使用，仅供参考。
'''

from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from settings import API_KEY, APP_ID

import base64
import pingpp
import random
import string
import os
import simplejson

# api_key 获取方式：登录 [Dashboard](https://dashboard.pingxx.com)->点击管理平台右上角公司名称->开发信息-> Secret Key
api_key = API_KEY
# app_id 获取方式：登录 [Dashboard](https://dashboard.pingxx.com)->点击你创建的应用->应用首页->应用 ID(App ID)
app_id = APP_ID
# 设置 API Key
pingpp.api_key = api_key

'''
  设置请求签名密钥，密钥对需要你自己用 openssl 工具生成，如何生成可以参考帮助中心：https://help.pingxx.com/article/123161；
  生成密钥后，需要在代码中设置请求签名的私钥(rsa_private_key.pem)；
  然后登录 [Dashboard](https://dashboard.pingxx.com)->点击右上角公司名称->开发信息->商户公钥（用于商户身份验证）
  将你的公钥复制粘贴进去并且保存->先启用 Test 模式进行测试->测试通过后启用 Live 模式
'''
# 设置私钥内容方式1：通过路径读取签名私钥
pingpp.private_key_path = os.path.join(
    os.path.dirname(__file__), 'RSACert/rsa_private_key.pem')

# 设置私钥内容方式2：直接设置请求签名私钥内容
# pingpp.private_key = '''-----BEGIN RSA PRIVATE KEY-----
# 私钥内容字符串
# -----END RSA PRIVATE KEY-----'''

# 订单号推荐使用 8-20 位，要求数字或字母，不允许其他字符


def decode_base64(data):
    remainder = len(data) % 4
    if remainder:
        data += '=' * (4 - remainder)
    return base64.decodestring(data.encode('utf-8'))


def verify(data, sign):
    signs = decode_base64(sign)
    data = data.decode('utf-8') if hasattr(data, "decode") else data
    pubkeystr = open(os.path.join(os.path.dirname(__file__), 'RSACert/rsa_public_key.pem')).read()
    pubkey = RSA.importKey(pubkeystr)
    digest = SHA256.new(data.encode('utf-8'))
    pkcs = PKCS1_v1_5.new(pubkey)
    return pkcs.verify(digest, signs)


def create_ping_order(orderno, subject, body, amount, channel, client_ip, openid='', success_url=''):
    amount = int(float(amount)*100)
    c_dict = {
        'subject': subject,
        'body': body,
        'amount': amount,
        'order_no': orderno,
        'currency': 'cny',
        'channel': channel,
        'client_ip': client_ip,
        'app': dict(id=app_id),
    }
    if channel == 'wx_pub':
        c_dict['extra'] = dict(open_id=openid)
    elif channel == 'alipay_wap' or channel == 'alipay_pc_direct':
        c_dict['extra'] = dict(success_url=success_url)
    ch = pingpp.Charge.create(**c_dict)
    print ch, '------------------------charge------------------------'
    return simplejson.loads(ch.to_str())  # 输出 Ping++ 返回的支付凭据 Charge


# 退款
def do_refund(charge_id, description, amount):
    amount = int(float(amount)*100)
    ch = pingpp.Charge.retrieve(charge_id)
    re = ch.refunds.create(description=description, amount=amount)
    return re
