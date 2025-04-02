"""
URL configuration for sp_team project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from sp_app import views
from django.conf import settings
from django.conf.urls.static import static

handler404 = 'sp_app.views.handler404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('account/login/', views.login, name='login'),
    path('account/logout/', views.logout, name='logout'),
    path('account/register/', views.register, name='register'),
    path('post/create_post/create_post', views.create_post, name='create_post'),
    path('post/create_post/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('post/like/<int:post_id>/', views.toggle_like, name='toggle_like'),
    path('api/check_like/<int:post_id>/', views.check_like, name='check_like'),
    path('comment/delete/<int:post_id>/<int:comment_id>/', views.delete_comment, name='delete_comment'),
    path('explore/',views.explore, name='explore'),
    path('profile/', views.profile, name='profile'),

    path('profile/<str:username>/', views.profile, name='profile_with_username'),
    
]

# 在開發環境中添加媒體文件的URL
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
