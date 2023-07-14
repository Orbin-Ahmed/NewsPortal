from django.urls import path
from . import views

urlpatterns = [
    path('', views.login),
    path('publish-news/', views.publish_news),
    path('edit-news/', views.edit_news),
    path('pending-news/', views.pending_news),
    path('all-news/', views.all_news),
    path('trendy-news/', views.trendy_news),
    path('rolling-headlines/', views.rolling_headlines),
    path('reporter/', views.reporter_status),
    path('focus-news/', views.focus_news),
    path('news-details/<news_id>/', views.news_details),
    path('admin-news/', views.admin_news),
    path('moderator/', views.moderator_status),
    path('reporter-suspend/', views.reporter_suspend),
    path('approve-post/<post_id>/', views.approve_post_view),  # Function start
]
