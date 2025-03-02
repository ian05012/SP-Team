from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
class user(AbstractUser):

    name = models.TextField(default="")
    gender = models.TextField(default="男")
    desription = models.TextField(default="這個人很懶，還沒留下任何東西~")
    skill = models.TextField(default="什麼都不會")
    birthday = models.DateTimeField(auto_now_add=True)
    headshot = models.TextField(default="")
    education = models.TextField(default="")
    created = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'username'
    def __str__(self):
        return self.username

class Post(models.Model):
    title = models.TextField(default="")
    content = models.TextField(default="")
    author = models.ForeignKey(user, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
