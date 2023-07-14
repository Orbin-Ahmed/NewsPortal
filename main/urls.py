from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('publish-news/', views.publish_news),  # Reporter
    path('edit-news/', views.edit_news),  # Reporter
    path('pending-news/', views.pending_news),  # Moderator
    path('all-news/', views.all_news),  # Moderator
    path('trendy-news/', views.trendy_news),  # Moderator
    path('rolling-headlines/', views.rolling_headlines),  # Moderator
    path('reporter/', views.reporter_status),  # Moderator
    path('focus-news/', views.focus_news),  # Moderator
    path('news-details/<news_id>/', views.news_details),  # Moderator
    path('admin-news/', views.admin_news),  # Admin
    path('moderator/', views.moderator_status),  # Admin
    path('reporter-suspend/', views.reporter_suspend),  # Admin
    path('approve-post/<post_id>/', views.approve_post_view),  # Function start
    path('password-update/', views.password_update),
]
