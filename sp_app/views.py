from django.shortcuts import render, redirect
from sp_app.backend import auth_system
from sp_app.models import Post


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


def create_team(request):
    if not request.user.is_authenticated:
        return redirect('/account/login')

    if request.method == 'POST':
        new_post = Post()
        new_post.title = request.POST.get('title', '').strip()
        new_post.content = request.POST.get('html_content', '').strip()
        new_post.author = request.user
        new_post.save()
        return redirect('/index')
    return render(request, 'post/post.html')
