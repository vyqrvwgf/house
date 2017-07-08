# coding: utf-8

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.template import loader


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)
            if user.is_superuser or user.is_staff:
                return HttpResponseRedirect('/admin/')
        else:
            context = {'error': '帐号/密码不正确'}
            template = loader.get_template('login.html')
            return HttpResponse(template.render(context, request))

    context = {}
    template = loader.get_template('login.html')
    return HttpResponse(template.render(context, request))


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/admin/login')
