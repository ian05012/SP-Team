from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import F, Q
from sp_app.backend import auth_system, post_manager
from .models import Post, Comment
from django.utils import timezone
from django.core.paginator import Paginator
from django import forms
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

def handler404(request, exception):
    return render(request, 'error/404.html', status=404)

def explore(request):
    query = request.GET.get('search_query', '')
    post_type = request.GET.get('type', 'all')
    post_list = Post.objects.all().order_by('created').reverse()
    
    if query:
        post_list = post_list.filter(
            Q(title__icontains=query) |
            Q(author__username__icontains=query) |
            Q(description__icontains=query)
        )
    
    if post_type and post_type != 'all':
        post_list = post_list.filter(post_type=post_type)
    
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
    
    # 檢查用戶是否已經按過讚
    user_liked = False
    if request.user.is_authenticated:
        from .models import UserLike
        user_liked = UserLike.objects.filter(user=request.user, post=post).exists()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': form,
        'comments_count': comments.count(),
        'user_liked': user_liked,
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


def create_post(request):
    return post_manager.create_post(request)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.user != post.author and not request.user.is_superuser:
        return JsonResponse({'error': '無操作權限'}, status=403)
    try:
        post.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': f'刪除失敗: {str(e)}'}, status=500)

@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    if request.user != comment.author and not request.user.is_superuser:
        return JsonResponse({'error': '無操作權限'}, status=403)
    try:
        comment.delete()
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'error': f'刪除失敗: {str(e)}'}, status=500)

@login_required
def toggle_like(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    from .models import UserLike
    
    # 檢查用戶是否已經按過讚
    like_exists = UserLike.objects.filter(user=request.user, post=post).exists()
    
    if like_exists:
        # 如果已經按過讚，則取消讚
        UserLike.objects.filter(user=request.user, post=post).delete()
        post.likes -= 1
        post.save()
        return JsonResponse({'liked': False, 'likes_count': post.likes})
    else:
        # 如果沒有按過讚，則添加讚
        UserLike.objects.create(user=request.user, post=post)
        post.likes += 1
        post.save()
        return JsonResponse({'liked': True, 'likes_count': post.likes})

def check_like(request, post_id):
    if not request.user.is_authenticated:
        return JsonResponse({'liked': False})
        
    post = get_object_or_404(Post, id=post_id)
    from .models import UserLike
    
    # 檢查用戶是否已經按過讚
    like_exists = UserLike.objects.filter(user=request.user, post=post).exists()
    
    return JsonResponse({'liked': like_exists})
@login_required
def profile(request, username=None):
    """
    用戶個人資料頁面 - 需要登入才能訪問
    """
    from django.contrib.auth import get_user_model
    User = get_user_model()
    
    if username:
        # 查看特定用戶的資料
        user_data = get_object_or_404(User, username=username)
        is_own_profile = request.user == user_data
    else:
        # 查看自己的資料
        user_data = request.user
        is_own_profile = True
    
    # 嚴格檢查：只有自己的個人資料頁面才能進入編輯模式
    edit_mode = False
    if request.GET.get('edit', 'false').lower() == 'true':
        # 必須是自己的資料才能編輯
        if is_own_profile:
            edit_mode = True
        else:
            # 如果嘗試編輯他人資料，重定向到查看模式並顯示錯誤訊息
            from django.urls import reverse
            from django.contrib import messages
            messages.error(request, '您沒有權限編輯其他用戶的資料')
            return redirect(reverse('profile_with_username', kwargs={'username': username}))
    
    # 再次檢查：確保只有本人才能提交表單更新資料
    if request.method == 'POST':
        # 必須是自己的資料
        if not is_own_profile:
            from django.http import HttpResponseForbidden
            return HttpResponseForbidden("您沒有權限編輯此用戶的資料")
            
        # 只有通過權限檢查才能更新資料
        # 處理表單提交
        user_data.username = request.POST.get('username', user_data.username)
        user_data.email = request.POST.get('email', user_data.email)
        user_data.custom_site_name = request.POST.get('custom_site_name', '')
        user_data.custom_site_url = request.POST.get('custom_site_url', '')
        user_data.name = request.POST.get('name', '')
        user_data.gender = request.POST.get('gender', '')
        user_data.birthday = request.POST.get('birthday', None)
        user_data.description = request.POST.get('description', '')
        user_data.github = request.POST.get('github', '')
        user_data.instagram = request.POST.get('instagram', '')
        user_data.line = request.POST.get('line', '')
        
        # 處理頭像上傳
        if 'avatar' in request.FILES:
            user_data.avatar = request.FILES['avatar']
        
        user_data.save()
        from django.contrib import messages
        messages.success(request, '讚喔! 你現在煥然一新了!')
        from django.urls import reverse
        return redirect(reverse('profile'))
    
    # 獲取用戶發布的文章
    team_posts = user_data.post_set.filter(post_type='team').order_by('-created')
    project_posts = user_data.post_set.filter(post_type='project').order_by('-created')
    experience_posts = user_data.post_set.filter(post_type='experience').order_by('-created')
    
    context = {
        'user_data': user_data,
        'is_own_profile': is_own_profile,
        'edit_mode': edit_mode,
        'team_posts': team_posts,
        'project_posts': project_posts,
        'experience_posts': experience_posts
    }
    return render(request, 'profile/profile.html', context)

def handler404(request, exception):
    """
    處理404錯誤
    """
    return render(request, 'error/404.html', status=404)

def handler500(request):
    """
    處理500錯誤
    """
    return render(request, 'error/500.html', status=500)