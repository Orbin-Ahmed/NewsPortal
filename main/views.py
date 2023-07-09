from django.shortcuts import render
from .services import *


# Create your views here.


def login(request):
    if request.method == "POST":
        username = request.POST['usernameInput']
        password = request.POST['passwordInput']
        t = t_login(username, password)
        print(t)
    return render(request, 'auth/login.html')


def publish_news(request):
    return render(request, 'reporter/newReport.html')


def edit_news(request):
    return render(request, 'reporter/editReport.html')
