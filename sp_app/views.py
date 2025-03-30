from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F, Q
from sp_app.backend import auth_system, post_manager
from .models import Post
from django.utils import timezone
from django.core.paginator import Paginator

def explore(request):
    query = request.GET.get('search_query', '')
    post_list = Post.objects.all().order_by('created').reverse()
    
    if query:
        post_list = post_list.filter(
            Q(title__icontains=query) |
            Q(author__username__icontains=query) |
            Q(description__icontains=query)
        )
    
    paginator = Paginator(post_list, 10)  # 每頁顯示10個項目
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': query
    }
    return render(request, 'explore.html', context)
def post_detail(request, post_id):
    # 原子化更新觀看次數
    Post.objects.filter(id=post_id).update(watched=F('watched') + 1)
    
    # 重新取得更新後的資料
    post = get_object_or_404(Post, id=post_id)
    
    context = {
        'post': post,
        #'related_posts': Post.objects.filter(author=post.author).exclude(id=post_id)[:3]
    }
    return render(request, 'post/post.html', context)

# 首頁
def index(request):
    posts_list = post_manager.get_posts_list()
    if len(posts_list) >= 12:
        posts_list = posts_list[:12]
    return render(request, 'index.html', {'posts_list': posts_list})


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
