# 登入
from django.contrib import auth
from django.contrib.auth import authenticate
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.template import loader

from sp_app.models import user


def login(request):
    error = None  # 預設位無錯誤
    if request.method == 'POST':
        username = request.POST.get('account', '').strip()
        password = request.POST.get('password', '').strip()

        # 嘗試驗證用戶
        login_user = authenticate(request, username=username, password=password)
        if login_user and login_user.is_active:
            # 登入成功
            auth.login(request, login_user)
            return redirect('/')
        else:
            # 驗證失敗，設定錯誤訊息，停留在登入頁面
            error = '帳號或密碼錯誤！'

    # 如果用戶已驗證，則不需要再顯示登入頁
    if request.user.is_authenticated:
        return redirect('/')

    # 傳遞錯誤訊息到模板
    return HttpResponse(loader.get_template("../templates/account/login.html").render({'error': error}, request))



# 註冊
import random
import os
import hashlib
from django.conf import settings
from django.core.files import File

def register(request):
    info_message = None  # 預設為無提示訊息
    if request.method == 'POST':
        account = request.POST.get('account', '').strip()
        password = request.POST.get('password', '').strip()

        # 檢查帳號是否已存在
        if user.objects.filter(username=account).exists():
            # 帳號存在，設定提示訊息
            info_message = '帳號已存在，請前往登入！'
        else:
            # 創建新用戶
            new_user = user()
            new_user.username = account
            new_user.set_password(password)
            
            # 隨機選擇一個預設頭像
            default_avatars = ['default1.png', 'default2.png', 'default3.png']
            random_avatar = random.choice(default_avatars)
            avatar_path = os.path.join(settings.MEDIA_ROOT, random_avatar)
            
            # 確保檔案存在
            if os.path.exists(avatar_path):
                # 設置用戶頭像
                with open(avatar_path, 'rb') as f:
                    new_user.avatar.save(random_avatar, File(f), save=False)
            
            new_user.save()
            info_message = '註冊成功，請登入您的帳號！'


    return render(request, 'account/register.html', {'info_message': info_message})


# 登出
def logout(request):
    auth.logout(request)
    return redirect('/')
