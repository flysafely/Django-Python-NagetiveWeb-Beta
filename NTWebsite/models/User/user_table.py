from django.db import models
from django.contrib.auth.models import User, Group
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """docstring for UserTable"""

    Nick = models.CharField(max_length=20, verbose_name='昵称')
    Sex = models.CharField(
        max_length=3, verbose_name='性别', default="未公开", blank=True, null=False)
    Region = models.CharField(
        max_length=10, verbose_name='地区', blank=True, null=True, default="城市")
    Description = models.TextField(
        max_length=50, verbose_name='简介', blank=True, null=True, default="简介")
    Avatar = models.TextField(max_length=1000, verbose_name='头像URL',
                              default='DefaultLogo.jpg', blank=True, null=False)
    Constellation = models.CharField(
        max_length=10, blank=True, null=True, default='天蝎座', verbose_name='星座')

    FansCount = models.IntegerField(verbose_name='关注者数量', default=0)
    FocusCount = models.IntegerField(verbose_name='关注数量', default=0)
    TCount = models.IntegerField(verbose_name='文章发布数量', default=0)
    SCount = models.IntegerField(
        verbose_name='专题发布数量', default=0)
    RCount = models.IntegerField(verbose_name='点名数量', default=0)
    RRCount = models.IntegerField(verbose_name='点名回复数量', default=0)
    TRCount = models.IntegerField(verbose_name='文章评论数量', default=0)
    SRCount = models.IntegerField(
        verbose_name='专题评论数量', default=0)

    class Meta(AbstractUser.Meta):
        verbose_name = '用户'
        # 末尾不加s
        verbose_name_plural = '用户信息'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.Nick
# 用户信息表
