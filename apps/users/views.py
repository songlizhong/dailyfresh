from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View


def register(request):
    """进入注册页面"""
    return render(request, 'register.html')


def do_register(request):
    """实现注册功能"""
    # 响应请求
    return HttpResponse('注册成功，进入登录页面')


class RegisterView(View):
    """注册视图"""
    def get(self, request):
        return render(request, 'register.html')

    def post(self, request):

    # 获取post请求

    # 校验参数合法
    # 判断参数不能为空
    # 判断两次输入的密码一致
    # 判断邮箱合法
    # 判断是否勾选用户协议

    # 处理业务：保存用户到数据库表
    # 判断用户是否存在
    # 修改用户状态为未激活

    # 发送激活邮件

