from django.urls import path
from . import views

urlpatterns = [
    path('post/create_post', views.create_post, name='create_post'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile, name='profile_with_username'),
    # 通知相關URL
    path('notifications/', views.get_notifications, name='get_notifications'),
    path('notifications/<int:notification_id>/read/', views.mark_notification_as_read, name='mark_notification_as_read'),
    path('notifications/<int:notification_id>/delete/', views.delete_notification, name='delete_notification'),
]
