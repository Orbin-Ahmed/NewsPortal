from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('reporter-dashboard/', views.reporter_dashboard),
]
