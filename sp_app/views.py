from django.shortcuts import render, redirect
from sp_app.backend import auth_system, post_manager


# 首頁
def index(request):
    posts_list = post_manager.get_posts_list()
    if len(posts_list) >= 8:
        new_posts_list = posts_list[-9:-1]
    else:
        new_posts_list = posts_list[-len(posts_list):-1]
    print(new_posts_list)
    return render(request, 'index.html', {'posts_list': new_posts_list})


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
    return post_manager.create_team(request)
