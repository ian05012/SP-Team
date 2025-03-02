from django.shortcuts import render, redirect
from sp_app.backend import auth_system

# 首頁
def index(request):
    return render(request, 'index.html')


# 登入
def login(request):
    return auth_system.login(request)

# 註冊
def register(request):
   return auth_system.register(request)

# 登出
def logout(request):
    return auth_system.logout(request)

def createTeam(request):
    return render(request, 'post/post.html')