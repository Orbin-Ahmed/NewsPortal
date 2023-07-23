from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [path('', views.landing_page),
               path('today-news/', views.today_news),
               path('other-category-news/', views.dynamic_news),
               path('category-news/<category_name>/', views.category_news),
               path('previous-news/<p_month>/<p_date>/<p_year>/', views.previous_date_news),
               path('details-news/<post_id>/<category_name>/', views.details_news),
               path('like-news/<post_id>/', views.like_news_counter),
               path('search-news/<keywords>/', views.search_news),
               path('login/', views.login),
               path('user-logout/', views.user_logout),
               path('publish-news/', views.publish_news),  # Reporter
               path('edit-news/', views.edit_news),  # Reporter
               path('edit-news-redirect/<post_id>/', views.edit_news_redirect),  # Reporter
               path('pending-news/', views.pending_news),  # Moderator
               path('all-news/', views.all_news),  # Moderator
               path('trendy-news/', views.trendy_news),  # Moderator
               path('rolling-headlines/', views.rolling_headlines),  # Moderator
               path('reporter/', views.reporter_status),  # Moderator
               path('focus-news/', views.focus_news),  # Moderator
               path('news-details/<news_id>/', views.news_details),  # Moderator
               path('admin-news/', views.admin_news),  # Admin
               path('moderator/', views.moderator_status),  # Admin
               path('admin-news-details/<news_id>/', views.admin_news_details),  # Admin
               path('reporter-suspend/', views.reporter_suspend),  # Admin
               path('approve-post/<post_id>/', views.approve_post_view),  # Function start
               path('edit-post/<post_id>/', views.edit_post_view),
               path('delete-news/<post_id>/', views.delete_news_view),
               path('delete-news-mod/<post_id>/', views.delete_news_mod_view),
               path('suspend-user/<username>/', views.suspend_user_view),
               path('suspend-user-mod/<username>/', views.suspend_mod_user_view),
               path('add-to-something/<post_id>/<post_type>/', views.add_to_something),
               path('remove-from-something/<post_id>/<post_type>/', views.remove_from_something),
               path('password-update/', views.password_update),
               ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
