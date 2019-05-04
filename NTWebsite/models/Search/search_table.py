from django.db import models


class SearchIndex(models.Model):
    """docstring for SearchIndex"""
    Content = models.CharField(max_length=50000, verbose_name='匹配内容')
    ID = models.CharField(
        primary_key=True, max_length=12, default='0', verbose_name='ID')
    Type = models.CharField(
        max_length=10, unique=True, verbose_name='所属板块')

    class Meta:
        verbose_name = '全局索引'
        # 末尾不加s
        verbose_name_plural = '**5**全局索引**5**'
        app_label = 'NTWebsite'

    def __str__(self):
        return self.Content
