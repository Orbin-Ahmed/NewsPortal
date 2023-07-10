from django.contrib import admin

from main import models


# Register your models here.

class UserAdmin(admin.ModelAdmin):
    pass


class PostAdmin(admin.ModelAdmin):
    pass


class BanglaTagAdmin(admin.ModelAdmin):
    pass


class EnglishTagAdmin(admin.ModelAdmin):
    pass


class BanglaCategoryAdmin(admin.ModelAdmin):
    pass


class EnglishCategoryAdmin(admin.ModelAdmin):
    pass


admin.site.register(models.User, UserAdmin)
admin.site.register(models.BanglaTag, BanglaTagAdmin)
admin.site.register(models.EnglishTag, EnglishTagAdmin)
admin.site.register(models.BanglaCategory, BanglaCategoryAdmin)
admin.site.register(models.EnglishCategory, EnglishCategoryAdmin)
admin.site.register(models.Post, PostAdmin)
