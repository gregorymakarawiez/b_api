

from django.shortcuts import render
from django.contrib.auth.decorators import login_required




from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.http import *
from django.views.generic import TemplateView
from django.conf import settings

@login_required
def base(request):
    return render(request, 'base.html')

@login_required
def home(request):
    return render(request,"home.html")


