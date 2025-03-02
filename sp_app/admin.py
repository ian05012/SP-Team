from django.contrib import admin
# Register your models here.
from django.contrib import admin
from sp_app.models import user
from .models import Article

admin.site.register(user)


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title',)