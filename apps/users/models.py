from django.contrib.auth.models import AbstractUser
from django.db import models
from itsdangerous import TimedJSONWebSignatureSerializer

from tinymce.models import HTMLField

from dailyfresh import settings
from utils.models import BaseModel


class User(BaseModel, AbstractUser):
    """用户模型类"""

    class Meta(object):
        db_table = 'df_user'

    def generate_active_token(self):
        """生成加密数据"""
        # 参数1：密钥，不能公开，用于解密
        # 参数２：加密数据失效时间(1天)
        serializer = TimedJSONWebSignatureSerializer(
            settings.SECRET_KEY, 3600 * 24)
        # 要加密的数据此处传入了一个字典，其格式是可以自定义的
        # 只要包含核心数据 用户id 就可以了，self.id即当前用户对象的id
        token = serializer.dumps({'confirm': self.id})
        # 类型转换： bytes -> str
        return token.decode()


class TestModel(BaseModel):
    """测试用"""
    name = models.CharField(max_length=20)
    # 商品详情，使用第三方的：HTMLField
    goods_detail = HTMLField(default='', verbose_name='商品详情')
