from django.contrib.auth.hashers import make_password
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .services import *


# Create your views here.


def login(request):
    if request.method == "POST":
        username = request.POST['usernameInput']
        password = request.POST['passwordInput']
        print(make_password(password))
        user_object = user_login(request, username, password)
        if user_object:
            if user_object.user_type == 3:
                return HttpResponseRedirect('/publish-news/')
            else:
                return HttpResponseRedirect('/pending-news/')
        else:
            print("None")
    return render(request, 'auth/login.html')


def publish_news(request):
    if request.method == "POST":
        title_bn = request.POST['newsTitleBN']
        details_bn = request.POST['detailsNewsBN']
        tag_bn = request.POST['newsTagBN']
        tag_bn = [tag_bn]
        category_bn = request.POST['newsCategoryBN']

        title_en = request.POST['newsTitleEn']
        details_en = request.POST['detailsNewsEN']
        tag_en = request.POST['newsTagEN']
        tag_en = [tag_en]
        category_en = request.POST['newsCategoryEN']

        news_image = request.FILES['news_image']

        t = post_report(request, title_bn, details_bn, tag_bn, category_bn, news_image, title_en, details_en, tag_en,
                        category_en)
        print(t)
    return render(request, 'reporter/newReport.html')


def edit_news(request):
    return render(request, 'reporter/editReport.html')


def pending_news(request):
    return render(request, 'moderator/pending_news.html')


def all_news(request):
    return render(request, 'moderator/all_news.html')


def trendy_news(request):
    return render(request, 'moderator/trendy_news.html')


def rolling_headlines(request):
    return render(request, 'moderator/rolling_headline.html')


def reporter_status(request):
    return render(request, 'moderator/reporter_status.html')


def focus_news(request):
    return render(request, 'moderator/focus_news.html')
