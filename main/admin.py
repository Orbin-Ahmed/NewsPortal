from django.contrib import admin

from main import models


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    pass

class PostAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.User, UserAdmin)

admin.site.register(models.Post, PostAdmin)
