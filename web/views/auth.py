# coding: utf-8

from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.template import loader
from web.models import (
    JointVentureAccount,
)

def login_view(request):
    context = {}
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)

        if not user or not user.is_active:
            context['error'] = '帐号/密码不正确'
        else:
            login(request, user)
            joint_venture_account = JointVentureAccount.objects.filter(user=user).first()
            if joint_venture_account:
                menu_str = joint_venture_account.permissions.menu_str
                request.session['menu_str'] = menu_str.split(',')
            return HttpResponseRedirect('/admin/') 

    template = loader.get_template('login.html')
    return HttpResponse(template.render(context, request))


@login_required
def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/admin/login')
