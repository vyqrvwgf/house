# coding: utf-8

from django.contrib.auth.models import User
from web.models import Profile


class MobileBackend(object):

    def authenticate(self, mobile=None, password=None):
        try:
            profile = Profile.objects.get(mobile=mobile)
            user = profile.user
            if user.check_password(password):
                return user
            else:
                return None
        except Profile.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
