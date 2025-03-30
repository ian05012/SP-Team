from django.urls import path
from . import views
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views

app_name = 'sp_app'

urlpatterns = [
    # 文章詳細頁面路由
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    
    # 現有路由保留區 (從 migration 檔案判斷已有帳戶系統)
    path('accounts/login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login'),
    path('accounts/register/', views.register, name='register'),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
]
