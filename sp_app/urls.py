from django.urls import path
from . import views

urlpatterns = [
    path('post/create_post', views.create_post, name='create_post'),
    path('profile/', views.profile, name='profile'),
    path('profile/<str:username>/', views.profile, name='profile_with_username'),
]
