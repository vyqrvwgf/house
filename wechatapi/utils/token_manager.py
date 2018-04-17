# coding: utf-8

import time
import json
import logging

from utils.prpcrypt import Prpcrypt

pc = Prpcrypt(b'0000000000000000')

EXPIRED = 3600 * 24 * 30


def token_encrypt(session_key, openid):
    '''加密生成token
    '''
    now = int(time.time())
    d = {
        'session_key': session_key,
        'openid': openid,
        'expired': now + EXPIRED,
    }
    token = pc.encrypt(json.dumps(d))

    return token


def token_decrypt(token):
    '''根据token解密
    '''
    try:
        d = json.loads(pc.decrypt(token))
    except Exception as e:
        logging.error(e)
        logging.error('-----------token_decrypt-------------')
        return None

    session_key = d.get('session_key', None)
    openid = d.get('openid', None)
    expired = d.get('expired', 0)

    now = int(time.time())
    if session_key and openid and expired > now:
        return d
    return None
