# 添加到celery服务器所在电脑的项目中,
# 让celery执行发送邮件前初始化django环境


from celery.app.base import Celery
from django.core.mail import send_mail
from dailyfresh import settings

app = Celery('dailyfresh', broker='redis://127.0.0.1:6379/1')


@app.task
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
