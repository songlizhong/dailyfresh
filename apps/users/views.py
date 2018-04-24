import re
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View


def register(request):
    """进入注册页面"""
    return render(request, 'register.html')


def do_register(request):
    """实现注册功能 """

    # 获取post请求参数
    username = request.POST.get('username')
    password = request.POST.get('password')
    password2 = request.POST.get('password2')
    email = request.POST.get('email')
    allow = request.POST.get('allow')  # 用户协议， 勾选后得到：on

    # todo: 校验参数合法性
    # 判断参数不能为空
    if not all([username, password, password2, email]):
        # return redirect('/users/register')
        return render(request, 'register.html', {'errmsg': '参数不能为空'})

    # 判断两次输入的密码一致
    if password != password2:
        return render(request, 'register.html', {'errmsg': '两次输入的密码不一致'})

    # 判断邮箱合法
    if not re.match('^[a-z0-9][\w.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$', email):
        return render(request, 'register.html', {'errmsg': '邮箱不合法'})

    # 判断是否勾选用户协议(勾选后得到：on)
    if allow != 'on':
        return render(request, 'register.html', {'errmsg': '请勾选用户协议'})

    # 响应请求
    return HttpResponse('注册成功，进入登录界面')
