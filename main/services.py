from django.contrib.auth import authenticate, login

from main.models import Post, EnglishCategory, BanglaCategory, EnglishTag, BanglaTag


# login call -> returns None if not authenticated

def user_login(request, username, password):
    user = authenticate(request, username=username, password=password)
    if user is not None:
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
        post_object.save()
        return True
    else:
        return None

