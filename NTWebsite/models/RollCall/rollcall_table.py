from django.db import models
from ..User import *
import uuid


class RollCallInfo(models.Model):
    """docstring for RollCallInfo"""
    ObjectID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name='点名ID')
    Title = models.CharField(
        max_length=35, unique=True, verbose_name='点名标题')
    EditDate = models.DateTimeField(auto_now=True, verbose_name='编辑时间')
    Publisher = models.ForeignKey(
        User, to_field='id', related_name='Publisher_User', default=0, on_delete=models.CASCADE, verbose_name='点名者')
    Target = models.ForeignKey(
        User, to_field='id', related_name='Target_User', default=0, on_delete=models.CASCADE, verbose_name='被点名者')
    LeftLike = models.IntegerField(
        default=0, blank=False, verbose_name='点名者支持数')
    RightLike = models.IntegerField(
        default=0, blank=False, verbose_name='被点名者支持数')
    Hot = models.IntegerField(
        default=0, blank=False, verbose_name='点名热度')
    Collect = models.IntegerField(
        default=0, blank=False, verbose_name='关注度')
    Comment = models.IntegerField(
        default=0, blank=False, verbose_name='活跃度')
    Share = models.IntegerField(
        default=0, blank=False, verbose_name='分享')
    Recommend = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, default=0, verbose_name='推荐度')

    class Meta:
        verbose_name = '点名信息'
        # 末尾不加s
        verbose_name_plural = '**4**点名基础信息**4**'
        app_label = 'NTWebsite'

    def __str__(self):
        return str(self.ObjectID)


class RollCallDialogue(models.Model):
    ObjectID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name='对话ID')
    RollCallID = models.ForeignKey(
        RollCallInfo, to_field='ObjectID', default='', on_delete=models.CASCADE, verbose_name='点名ID')
    EditDate = models.DateTimeField(auto_now=True, verbose_name='编辑时间')
    Publisher = models.ForeignKey(
        User, to_field='id', related_name='RollCallDialogue_User', default=0, on_delete=models.CASCADE, verbose_name='发布者')
    Display = models.CharField(max_length=10,default='',verbose_name='显示位置')
    Content = models.CharField(
        max_length=30, default='', blank=False, verbose_name='回复内容')

    class Meta:
        verbose_name = '对话记录'
        # 末尾不加s
        verbose_name_plural = '**4**点名对话明细**4**'
        app_label = 'NTWebsite'

    def __str__(self):
        return str(self.RollCallID)
