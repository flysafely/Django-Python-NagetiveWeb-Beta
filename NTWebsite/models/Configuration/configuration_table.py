from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from imagekit.processors import SmartResize


class ConfigParams(models.Model):
    """docstring for ConfigParams"""

    Name = models.CharField(max_length=20, unique=True, verbose_name='配置名称')

    TimeOut = models.IntegerField(
        default=60, blank=False, verbose_name='缓存时间')

    IndexURL = models.CharField(max_length=200,
                                default='/Topic/List/0/LE/1', blank=False, verbose_name='首页URL')
    ReadsThreshold = models.CharField(max_length=20,
                                      default=10, blank=False, verbose_name='阅读量阈值')
    TopicHotKeyWord = models.CharField(max_length=20,
                                       default='差评', blank=False, verbose_name='文章热搜词')
    RollCallHotKeyWord = models.CharField(max_length=20,
                                          default='差评', blank=False, verbose_name='点名热搜词')
    SpecialTopicHotKeyWord = models.CharField(max_length=20,
                                              default='差评', blank=False, verbose_name='专题热搜词')

    TopicsLimit = models.CharField(max_length=20,
                                   default=100, blank=False, verbose_name='文章获取数量')
    CommentsLimit = models.CharField(max_length=20,
                                     default=100, blank=False, verbose_name='文章评论获取数量')
    SecretKey = models.CharField(
        max_length=16, blank=False, verbose_name='加密秘钥')
    SecretVI = models.CharField(
        max_length=16, blank=False, verbose_name='加密偏移量')
    CommonPageLimit = models.IntegerField(
        default=10, blank=False, verbose_name='通用分页限制')
    TopicsPageLimit = models.IntegerField(
        default=10, blank=False, verbose_name='每页文章数量')
    SpecialTopicsPageLimit = models.IntegerField(
        default=10, blank=False, verbose_name='每页专题数量')
    RollCallsPageLimit = models.IntegerField(
        default=10, blank=False, verbose_name='每页点名数量')
    CommentsPageLimit = models.IntegerField(
        default=10, blank=False, verbose_name='每页评论数量')
    AvatarResolution = models.IntegerField(
        default=102, blank=False, verbose_name='头像分辨率')
    PicUploadWidth = models.IntegerField(
        default=600, blank=False, verbose_name='上传图片限制宽度')
    PicUploadFormat = models.CharField(max_length=20,
                                       default='jpg,png', blank=False, verbose_name='上传图片格式')
    PicTempPath = models.CharField(max_length=50,
                                   default='TopicPicUpload/Temp/', blank=False, verbose_name='文章临时图片路径')
    PicSavePath = models.CharField(max_length=50,
                                   default='TopicPicUpload/Save/', blank=False, verbose_name='文章发布图片路径')
    AvatarSavePath = models.CharField(max_length=50,
                                      default='Avatar/', blank=False, verbose_name='头像存放路径')
    DefaultAvatar = models.ImageField(
        upload_to='Avatar', blank=True, verbose_name='默认头像', default='')

    class Meta:
        # 末尾不加s
        verbose_name = '参数配置表'
        verbose_name_plural = '2.参数配置表'
        app_label = 'NTWebsite'
        #app_label = "配置表"

    def __str__(self):
        return self.Name


class PreferredConfigName(models.Model):
    Name = models.ForeignKey(
        ConfigParams, to_field='Name', null=True, on_delete=models.CASCADE, verbose_name='目前配置')

    class Meta:
        verbose_name = '配置设置'
        app_label = 'NTWebsite'
        # 末尾不加s
        verbose_name_plural = '3.配置设置'


class FilterQueryString(models.Model):
    Name = models.CharField(
        max_length=100, unique=True, verbose_name='过滤器关键')
    MethodString = models.CharField(
        max_length=200, blank=False, default='', verbose_name='匹配方法')
    QueryString = models.CharField(
        max_length=200, blank=False, verbose_name='查询语句')
    Template = models.CharField(
        max_length=100, null=True, verbose_name='使用模板')

    class Meta:
        verbose_name = '过滤器'
        app_label = 'NTWebsite'
        # 末尾不加s
        verbose_name_plural = '4.URL过滤器'
