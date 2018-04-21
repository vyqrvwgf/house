# coding: utf-8

import urllib
from settings import DOMAIN, WECHAT_APP_ID

GET = 'GET'
POST = 'POST'


WECHAT_REDIRECT_URI = '{}/h5/wechat/callback/'.format(DOMAIN,)
WECHAT_GET_ACCESS_TOKEN_URL = 'https://api.weixin.qq.com/sns/oauth2/access_token?appid={}&secret={}&code={}&grant_type=authorization_code'
WECHAT_AUTH_URL = 'https://open.weixin.qq.com/connect/oauth2/authorize?appid={}&redirect_uri={}&response_type=code&scope=snsapi_userinfo&state=STATE#wechat_redirect'.format(
    WECHAT_APP_ID,
    urllib.quote_plus(WECHAT_REDIRECT_URI)
)
WECAHT_USER_INFO_URL = 'https://api.weixin.qq.com/sns/userinfo?access_token={}&openid={}&lang=zh_CN'

TEMPLATE_SET_INDUSTRY_URL = 'https://api.weixin.qq.com/cgi-bin/template/api_set_industry?access_token={}'
TEMPLATE_GET_INDUSTRY_INFO_URL = 'https://api.weixin.qq.com/cgi-bin/template/get_industry?access_token={}'
TEMPLATE_GET_ID_URL = 'https://api.weixin.qq.com/cgi-bin/template/api_add_template?access_token={}'
TEMPLATE_GET_LIST_URL = 'https://api.weixin.qq.com/cgi-bin/template/get_all_private_template?access_token={}'
TEMPLATE_DELETE_URL = 'https://api.weixin.qq.com/cgi-bin/template/del_private_template?access_token={}'
TEMPLATE_SEND_MESSAGE_URL = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token={}'
