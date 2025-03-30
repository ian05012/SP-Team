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
    objects = UserManager()
    name = models.TextField(default="")
    gender = models.TextField(default="男")
    description = models.TextField(default="這個人很懶，還沒留下任何東西~")
    skill = models.TextField(default="什麼都不會")
    birthday = models.DateTimeField(auto_now_add=True)
    headshot = models.TextField(default="")
    education = models.TextField(default="")
    created = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username

class Post(models.Model):
    title = models.TextField(default="")
    description = models.TextField(default="")
    content = models.TextField(default="")
    author = models.ForeignKey(user, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    likes = models.IntegerField(default=0)
    watched = models.IntegerField(default=0)

    def someone_watched(self):
       self.watched+=1

    def __str__(self):
        return self.title
