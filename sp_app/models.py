from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, username, password=None, **extra_fields):
        if not username:
            raise ValueError('用戶名必須設置')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, password, **extra_fields)

class user(AbstractUser):

    name = models.TextField(default="")
    gender = models.TextField(default="男")
    description = models.TextField(default="這個人很懶，還沒留下任何東西~")
    github = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    line = models.TextField(blank=True, null=True)
    custom_site_name = models.TextField(blank=True, null=True)
    custom_site_url = models.URLField(blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    birthday = models.DateTimeField(auto_now_add=True)
    created = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Post(models.Model):
    # 文章類型選項
    TYPE_CHOICES = (
        ('team', '團隊招募'),
        ('project', '作品發布'),
        ('experience', '心得分享'),
    )
    
    title = models.TextField(default="")
    description = models.TextField(default="")
    content = models.TextField(default="")
    author = models.ForeignKey(user, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)
    watched = models.IntegerField(default=0)
    tags = models.ManyToManyField(Tag, blank=True)
    post_type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='team')

    def someone_watched(self):
       self.watched+=1

    def __str__(self):
        return self.title

class UserLike(models.Model):
    user = models.ForeignKey(user, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'post')  # 確保一個用戶只能對一篇文章按一次讚

class Comment(models.Model):
    content = models.TextField(default="")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(user, on_delete=models.CASCADE)  # 注意小寫user模型
    created = models.DateTimeField(auto_now_add=True)  # 字段名與Post一致

    class Meta:
        ordering = ['-created']  # 使用相同時間字段名稱

    def __str__(self):
        return f"{self.author.username}的留言"
