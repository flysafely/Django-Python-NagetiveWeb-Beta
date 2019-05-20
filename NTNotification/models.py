from django.db import models
from NTWebsite.models.User import *
from NTWebsite.models.Topic import *
# Create your models here.
class CommentNotification(models.Model):

    ID = models.CharField(
        primary_key=True, max_length=12,default='', editable=True, verbose_name='通知ID')
    Object = models.ForeignKey(TopicInfo, to_field='ObjectID', default=0, on_delete=models.CASCADE, verbose_name='文章')
    SourceUser = models.ForeignKey(
        User, to_field='id', related_name='SUser', default=0, on_delete=models.CASCADE, verbose_name='通知者')
    TargetUser = models.ForeignKey(
        User, to_field='id', related_name='TUser', default=0, on_delete=models.CASCADE, verbose_name='被通知者')

    class Meta:
        verbose_name = '评论通知'
        # 末尾不加s
        verbose_name_plural = '评论通知中心'
        app_label = 'NTNotification'

    def __str__(self):
        return str(self.ID)