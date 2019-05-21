from django.db import models
from NTWebsite.models.User import *
from NTWebsite.models.Topic import *
from NTWebsite.models.OperationRecord import *
# Create your models here.
class CommentNotification(models.Model):

    ID = models.CharField(
        primary_key=True, max_length=12,default='', editable=True, verbose_name='通知ID')
    Type = models.CharField(max_length=10,default='Comment',verbose_name='通知类型')
    Object = models.ForeignKey(CommentInfo, to_field='ObjectID', default=0, on_delete=models.CASCADE, verbose_name='文章')

    class Meta:
        verbose_name = '评论通知'
        # 末尾不加s
        verbose_name_plural = '评论通知中心'
        app_label = 'NTNotification'

    def __str__(self):
        return str(self.ID)

class RollCallNotification(models.Model):

    ID = models.CharField(
        primary_key=True, max_length=12,default='', editable=True, verbose_name='通知ID')
    Type = models.CharField(max_length=10,default='Comment',verbose_name='通知类型')
    RCObject = models.ForeignKey(RollCallInfo, to_field='ObjectID', default=0, null=True,on_delete=models.CASCADE, verbose_name='点名')
    RCDObject = models.ForeignKey(RollCallDialogue, to_field='ObjectID', default=0, null=True,on_delete=models.CASCADE, verbose_name='点名对话')

    class Meta:
        verbose_name = '点名通知'
        # 末尾不加s
        verbose_name_plural = '点名通知中心'
        app_label = 'NTNotification'

    def __str__(self):
        return str(self.ID)

class LinkNotification(models.Model):

    ID = models.CharField(
        primary_key=True, max_length=12,default='', editable=True, verbose_name='通知ID')
    ObjectID = models.ForeignKey(UserLink, to_field="id",default=0, null=True,on_delete=models.CASCADE, verbose_name='被关注者')

    class Meta:
        verbose_name = '关注通知'
        # 末尾不加s
        verbose_name_plural = '关注通知中心'
        app_label = 'NTNotification'

    def __str__(self):
        return str(self.ID)

class PublishNotification(models.Model):

    ID = models.CharField(
        primary_key=True, max_length=12,default='', editable=True, verbose_name='通知ID')
    Type = models.CharField(max_length=10,default='Comment',verbose_name='通知类型')
    TopicObject = models.ForeignKey(TopicInfo, to_field='ObjectID', default=0, null=True,on_delete=models.CASCADE, verbose_name='文章专题')
    RollCallObject = models.ForeignKey(RollCallInfo, to_field='ObjectID', default=0, null=True,on_delete=models.CASCADE, verbose_name='点名')
    class Meta:
        verbose_name = '更新通知'
        # 末尾不加s
        verbose_name_plural = '更新通知中心'
        app_label = 'NTNotification'

    def __str__(self):
        return str(self.ID)