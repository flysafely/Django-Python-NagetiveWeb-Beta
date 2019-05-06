from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from imagekit.processors import SmartResize
from ckeditor_uploader.fields import RichTextUploadingField
from ..User import *
import uuid
import django.utils.timezone as timezone

class TopicThemeInfo(models.Model):
    """docstring for TopicThemeInfo"""
    Name = models.CharField(
        max_length=10, primary_key=True, verbose_name='标签名称')

    class Meta:
        verbose_name = '标签'
        # 末尾不加s
        verbose_name_plural = '16.文章标签'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.Name

# 品类信息表


class TopicCategoryInfo(models.Model):

    Name = models.CharField(primary_key=True,
                            max_length=10, null=False, blank=False, verbose_name='品类名称')
    SVG = models.TextField(max_length=1000, verbose_name='图标SVG')

    class Meta:
        verbose_name = '类目'
        # 末尾不加s
        verbose_name_plural = '17.文章分类'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.Name


# 文章信息表.

class TopicInfo(models.Model):
    """docstring for TopicInfo"""
    ObjectID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name='文章ID')
    # ID = models.CharField(
    #    primary_key=True, auto_created=True, max_length=12, default=str(uuid.uuid4())[-12:], verbose_name='文章ID')
    Title = models.CharField(
        max_length=35, unique=True, verbose_name='文章标题')
    Description = models.TextField(max_length=140, verbose_name='文章描述')
    Publisher = models.ForeignKey(
        User, to_field='id', default=0, on_delete=models.CASCADE, verbose_name='用户名')
    Theme = models.ManyToManyField(
        TopicThemeInfo, verbose_name='文章主题标签', related_name='Topic')
    Category = models.ForeignKey(
        TopicCategoryInfo, to_field='Name', on_delete=models.CASCADE, null=True, verbose_name='文章类别')

    Content = RichTextUploadingField(
        null=True, blank=True, config_name='admin', verbose_name='文章正文')
    Type = models.CharField(
        max_length=20, default='Topic', verbose_name='文章类型')
    # SpecialTopic字段
    Cover = models.ImageField(
        upload_to='Cover', blank=True, verbose_name='封面', default='')
    Cover_210x140 = ImageSpecField(processors=[
        SmartResize(210, 140)], format='JPEG', options={'quality': 95})
    Cover_SR965x300 = ImageSpecField(processors=[
        SmartResize(965, 300)], format='JPEG', options={'quality': 95})

    Recommend = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, default=0, verbose_name='推荐度')
    Like = models.IntegerField(verbose_name='赞', default=0)
    Dislike = models.IntegerField(verbose_name='怼', default=0)
    Hot = models.IntegerField(verbose_name='热度', default=10)
    Comment = models.IntegerField(verbose_name='评论数', default=0)
    Share = models.IntegerField(
        default=0, blank=False, verbose_name='分享')
    Collect = models.IntegerField(
        default=0, blank=False, verbose_name='关注或收藏量')
    EditTime = models.DateTimeField(auto_now=True, verbose_name='编辑时间')
    CreateTime = models.DateTimeField(default=timezone.now, editable=True,verbose_name='添加时间')

    class Meta:
        verbose_name = '文章内容'
        # 末尾不加s
        verbose_name_plural = '18.文章内容'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.Title
