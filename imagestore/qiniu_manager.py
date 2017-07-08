# coding: utf-8

import os
import logging
import time

from settings import (
    QINIU_DOMAIN,
    QINIU_ACCESS_KEY,
    QINIU_SECRET_KEY,
    BUCKET_NAME,
    BASE_DIR
)


def upload(key, localpath):
    from qiniu import Auth, put_file, set_default
    q = Auth(QINIU_ACCESS_KEY, QINIU_SECRET_KEY)
    key = os.path.join(BUCKET_NAME, key)
    token = q.upload_token(BUCKET_NAME, key)
    ret, info = put_file(token, key, localpath)
    # 删除本地存在的文件
    if os.path.exists(localpath):
        os.remove(localpath)


def url(key):
    if key:
        return 'http://' + os.path.join(QINIU_DOMAIN, BUCKET_NAME, key)
    else:
        return ''

def o_url(key):
    if key:
        return 'http://' + os.path.join(QINIU_DOMAIN, key)
    else:
        return ''


def get_extension(filename):
    arr = filename.split('.')
    if not arr:
        return ''

    return arr[-1]


def handle_uploaded_file(f, path):
    from settings import UPLOAD_DIR
    with open(os.path.join(UPLOAD_DIR, path), 'wb') as dest:
        for chunk in f.chunks():
            dest.write(chunk)

