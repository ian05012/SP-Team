from django.shortcuts import redirect, render

from sp_app.models import Post


def create_team(request):
    if not request.user.is_authenticated:
        return redirect('/account/login')

    if request.method == 'POST':
        new_post = Post()
        new_post.title = request.POST.get('title', '').strip()
        new_post.description = request.POST.get('description', '').strip()
        new_post.content = request.POST.get('html_content', '').strip()
        new_post.author = request.user
        new_post.save()
        return redirect('/index')
    return render(request, 'post/create_post.html')

def get_posts_list():
    return list(Post.objects.order_by('-id'))

