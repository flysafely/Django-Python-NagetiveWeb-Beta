from django.db import models
from NTWebsite.models.User import *
from NTWebsite.models.Topic import *
from NTWebsite.models.OperationRecord import *

# Create your models here.


class Notice(models.Model):
    ID = models.CharField(
        primary_key=True, max_length=12, default='', editable=True, verbose_name='通知ID')
    Type = models.CharField(max_length=15, verbose_name='通知类型')# C CR TAL TAD CAL CAD R RD L TP RP

    CommentInfo = models.ForeignKey(CommentInfo, to_field='ObjectID', related_name='CObject',
                                null=True, on_delete=models.CASCADE, verbose_name='评论')

    TopicInfo = models.ForeignKey(TopicInfo, to_field='ObjectID', related_name='TAObject',
                                 null=True, on_delete=models.CASCADE, verbose_name='文章')

    RollCallInfo = models.ForeignKey(RollCallInfo, to_field='ObjectID', related_name='RObject',
                                null=True, on_delete=models.CASCADE, verbose_name='点名')

    RollCallDialogue = models.ForeignKey(RollCallDialogue, to_field='ObjectID', related_name='RDObject',
                                 null=True, on_delete=models.CASCADE, verbose_name='点名对话')

    UserLink = models.ForeignKey(UserLink, to_field="id", related_name='LObject',
                                null=True, on_delete=models.CASCADE, verbose_name='被关注者')

    SourceUser = models.ForeignKey(
        User, to_field='id', related_name='NSourceUser', on_delete=models.CASCADE, verbose_name='通知者')
    TargetUser = models.ForeignKey(
        User, to_field='id', related_name='NTargetUser', on_delete=models.CASCADE, verbose_name='被通知者')

    class Meta:
        verbose_name = '通知信息'
        # 末尾不加s
        verbose_name_plural = '通知信息'
        app_label = 'NTNotification'

    def __str__(self):
        return str(self.ID)
