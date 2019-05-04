from django.db import models

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from imagekit.processors import SmartResize

from ckeditor_uploader.fields import RichTextUploadingField
from ..User import *

import uuid


class SpecialTopicInfo(models.Model):
    """docstring for SpecialTopicInfo"""
    STI_ID = models.CharField(
        primary_key=True, auto_created=True, max_length=12, default=str(uuid.uuid4())[-12:], verbose_name='专题ID')
    STI_Title = models.CharField(
        max_length=35, unique=True, verbose_name='专题标题')
    STI_Cover = models.ImageField(
        upload_to='Cover', blank=False, verbose_name='封面图', default='')
    STI_Cover_210x140 = ImageSpecField(source='STI_Cover', processors=[
                                       SmartResize(210, 140)], format='JPEG', options={'quality': 95})
    STI_Cover_SR965x300 = ImageSpecField(source='STI_Cover', processors=[
                                         SmartResize(965, 300)], format='JPEG', options={'quality': 95})
    STI_EditDate = models.DateField(auto_now=True, verbose_name='发布时间')
    STI_Publisher = models.ForeignKey(
        User, to_field='username', related_name='Publisher', on_delete=models.CASCADE, verbose_name='发布者')
    STI_Type = models.CharField(
        max_length=10, default='article', verbose_name='专题类型')
    STI_Follower = models.IntegerField(
        default=0, blank=False, verbose_name='关注量')
    STI_Hot = models.IntegerField(default=10, blank=False, verbose_name='热度')
    STI_Abstract = models.CharField(
        max_length=30, blank=False, default='', verbose_name='简介')
    STI_Content = RichTextUploadingField(
        null=True, blank=True, config_name='admin', verbose_name='正文')
    STI_Comment = models.IntegerField(verbose_name='评论数', default=0)

    class Meta:
        verbose_name = '专题'
        # 末尾不加s
        verbose_name_plural = '**3**专题信息**3**'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.STI_Title


# 专题评论表
