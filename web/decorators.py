# coding: utf-8

from functools import partial

from django.contrib.auth.decorators import login_required
from django.utils.functional import wraps
from django.http import HttpResponse

from backend.models import ACL


backend_login_required = partial(login_required, login_url='/admin/login')


def backend_permission_required(codename, module):
    def decorator(view):
        @wraps(view)
        def wrapper(request, *args, **kwargs):
            print module
            acl = ACL.objects.get(module=module)
            if not request.user.has_perm(codename, acl):
                return HttpResponse(status=403)

            return view(request, *args, **kwargs)

        return wrapper

    return decorator
