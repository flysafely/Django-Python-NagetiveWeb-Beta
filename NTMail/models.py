from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class MailBody(models.Model):
    Scene = models.CharField(max_length=20, primary_key=True, verbose_name='发送场景')
    Title = models.CharField(max_length=50, verbose_name='邮件标题')
    Message = models.CharField(max_length=100, verbose_name='邮件内容')
    Html = RichTextUploadingField(
        null=True, blank=True, config_name='admin', verbose_name='邮件HTML')

    class Meta:
        verbose_name = '邮件模板'
        # 末尾不加s
        verbose_name_plural = '邮件模板'
        app_label = 'NTMail'

    def __str__(self):
        return str(self.Scene)


