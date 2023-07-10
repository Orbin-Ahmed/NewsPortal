from django.contrib import admin

from main import models


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.User, UserAdmin)
