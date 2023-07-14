from datetime import datetime

from django.contrib.auth import authenticate, login

from main.models import Post, EnglishCategory, BanglaCategory, EnglishTag, BanglaTag


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
            tag_object.post.add(report_object)
            tag_object.save()
        else:
            new_tag_object = EnglishTag.objects.create(the_tag=i)
            new_tag_object.post.add(report_object)
            new_tag_object.save()

    for i in bangla_tag:
        tag_object = BanglaTag.objects.filter(the_tag=i)
        if tag_object:
            tag_object.post.add(report_object)
            tag_object.save()
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
        post_object.date_created = datetime.datetime.now()
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
        post_list = Post.objects.filter(is_approved=False, need_edit=True)
        return post_list
    else:
        return False


# return post object
def post_details(post_id):
    post_object = Post.objects.get(id=post_id)
    return post_object

