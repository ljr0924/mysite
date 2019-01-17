import random
import time
from django.contrib import auth
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse

# Create your views here.
from login.models import Users


def regist(request):
    # get请求直接返回注册页面
    if request.method == 'GET':
        return render(request, 'login/regist.html')
    if request.method == 'POST':
        name = request.POST.get('name')
        password = request.POST.get('password')
        # 密码进行加密
        password = make_password(password)
        Users.objects.create(user_name=name, user_password=password)
        return HttpResponseRedirect('/login/')


def login(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        # 如果登陆成功，，绑定参数到cookie中，set_cookie
        name = request.POST.get('name')
        password = request.POST.get('password')
        # 查询用户是否在数据库中
        if User.objects.filter(username=name).exists():
            user = User.objects.get(username=name)
            if check_password(password, user.password):
                ticket = ''
                s = 'abcdefghijklmnopqrstuvwxyz'
                for i in range(15):
                    ticket += random.choice(s)
                now_time = int(time.time())
                ticket = 'TK' + ticket + str(now_time)
                # 绑定令牌到cookie中
                response = HttpResponseRedirect()
                # max_age 存活时间(秒)
                response.set_cookie('ticket', ticket, max_age=10000)
                # 存在服务端
                user.user_ticket = ticket
                user.save()
                return response
            else:
                # 密码错误
                return render(request, 'login/login.html', {'name': '密码错误'})
        else:
            # 用户不存在
            return render(request, 'login/login.html', {'name': '用户不存在'})