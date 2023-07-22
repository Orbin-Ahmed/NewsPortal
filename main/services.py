from datetime import datetime, date
import pybengali
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.utils.timezone import make_aware

from main.models import Post, EnglishCategory, BanglaCategory, EnglishTag, BanglaTag, SpecialNews, User


# login call -> returns None if not authenticated

def user_login(request, username, password):
    user = authenticate(request, username=username, password=password)
    if user is not None:
        if user.user_type == 3 and user.is_suspended is True:
            return False
        else:
            login(request, user)
        return user
    else:
        return None


# post call for report -> return report object

def post_report(request, bangla_title, bangla_content, bangla_tag, bangla_category, image,
                english_title, english_content, english_tag, english_category):
    if not BanglaCategory.objects.filter(the_category=bangla_category):
        bangla_category_object = BanglaCategory.objects.create(the_category=bangla_category)
    else:
        bangla_category_object = BanglaCategory.objects.get(the_category=bangla_category)

    if not EnglishCategory.objects.filter(the_category=english_category.lower()):
        english_category_object = EnglishCategory.objects.create(the_category=english_category.lower())
    else:
        english_category_object = EnglishCategory.objects.get(the_category=english_category.lower())

    report_object = Post.objects.create(reporter=request.user,
                                        image=image,
                                        english_title=english_title,
                                        bangla_title=bangla_title,
                                        english_content=english_content,
                                        bangla_content=bangla_content,
                                        english_category=english_category_object,
                                        bangla_category=bangla_category_object,
                                        )
    for i in english_tag:
        i = i.lower()
        tag_object = EnglishTag.objects.filter(the_tag=i)
        if tag_object:
            for each in tag_object:
                each.post.add(report_object)
                each.save()
        else:
            new_tag_object = EnglishTag.objects.create(the_tag=i)
            new_tag_object.post.add(report_object)
            new_tag_object.save()

    for i in bangla_tag:
        tag_object = BanglaTag.objects.filter(the_tag=i)
        if tag_object:
            for each in tag_object:
                each.post.add(report_object)
                each.save()
        else:
            new_tag_object = BanglaTag.objects.create(the_tag=i)
            new_tag_object.post.add(report_object)
            new_tag_object.save()

    return report_object


# approval from moderator

def approve_post(request, post_id):
    if request.user.user_type == 2:
        post_object = Post.objects.get(id=post_id)
        post_object.is_approved = True
        post_object.need_edit = False
        post_object.date_created = make_aware(datetime.now())
        # approved true, need edit false
        post_object.save()
        return True
    else:
        return None


# need edit from reporter
def re_edit_post(request, post_id):
    if request.user.user_type == 2:
        post_object = Post.objects.get(id=post_id)
        post_object.is_approved = False
        post_object.need_edit = True
        # approved false, need edit True
        post_object.save()
        return True
    else:
        return None


# delete post by moderator
def delete_post(request, post_id):
    if request.user.user_type == 2:
        post_object = Post.objects.get(id=post_id)
        post_object.delete()
        # directly delete
        return True
    else:
        return None


# moderator view
def moderator_view(request):
    if request.user.user_type == 2:
        post_list = Post.objects.filter(is_approved=False, need_edit=False)
        return post_list  # queryset for iteration
    else:
        return False


# reporter view for need editing
def reporter_view(request):
    if request.user.user_type == 3:
        post_list = Post.objects.filter(is_approved=False, need_edit=True, reporter=request.user)
        return post_list
    else:
        return False


# return post object
def post_details(post_id):
    post_object = Post.objects.get(id=post_id)
    bn_tag = BanglaTag.objects.get(post=post_object).the_tag
    en_tag = EnglishTag.objects.get(post=post_object).the_tag
    the_list = [bn_tag, en_tag, post_object]
    return the_list


# add to special
def add_to_special(post_id, post_type):
    post_object = Post.objects.get(id=post_id)
    if not SpecialNews.objects.filter(post=post_object):
        SpecialNews.objects.create(post=post_object)
    if post_type == "headline":
        if SpecialNews.objects.filter(is_headline=True).count() > 29:
            return "remove headlines"
        else:
            post_object.specialnews.is_headline = True
            post_object.specialnews.save()
            return True
    elif post_type == "trending":
        if SpecialNews.objects.filter(is_trending=True).count() > 29:
            return "remove trending"
        else:
            post_object.specialnews.is_trending = True
            post_object.specialnews.save()
            return True
    elif post_type == "focus":
        if SpecialNews.objects.filter(is_focus=True).count() > 29:
            return "remove focus"
        else:
            post_object.specialnews.is_focus = True
            post_object.specialnews.save()
            return True
    else:
        return "incorrect type"


def remove_from_special(post_id, post_type):
    post_object = Post.objects.get(id=post_id)
    if post_type == "headline":
        post_object.specialnews.is_headline = False
        post_object.specialnews.save()
    elif post_type == "trending":
        post_object.specialnews.is_trending = False
        post_object.specialnews.save()
    elif post_type == "focus":
        post_object.specialnews.is_focus = False
        post_object.specialnews.save()
    else:
        return "incorrect type"


# admin view all approved news
def admin_view(request):
    if request.user.user_type == 1 or request.user.user_type == 2:
        post_list = Post.objects.filter(is_approved=True)
        return post_list
    else:
        return False


# date filter view all approved news
def filter_date_view(request, _date):
    post_list = Post.objects.filter(is_approved=True, date_created=_date)
    return post_list


# admin delete news
def delete_news(request, post_id):
    if request.user.user_type == 1 or request.user.user_type == 2:
        post = Post.objects.get(id=post_id)
        post.delete()
        return True
    else:
        return None


# suspend
def suspend_user(request, username):
    user_object = User.objects.get(username=username)
    if request.user.user_type == 1:
        if not user_object.is_suspended:
            user_object.is_suspended = True
            user_object.save()
        else:
            user_object.is_suspended = False
            user_object.save()
        return True
    elif request.user.user_type == 2:
        if user_object.user_type == 3:
            if not user_object.is_suspended:
                user_object.is_suspended = True
                user_object.save()
            else:
                user_object.is_suspended = False
                user_object.save()
            return True
        else:
            return "invalid rank"
    else:
        return False


# # unsuspend
# def unsuspend_user(request, username):
#     user_object = User.objects.get(username=username)
#     if request.user.user_type == 1:
#         user_object.is_suspended = False
#         user_object.save()
#         return True
#     elif request.user.user_type == 2:
#         if user_object.user_type == 3:
#             user_object.is_suspended = False
#             user_object.save()
#             return True
#         else:
#             return "cant unsuspend same rank"
#     else:
#         return False


# change pass
def pass_update(request, username, new_pass1, new_pass2):
    if new_pass1 != new_pass2:
        return "Password mismatch"
    else:
        user_object = User.objects.get(username=username)
        if request.user.user_type == 1:
            user_object.password = make_password(new_pass1)
            user_object.save()
            return True
        elif request.user.user_type == 2:
            if user_object.user_type == 3:
                user_object.password = make_password(new_pass1)
                user_object.save()
                return True
            else:
                return "cant suspend same rank"
        else:
            return False


def reporter_list():
    user_list = User.objects.filter(user_type=3)
    users = []
    for i in user_list:
        the_object = {
            "username": i.username,
            "is_suspended": i.is_suspended
        }
        users.append(the_object)
    return users


def moderator_list():
    user_list = User.objects.filter(user_type=2)
    the_list = []
    for i in user_list:
        the_object = {
            "username": i.username,
            "is_suspended": i.is_suspended
        }
        the_list.append(the_object)
    return the_list


def headline_list():
    return SpecialNews.objects.filter(is_headline=True)


def trending_list():
    return SpecialNews.objects.filter(is_trending=True)


def bangla_date():
    bangla_object = pybengali.today()
    today = date.today()
    english_object = {
        "english_year": pybengali.convert_e2b_digit(date.today().year),
        "english_month": pybengali.eng_month_to_bengali(date.today().month),
        "english_date": pybengali.convert_e2b_digit(date.today().day)
    }
    bangla_object.update(english_object)
    return bangla_object


# # reporter edits the post
# def edit_post(request, post_id, update_object):
#     if request.user.user_type == 3:
#         post_object = Post.objects.get(id=post_id)
#         key_list = list(update_object.keys())
#         for i in key_list:
#             if i == "image":
#                 post_object.image = update_object.get("image")
#                 post_object.save()
#             if i == "english_content":
#                 post_object.english_content = update_object.get("english_content")
#                 post_object.save()
#             if i == "bangla_content":
#                 post_object.bangla_content = update_object.get("bangla_content")
#                 post_object.save()
#             if i == "english_title":
#                 post_object.english_title = update_object.get("english_title")
#                 post_object.save()
#             if i == "bangla_title":
#                 post_object.bangla_title = update_object.get("bangla_title")
#                 post_object.save()
#             if i == "english_category":
#                 post_object.english_category = update_object.get("english_category")
#                 post_object.save()
#             if i == "bangla_category":
#                 post_object.bangla_category = update_object.get("bangla_category")
#                 post_object.save()
#             # send me all the new tags, previous tags will be deleted
#             if i == "english_tag":
#                 the_tag = update_object.get("english_tag").lower()
#                 for j in the_tag:
#                     remove_tag_objects = EnglishTag.objects.filter(post=post_object)
#                     for each in remove_tag_objects:
#                         each.post.remove(post_object)
#                     add_tag_objects = EnglishTag.objects.filter(the_tag=j)
#                 if add_tag_objects:
#                     for each in add_tag_objects:
#                         each.post.add(post_object)
#                         each.save()
#                 else:
#                     new_tag_object = EnglishTag.objects.create(the_tag=j)
#                     new_tag_object.post.add(post_object)
#                     new_tag_object.save()
#             # send me all the new tags, previous tags will be deleted
#             if i == "bangla_tag":
#                 the_tag = update_object.get("bangla_tag").lower()
#                 for j in the_tag:
#                     remove_tag_objects = BanglaTag.objects.filter(post=post_object)
#                     for each in remove_tag_objects:
#                         each.post.remove(post_object)
#                     add_tag_objects = BanglaTag.objects.filter(the_tag=j)
#                 if add_tag_objects:
#                     for each in add_tag_objects:
#                         each.post.add(post_object)
#                         each.save()
#                 else:
#                     new_tag_object = BanglaTag.objects.create(the_tag=j)
#                     new_tag_object.post.add(post_object)
#                     new_tag_object.save()
#         return True
#     else:
#         return None

def edit_post(request, post_id, update_object):
    if request.user.user_type == 3:
        post_object = Post.objects.get(id=post_id)
        post_object.delete()
        return post_report(request,
                           update_object.get("bangla_title"),
                           update_object.get("bangla_content"),
                           update_object.get("bangla_tag"),
                           update_object.get("bangla_category"),
                           update_object.get("image"),
                           update_object.get("english_title"),
                           update_object.get("english_content"),
                           update_object.get("english_tag"),
                           update_object.get("english_category")
                           )


# trending top views in descending order -> 8 objects returned in queryset
def highlights():
    approved_post = Post.objects.filter(is_approved=True, specialnews__is_trending=True)
    return approved_post.order_by("-view_counter")[:10]


# returns a list of category except static 5 ta -> returns [["english_category", "bangla_category"], ... ]
def category_list():
    approved_post = Post.objects.filter(is_approved=True)
    approved_post = approved_post.exclude(Q(english_category__the_category="national") |
                                          Q(english_category__the_category="sports") |
                                          Q(english_category__the_category="country") |
                                          Q(english_category__the_category="showbiz") |
                                          Q(english_category__the_category="world")).distinct(
        "english_category__the_category")
    _list = []
    for each in approved_post:
        combo = [each.english_category.the_category, each.bangla_category.the_category]
        _list.append(combo)
    return _list


# # returns queryset of trending all
# def focus_list():
#     approved_post = Post.objects.filter(is_approved=True)
#     return approved_post.filter(specialnews__is_trending=True)
#
#
# # returns queryset of headline all
# def headline_list():
#     approved_post = Post.objects.filter(is_approved=True)
#     return approved_post.filter(specialnews__is_headline=True)


# like counter -> returns True when done
def like_counter(post_id):
    post_object = Post.objects.get(id=post_id)
    post_object.like_counter = post_object.like_counter + 1
    post_object.save()
    return True


# view counter -> returns True when done
def view_counter(post_id):
    post_object = Post.objects.get(id=post_id)
    post_object.view_counter = post_object.view_counter + 1
    post_object.save()
    return True


def latest_news():
    return Post.objects.filter(is_approved=True).order_by("-date_created")[:30]


def highest_view_category_news(category_name, number=None):
    result = Post.objects.filter(is_approved=True, english_category__the_category=category_name.lower()).order_by(
        "-view_counter")
    if number is None:
        result = result[:number]
    return result


def latest_category_news(category_name):
    return Post.objects.filter(is_approved=True, english_category__the_category=category_name.lower()).order_by(
        "-date_created")


def max_views_today():
    result = Post.objects.filter(is_approved=True, date_created__day=datetime.today().day).order_by("-view_counter")
    if result.count() > 30:
        result = result[:30]
    return result


def filtered_all_news():
    approved_post = Post.objects.filter(is_approved=True)
    return approved_post.exclude(Q(english_category__the_category="national") |
                                 Q(english_category__the_category="sports") |
                                 Q(english_category__the_category="country") |
                                 Q(english_category__the_category="showbiz") |
                                 Q(english_category__the_category="world"))


def search_filter(keyword):
    approved_post = Post.objects.filter(is_approved=True)
    return approved_post.filter(Q(english_title__icontains=keyword) |
                                Q(bangla_title__icontains=keyword) |
                                Q(englishtag__the_tag__icontains=keyword) |
                                Q(banglatag__the_tag__icontains=keyword)).distinct("id")


def today_all_news():
    return Post.objects.filter(is_approved=True, date_created__day=datetime.today().day)

def today_all_headlines():
    return Post.objects.filter(is_approved=True, specialnews__is_headline=True, date_created__day=datetime.today().day)
