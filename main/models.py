from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.

class User(AbstractUser):
    user_type = models.IntegerField(default=0)


class Tag(models.Model):
    the_tag = models.CharField(max_length=255)


class Category(models.Model):
    the_category = models.CharField(max_length=255)


class Post(models.Model):
    reporter = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="reporter")
    moderator = models.ForeignKey(User, on_delete=models.DO_NOTHING, related_name="moderator", null=True, blank=True)
    english_image = models.ImageField(upload_to='post/english/')
    bangla_image = models.ImageField(upload_to='post/bangla/')
    english_content = models.TextField()
    bangla_content = models.TextField()
    english_title = models.CharField(max_length=255)
    bangla_title = models.CharField(max_length=255)
    english_tag = models.ForeignKey(Tag, null=True, on_delete=models.SET_NULL, related_name="english_tag")
    bangla_tag = models.ForeignKey(Tag, null=True, on_delete=models.SET_NULL, related_name="bangla_tag")
    english_category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL,
                                         related_name="english_category")
    bangla_category = models.ForeignKey(Category, null=True, on_delete=models.SET_NULL, related_name="bangla_category")
    is_approved = models.BooleanField(default=False)
    date_created = models.DateField()
    social_link = models.URLField()
    like_counter = models.IntegerField(default=0)
    view_counter = models.IntegerField(default=0)
