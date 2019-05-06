from django.db import models
from ..User import *
from ..Topic import *
#from ..SpecialTopic import *
from ..RollCall import *
from ..Comment import *

import uuid

# 文章立场统计


class Attitude(models.Model):
    Publisher = models.ForeignKey(
        User, to_field='id', default=0, on_delete=models.CASCADE, verbose_name='用户')
    Point = models.IntegerField(blank=False, verbose_name='立场代码')
    EditTime = models.DateTimeField(auto_now=True, verbose_name='时间')
    ObjectID = models.CharField(
        max_length=50, blank=True, verbose_name='ID')
    Type = models.CharField(
        max_length=30, blank=True, verbose_name='类型')

    class Meta:
        verbose_name = '赞/怼统计'
        # 末尾不加s
        verbose_name_plural = '5.赞/怼统计'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.Publisher.Nick

# 阅读IP统计


class ReadsIP(models.Model):
    """docstring for ArticleLikseIP"""
    IP = models.CharField(max_length=100, null=True,
                          blank=True, verbose_name='IP')
    EditDate = models.DateField(auto_now=True, verbose_name='时间')
    Type = models.CharField(
        max_length=30, default='T', blank=True, verbose_name='IP归入')
    ObjectID = models.CharField(
        max_length=100, null=True, blank=True, verbose_name='文章ID')

    class Meta:
        verbose_name = '访问统计'
        # 末尾不加s
        verbose_name_plural = '6.访问统计'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.IP

# 用户关注


class UserLink(models.Model):
    """docstring for UserLink"""
    UserBeLinked = models.ForeignKey(
        User, to_field='id', default='', blank=False, on_delete=models.CASCADE, verbose_name='被关注用户')
    UserLinking = models.ForeignKey(
        User, to_field='id', related_name='NickLinking', default='', blank=False, on_delete=models.CASCADE, verbose_name='关注用户')
    LinkTime = models.DateField(auto_now=True, verbose_name='时间')

    class Meta:
        verbose_name = '用户链接统计'
        verbose_name_plural = '7.用户链接统计'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.UserBeLinked.Nick


class Collection(models.Model):
    """docstring for Collection"""
    Publisher = models.ForeignKey(
        User, to_field='id', default=0, on_delete=models.CASCADE, verbose_name='用户名')
    Type = models.CharField(
        max_length=30, blank=True, default='T', verbose_name='收藏类型')
    ObjectID = models.CharField(
        max_length=12, blank=False, verbose_name='文章ID')
    CollectTime = models.DateField(auto_now=True, verbose_name='时间')

    class Meta:
        verbose_name = '收藏关注统计'
        verbose_name_plural = '8.收藏关注统计'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.Publisher.Nick


class PublisherList(models.Model):
    Publisher = models.ForeignKey(
        User, to_field='id', default=0, on_delete=models.CASCADE, verbose_name='用户名')
    Order = models.IntegerField(
        default=0, blank=False, verbose_name='顺序')

    class Meta:
        verbose_name = '推荐用户'
        # 末尾不加s
        verbose_name_plural = '9.推荐用户表'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.Publisher.Nick


class Notification(models.Model):

    ID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name='通知ID')
    Region = models.CharField(
        max_length=100, blank=False, default='', verbose_name='目标区域')
    ObjectID = models.CharField(
        max_length=100, blank=False, default='', verbose_name='目标ID')
    AnchorID = models.CharField(
        max_length=100, blank=False, default='', verbose_name='定位ID')
    SourceUser = models.ForeignKey(
        User, to_field='id', related_name='SourceUser', default=0, on_delete=models.CASCADE, verbose_name='通知者')
    TargetUser = models.ForeignKey(
        User, to_field='id', related_name='TargetUser', default=0, on_delete=models.CASCADE, verbose_name='被通知者')

    class Meta:
        verbose_name = '通知'
        # 末尾不加s
        verbose_name_plural = '10.通知中心'
        app_label = 'NTWebsite'

    def __str__(self):
        return str(self.ID)


class BlackList(models.Model):
    """docstring for blacklist"""

    ID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name='黑名单ID')
    Enforceder = models.ForeignKey(User, to_field='id', related_name='BlackList_User',
                                   on_delete=models.CASCADE, default=0, verbose_name='被添加用户')
    Handler = models.ForeignKey(
        User, to_field='id', related_name='Handler', null=True, on_delete=models.CASCADE, verbose_name='操作用户')

    class Meta:
        verbose_name = '黑名单记录'
        # 末尾不加s
        verbose_name_plural = '11.黑名单'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.ID


class TipOffBox(models.Model):
    """docstring for ComplaintBox"""

    ObjectID = models.CharField(
        max_length=100, blank=False, default='', verbose_name='对象ID')
    Type = models.CharField(
        max_length=30, blank=False, default='', verbose_name='对象类型')
    Content = models.CharField(
        max_length=100, blank=False, default='', verbose_name='举报内容')
    Publisher = models.ForeignKey(
        User, to_field='id', related_name='TipOffUser', null=True, on_delete=models.CASCADE, verbose_name='举报用户')
    EditDate = models.DateField(auto_now=True, verbose_name='编辑时间')

    class Meta:
        verbose_name = '举报统计'
        # 末尾不加s
        verbose_name_plural = '12.举报统计'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.Type + self.ObjectID
