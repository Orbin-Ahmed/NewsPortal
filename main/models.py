from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    user_type = models.IntegerField(default=0)


class BanglaCategory(models.Model):
    the_category = models.CharField(max_length=255)


class EnglishCategory(models.Model):
    the_category = models.CharField(max_length=255)


class Post(models.Model):
    reporter = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name="reporter")
    moderator = models.OneToOneField(User, on_delete=models.DO_NOTHING, related_name="moderator", null=True, blank=True)
    image = models.ImageField(upload_to='post/')
    english_content = models.TextField()
    bangla_content = models.TextField()
    english_title = models.CharField(max_length=255)
    bangla_title = models.CharField(max_length=255)
    english_category = models.ForeignKey(EnglishCategory, null=True, on_delete=models.SET_NULL,
                                         related_name="english_category")
    bangla_category = models.ForeignKey(BanglaCategory, null=True, on_delete=models.SET_NULL,
                                        related_name="bangla_category")
    is_approved = models.BooleanField(default=False)
    need_edit = models.BooleanField(default=False)
    date_created = models.DateField(null=True, blank=True)
    like_counter = models.IntegerField(default=0)
    view_counter = models.IntegerField(default=0)


class BanglaTag(models.Model):
    the_tag = models.CharField(max_length=255)
    post = models.ManyToManyField(Post)


class EnglishTag(models.Model):
    the_tag = models.CharField(max_length=255)
    post = models.ManyToManyField(Post)
