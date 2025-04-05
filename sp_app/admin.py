from django.contrib import admin
# Register your models here.
from django.contrib import admin
from sp_app.models import user, Post,Announcement

admin.site.register(user)
admin.site.register(Post)
admin.site.register(Announcement)