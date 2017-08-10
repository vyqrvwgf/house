# coding: utf-8

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.contrib.auth import login, logout, authenticate
from django.contrib.admin.views.decorators import staff_member_required
from django.views.decorators.csrf import csrf_exempt
from web.models import(
    Advertising
)
import os
import datetime
import time
import simplejson
import requests
import random
import string
import logging


def index(request):

    context = {
        'module': 'index',
    }

    return render(request, 'frontend/index.html', context)


def register(request):

    context = {
        'module': 'index',
    }

    return render(request, 'frontend/register.html', context)


def login(request):

    context = {
        'module': 'index',
    }

    return render(request, 'frontend/login.html', context)

