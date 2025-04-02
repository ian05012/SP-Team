from django.shortcuts import redirect, render
from sp_app.models import Post, Tag
import json

def create_post(request):
    if not request.user.is_authenticated:
        return redirect('/account/login')

    if request.method == 'POST':
        new_post = Post()
        new_post.title = request.POST.get('title', '').strip()
        new_post.description = request.POST.get('description', '').strip()
        html_content = request.POST.get('content', '')
        print("Received HTML content:", html_content)
        new_post.content = html_content
        new_post.author = request.user
        new_post.post_type = request.POST.get('post_type', 'team')
        new_post.save()
        
        # 處理標籤
        tags_json = request.POST.get('tags', '[]')
        try:
            tag_names = json.loads(tags_json)
            for tag_name in tag_names:
                tag, created = Tag.objects.get_or_create(name=tag_name)
                new_post.tags.add(tag)
        except json.JSONDecodeError:
            pass
        return redirect('/')    

    return render(request, 'post/create_post.html')

def get_posts_list():
    return list(Post.objects.order_by('-id'))
