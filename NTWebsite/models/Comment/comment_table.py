from django.db import models
from ..User import *
import uuid
# 文章评论表


class CommentInfo(models.Model):
    """docstring for CommentInfo"""

    CommentID = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, verbose_name='评论ID')
    ObjectID = models.CharField(
        max_length=100, editable=True, default='', verbose_name='文章ID')
    Content = models.TextField(verbose_name="评论内容")
    Parent = models.CharField(
        max_length=100, editable=True, default='', null=True, blank=True, verbose_name='父评论ID')
    Like = models.IntegerField(verbose_name='赞', default="0")
    Type = models.CharField(
        max_length=30, editable=True, default='T', verbose_name='评论归属')
    Dislike = models.IntegerField(verbose_name='怼', default="0")
    EditDate = models.DateTimeField(auto_now=True, verbose_name='编辑时间')
    Publisher = models.ForeignKey(
        User, to_field='id', default=0, on_delete=models.CASCADE, verbose_name='用户名')

    class Meta:
        verbose_name = '评论统计'
        # 末尾不加s
        verbose_name_plural = '1.评论统计'
        app_label = 'NTWebsite'

    def __str__(self):
        return str(self.ObjectID)
