# conding: utf-8

import redis
import os
import hashlib
import json

from settings import (
    WXAPP_APPID,
    REDIS_HOST,
    REDIS_PORT,
    REDIS_DB_WECHAT_SESSION,
)

r = redis.StrictRedis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    db=REDIS_DB_WECHAT_SESSION)

EXPIRED = 60 * 60 * 24 * 30


def set_wxapp_session(session_key, openid):
    '''保存openid、session_key，返回key，
    '''
    if not WXAPP_APPID:
        raise Exception('not WXAPP_APPID')

    k = hashlib.sha1(WXAPP_APPID + os.urandom(24)).hexdigest()
    v = json.dumps({
        'session_key': session_key,
        'openid': openid,
    })

    r.set(k, v, EXPIRED)

    return k


def get_wxapp_session(k):
    '''获取openid、session_key
    '''

    v = r.get(k)
    if not v:
        return None

    r.set(k, v, EXPIRED)
    obj = json.loads(v)

    return obj
