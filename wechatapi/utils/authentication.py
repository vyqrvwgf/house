# coding: utf-8

from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions

from web.models import UserInfo
from applet.utils.token_manager import token_decrypt
from settings import DEBUG


class WXAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        # if DEBUG:
        #     return self._authenticate_local(request)

        token = request.META.get('HTTP_AUTHORIZATION', None)
        if not token:
            return None

        d = token_decrypt(token)
        if not d:
            return None
        print d
        try:
            userinfo = UserInfo.objects.filter(openid=d['openid']).first()
            if not userinfo:
                raise Exception("I know python!")
        except Exception as e:
            raise exceptions.AuthenticationFailed('No such user')

        return (userinfo.user, None)

    def _authenticate_local(self, request):
        user = User.objects.filter(username='jinji').first()
        userinfo, _ = UserInfo.objects.get_or_create(user=user)

        openid = '12345'
        userinfo.openid = openid
        userinfo.save()

        return (userinfo.user, None)
