from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from .models import BoardModel
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy

# Create your views here.


# 新規登録
def signupfunc(request):
    # # Userデータを変数に入れる
    if request.method == 'POST':
        # フォームからのデータ受け取り
        username = request.POST['username']
        password = request.POST['password']
        # 登録されているデータの重複の有り無し
        try:
            # 重複してない場合
            user = User.objects.create_user(username, '', password)
            return render(request, 'signup.html', {'some':500})
        except IntegrityError:
            # 重複した場合
            return render(request, 'signup.html', {'error':'このユーザーは既に登録されています'})
    return render(request, 'signup.html', {'some':500})

# ログイン
def loginfunc(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('list')
        else:
            return render(request, 'login.html' ,{})
    return render(request, 'login.html' ,{})

# 投稿一覧
@login_required
def listfunc(request):
    object_list = BoardModel.objects.all()
    
    return render(request, 'list.html', {'object_list':object_list})

# ログアウト
def logoutfunc(request):
    logout(request)
    return redirect('login')

# 詳細画面
@login_required
def detailfunc(request, pk):
    object = get_object_or_404(BoardModel, pk=pk)
    return render(request, 'detail.html', {'object':object})

# いいね機能
def goodfunc(request, pk):
    object = BoardModel.objects.get(pk=pk)
    object.good = object.good + 1
    object.save()
    return redirect('list')

# 既読機能
def readfunc(request, pk):
    object = BoardModel.objects.get(pk=pk)
    # ユーザー判定
    username = request.user.get_username()
    if username in object.readtext:
        return redirect('list')
    else:
        object.read = object.read + 1
        object.readtext = object.readtext + ', ' + username
        object.save()
        return redirect('list')
    
# 投稿機能
class BoardCreate(CreateView):
    template_name = 'create.html'
    model = BoardModel
    fields = ('title', 'content', 'author', 'sns_image')
    success_url = reverse_lazy('list/')