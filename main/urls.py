from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('publish-news/', views.publish_news),
    path('edit-news/', views.edit_news),
]
