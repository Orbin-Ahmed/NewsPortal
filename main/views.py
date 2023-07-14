import re

from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponseRedirect
from django.shortcuts import render
from .services import *


# Create your views here.


def login(request):
    if request.method == "POST":
        username = request.POST['usernameInput']
        password = request.POST['passwordInput']
        user_object = user_login(request, username, password)
        if user_object:
            if user_object.user_type == 3:
                return HttpResponseRedirect('/publish-news/')
            elif user_object.user_type == 2:
                return HttpResponseRedirect('/pending-news/')
            else:
                return HttpResponseRedirect('/admin-news/')
        else:
            print("Invalid")
            return HttpResponseRedirect('/')
    return render(request, 'auth/login.html')


# Admin View Start
def admin_news(request):
    user_obj = request.user
    if user_obj == AnonymousUser():
        return HttpResponseRedirect('/')
    elif user_obj.user_type == 1:
        user_obj = user_obj.username
    return render(request, 'admin/admin_news.html', {'user_name': user_obj})


def moderator_status(request):
    user_obj = request.user
    if user_obj == AnonymousUser():
        return HttpResponseRedirect('/')
    elif user_obj.user_type == 1:
        user_obj = user_obj.username
    return render(request, 'admin/moderator_status.html', {'user_name': user_obj})


def reporter_suspend(request):
    user_obj = request.user
    if user_obj == AnonymousUser():
        return HttpResponseRedirect('/')
    elif user_obj.user_type == 1:
        user_obj = user_obj.username
    return render(request, 'admin/admin_reporter_status.html', {'user_name': user_obj})


# Admin View End

# Reporter View Start
def publish_news(request):
    user_obj = request.user
    if user_obj == AnonymousUser():
        return HttpResponseRedirect('/')
    elif user_obj.user_type == 3:
        user_obj = user_obj.username
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

            t = post_report(request, title_bn, details_bn, tag_bn, category_bn, news_image, title_en, details_en,
                            tag_en,
                            category_en)
        return render(request, 'reporter/newReport.html', {'user_name': user_obj})
    else:
        return HttpResponseRedirect('/')


def edit_news(request):
    user_obj = request.user
    if user_obj == AnonymousUser():
        return HttpResponseRedirect('/')
    elif user_obj.user_type == 3:
        user_obj = user_obj.username
        return render(request, 'reporter/editReport.html', {'user_name': user_obj})
    else:
        return HttpResponseRedirect('/')


# Reporter View End

# Moderator View start
def pending_news(request):
    user_obj = request.user
    if user_obj == AnonymousUser():
        return HttpResponseRedirect('/')
    elif user_obj.user_type == 2:
        user_obj = user_obj.username
        pending_news_list = moderator_view(request)
        loop_counter = int(pending_news_list.count() / 2);
        return render(request, 'moderator/pending_news.html',
                      {'user_name': user_obj, 'pending_news_list': pending_news_list, 'loop_counter': loop_counter})
    else:
        return HttpResponseRedirect('/')


def all_news(request):
    user_obj = request.user
    if user_obj == AnonymousUser():
        return HttpResponseRedirect('/')
    elif user_obj.user_type == 2:
        user_obj = user_obj.username
        return render(request, 'moderator/all_news.html', {'user_name': user_obj})
    else:
        return HttpResponseRedirect('/')


def trendy_news(request):
    user_obj = request.user
    if user_obj == AnonymousUser():
        return HttpResponseRedirect('/')
    elif user_obj.user_type == 2:
        user_obj = user_obj.username
        return render(request, 'moderator/trendy_news.html', {'user_name': user_obj})
    else:
        return HttpResponseRedirect('/')


def rolling_headlines(request):
    user_obj = request.user
    if user_obj == AnonymousUser():
        return HttpResponseRedirect('/')
    elif user_obj.user_type == 2:
        user_obj = user_obj.username
        return render(request, 'moderator/rolling_headline.html', {'user_name': user_obj})
    else:
        return HttpResponseRedirect('/')


def reporter_status(request):
    user_obj = request.user
    if user_obj == AnonymousUser():
        return HttpResponseRedirect('/')
    elif user_obj.user_type == 2:
        user_obj = user_obj.username
        return render(request, 'moderator/reporter_status.html', {'user_name': user_obj})
    else:
        return HttpResponseRedirect('/')


def focus_news(request):
    user_obj = request.user
    if user_obj == AnonymousUser():
        return HttpResponseRedirect('/')
    elif user_obj.user_type == 2:
        user_obj = user_obj.username
        return render(request, 'moderator/focus_news.html', {'user_name': user_obj})
    else:
        return HttpResponseRedirect('/')


# Moderator View End

def news_details(request, news_id):
    user_obj = request.user
    if user_obj == AnonymousUser():
        return HttpResponseRedirect('/')
    elif user_obj.user_type != 3:
        user_obj = user_obj.username
        news_details_info = post_details(news_id)
        news_details_info.bangla_content = re.sub(r'\r?\n', '', news_details_info.bangla_content)
        news_details_info.english_content = re.sub(r'\r?\n', '', news_details_info.english_content)
        return render(request, 'moderator/report_details.html',
                      {'news_details': news_details_info, 'user_name': user_obj})
    else:
        return HttpResponseRedirect('/')


# Single Api View start
def approve_post_view(request, post_id):
    approve_post(request, post_id)
    return HttpResponseRedirect('/pending-news/')
