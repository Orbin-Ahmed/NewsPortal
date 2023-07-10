from django.contrib.auth import authenticate, login

from main.models import Post


# login call -> returns None if not authenticated

def user_login(request, username, password):
    user = authenticate(username, password)
    if user is not None:
        login(request, user)
        return user
    else:
        return None


def post_report(request, bangla_title, bangla_content, bangla_tag, bangla_category, bangla_image,
                english_title, english_content, english_tag, english_category, english_image,
                social_link):
    report_object = Post.objects.create(reporter=request.user,
                                        english_image=english_image,
                                        bangla_image=bangla_image,
                                        english_title=english_title,
                                        bangla_title=bangla_title,
                                        english_content=english_content,
                                        bangla_content=bangla_content,
                                        english_category=english_category,
                                        bangla_category=bangla_category,
                                        social_link=social_link)

    return report_object
