from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F, Q
from sp_app.backend import auth_system, post_manager
from .models import Post, Comment
from django.utils import timezone
from django.core.paginator import Paginator
from django import forms

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
from django.contrib.auth.decorators import login_required
from .models import Comment
from django.http import HttpResponseRedirect

class CommentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 3,
        'placeholder': '輸入您的留言...',
        'class': 'comment-input'
    }), label='')

def post_detail(request, post_id):
    # 原子化更新觀看次數
    Post.objects.filter(id=post_id).update(watched=F('watched') + 1)
    post = get_object_or_404(Post, id=post_id)
    
    # 處理留言提交
    if request.method == 'POST':
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/account/login')
            
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                content=form.cleaned_data['content'],
                post=post,
                author=request.user
            )
            return HttpResponseRedirect(request.path)
    
    # 取得排序後的留言
    comments = post.comments.all()
    form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': form,
        'comments_count': comments.count(),
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
