from django.contrib.auth.models import AbstractUser
from django.db import models

from tinymce.models import HTMLField
from utils.models import BaseModel


class User(BaseModel, AbstractUser):
    """用户模型类"""
    class Meta(object):
        db_table = 'df_user'


class TestModel(BaseModel):
    """测试用"""
    name = models.CharField(max_length=20)

    # 商品详情，使用第三方的：HTMLField
    goods_detail = HTMLField(default='', verbose_name='商品详情')














