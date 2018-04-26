import re
from time import sleep

from django.core.mail import send_mail
from django.db.utils import IntegrityError
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from itsdangerous import TimedJSONWebSignatureSerializer, SignatureExpired

from apps.users.models import User
from celery_tasks.tasks import send_active_mail
from dailyfresh import settings


def register(request):
    """进入注册页面"""
    return render(request, 'register.html')


class RegisterView(View):
    """注册视图"""

    def get(self, request):
        """进入注册界面 """
        return render(request, 'register.html')

    def post(self, request):
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

        # 处理业务： 保存用户到数据库表中
        # django提供的方法，会对密码进行加密
        user = None
        try:
            user = User.objects.create_user(username, email, password)  # type: User
            # 修改用户状态为未激活
            user.is_active = False
            user.save()
        except IntegrityError:
            # 判断用户是否存在
            return render(request, 'register.html', {'errmsg': '用户已存在'})

        # user = User.objects.get(id=19)
        print(type(user), user)
        # todo: 发送激活邮件
        token = user.generate_active_token()
        # 同步发送：会阻塞
        # RegisterView.send_active_mail(username, email, token)
        # 使用celery异步发送：不会阻塞
        # 会保存方法名参数等到Redis数据库中
        self.send_active_mail.delay(username, email, token)

        # 响应请求
        return HttpResponse('注册成功，进入登录界面')

    @staticmethod
    def send_active_mail(username, email, token):
        """发送激活邮件"""
        subject = '天天生鲜激活邮件'  # 标题，必须指定
        message = ''  # 正文
        from_email = settings.EMAIL_FROM  # 发件人
        recipient_list = [email]  # 收件人
        # 正文 （带有html样式）
        html_message = ('<h3>尊敬的%s：感谢注册天天生鲜</h3>'
                        '请点击以下链接激活您的帐号:<br/>'
                        '<a href="http://127.0.0.1:8000/users/active/%s">'
                        'http://127.0.0.1:8000/users/active/%s</a>'
                        ) % (username, token, token)

        send_mail(subject, message, from_email, recipient_list,
                  html_message=html_message)


class ActiveView(View):
    def get(self, request, token: str):
        """
        激活注册用户
        :param request:
        :param token: 对{'confirm':用户id}字典进行加密后的结果
        :return:
        """
        # 解密数据，得到字典
        dict_data = None
        try:
            s = TimedJSONWebSignatureSerializer(
                settings.SECRET_KEY, 3600 * 24)
            dict_data = s.loads(token.encode())  # type: dict
        except SignatureExpired:
            # 激活链接已经过期
            return HttpResponse('激活链接已经过期')

        # 获取用id
        user_id = dict_data.get('confirm')

        # 激活用户，修改表字段is_active=True
        User.objects.filter(id=user_id).update(is_active=True)

        # 响应请求
        return HttpResponse('激活成功，进入登录界面')
