from django.db import models

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from imagekit.processors import SmartResize

from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
import uuid

'''
class ConfigParams(models.Model):
    """docstring for ConfigParams"""

    CP_Name = models.CharField(max_length=20, unique=True, verbose_name='配置名称')
    CP_ReadsThreshold = models.IntegerField(
        default=10, blank=False, verbose_name='上榜阅读量')
    CP_HotKeyWord = models.CharField(max_length=20,
                                     default='差评', blank=False, verbose_name='热搜关键字')
    CP_TopicsLimit = models.IntegerField(
        default=100, blank=False, verbose_name='文章获取数量')
    CP_CommentsLimit = models.IntegerField(
        default=100, blank=False, verbose_name='文章评论获取数量')
    CP_SecretKey = models.CharField(
        max_length=16, blank=False, verbose_name='加密秘钥')
    CP_SecretVI = models.CharField(
        max_length=16, blank=False, verbose_name='加密偏移量')
    CP_TopicsPageLimit = models.IntegerField(
        default=10, blank=False, verbose_name='每页文章数量')
    CP_SpecialTopicsPageLimit = models.IntegerField(
        default=10, blank=False, verbose_name='每页专题数量')
    CP_RollCallsPageLimit = models.IntegerField(
        default=10, blank=False, verbose_name='每页点名数量')
    CP_CommentsPageLimit = models.IntegerField(
        default=10, blank=False, verbose_name='每页评论数量')
    CP_AvatarResolution = models.IntegerField(
        default=102, blank=False, verbose_name='头像分辨率')

    class Meta:
        # 末尾不加s
        verbose_name = '配置参数'
        verbose_name_plural = '*****配置参数*****'
        #app_label = "配置表"

    def __str__(self):
        return self.CP_Name


class PreferredConfigName(models.Model):
    PC_Name = models.ForeignKey(
        ConfigParams, to_field='CP_Name', on_delete=models.CASCADE, verbose_name='首选配置名称')

    class Meta:
        verbose_name = '首选配置'
        # 末尾不加s

        verbose_name_plural = '*****首选配置设置*****'
        pass
'''

# 用户信息表
class User(AbstractUser):
    """docstring for UserTable"""

    UT_Nick = models.CharField(max_length=20, verbose_name='昵称')
    #UT_CheckInDate = models.CharField(max_length=50, verbose_name='注册时间', blank=True, null=False)
    UT_Sex = models.CharField(
        max_length=3, verbose_name='性别', default="未公开", blank=True, null=False)
    UT_Region = models.CharField(
        max_length=10, verbose_name='地区', blank=True, null=True, default="城市")
    UT_Description = models.TextField(
        max_length=50, verbose_name='简介', blank=True, null=True, default="简介")
    UT_Avatar = models.TextField(max_length=1000, verbose_name='头像URL',
                                 default='/static/media/DefaultLogo.jpg', blank=True, null=False)
    UT_Constellation = models.CharField(
        max_length=10, blank=True, null=True, default='天蝎座', verbose_name='星座')
    UT_FansCount = models.IntegerField(verbose_name='关注者数量', default=0)
    UT_FoucusCount = models.IntegerField(verbose_name='关注数量', default=0)
    UT_TopicsCount = models.IntegerField(verbose_name='文章发布数量', default=0)
    UT_SpecialTopicsCount = models.IntegerField(
        verbose_name='专题发布数量', default=0)
    UT_RollCallsCount = models.IntegerField(verbose_name='点名发布数量', default=0)
    UT_RreplayCount = models.IntegerField(verbose_name='点名回复数量', default=0)
    UT_TreplayCount = models.IntegerField(verbose_name='文章评论数量', default=0)
    UT_SreplayCount = models.IntegerField(verbose_name='专题评论数量', default=0)

    class Meta(AbstractUser.Meta):
        verbose_name = '用户'
        # 末尾不加s
        #verbose_name_plural = '用户'
        pass

    def __str__(self):
        return self.UT_Nick

# 文章主题表


class TopicArticleTheme(models.Model):
    """docstring for TopicArticleTheme"""
    TAT_ID = models.CharField(
        primary_key=True, max_length=10, default='0', verbose_name='主题代码')
    TAT_Name = models.CharField(
        max_length=10, unique=True, verbose_name='主题名称')

    class Meta:
        verbose_name = '文章'
        # 末尾不加s
        verbose_name_plural = '**1**文章主题**1**'

    def __str__(self):
        return self.TAT_Name

# 品类信息表


class CategoryInfo(models.Model):
    CI_Name = models.CharField(primary_key=True,
                               max_length=10, null=False, blank=False, verbose_name='品类名称')
    CI_SVG = models.TextField(max_length=1000, verbose_name='图标SVG')

    class Meta:
        verbose_name = '类目'
        # 末尾不加s
        verbose_name_plural = '**1**来自类目**1**'

    def __str__(self):
        return self.CI_Name


# 文章信息表.


class TopicArticleStatistic(models.Model):
    """docstring for ClassName"""

    TAS_ID = models.UUIDField(
        primary_key=True, auto_created=True, default=uuid.uuid4, verbose_name='文章ID')
    TAS_Title = models.CharField(
        max_length=35, unique=True, verbose_name='文章标题')
    TAS_Description = models.TextField(max_length=140, verbose_name='文章描述')
    TAS_EditDate = models.DateField(auto_now=True, verbose_name='编辑时间')
    TAS_Author = models.ForeignKey(
        User, to_field='username', default='flysafely', on_delete=models.CASCADE, verbose_name='用户名')
    TAS_Theme = models.CharField(
        max_length=100, default="其他", verbose_name='文章主题')
    TAS_Type = models.ForeignKey(
        CategoryInfo, to_field='CI_Name', on_delete=models.CASCADE, verbose_name='文章类别')
    TAS_Like = models.IntegerField(verbose_name='赞', default=0)
    TAS_Dislike = models.IntegerField(verbose_name='怼', default=0)
    TAS_Read = models.IntegerField(verbose_name='阅读量', default=10)
    TAS_Comment = models.IntegerField(verbose_name='评论数', default=0)
    TAS_Content = RichTextUploadingField(
        null=True, blank=True, config_name='admin', verbose_name='文章正文')

    class Meta:
        verbose_name = '文章信息'
        # 末尾不加s
        verbose_name_plural = '**1**文章基础信息**1**'

    def __str__(self):
        return self.TAS_Title


# 文章标签表


class ArticleTags(models.Model):
    AT_TAID = models.UUIDField(
        default=uuid.uuid4, null=False, editable=False, verbose_name='文章ID')
    AT_ID = models.IntegerField(verbose_name='标签代码')
    AT_Name = models.CharField(max_length=10, verbose_name='标签名称')

    class Meta:
        verbose_name = '标签'
        # 末尾不加s
        verbose_name_plural = '**1**文章标签**1**'

    def __str__(self):
        return self.AT_Name

# 文章评论表


class ArticleComment(models.Model):
    """docstring for ArticleComment"""
    Readstatus = (("Y", "已阅"), ("N", "未读"))

    AC_ID = models.UUIDField(
        primary_key=True, editable=False, auto_created=True, default=uuid.uuid4, verbose_name='评论ID')
    AC_ArticleID = models.ForeignKey(
        TopicArticleStatistic, to_field='TAS_Title', on_delete=models.CASCADE, verbose_name='文章ID')
    # AC_ArticleID = models.UUIDField(
    #    null=False, editable=True, verbose_name='文章ID')
    AC_Comment = models.TextField(verbose_name="评论内容")
    AC_Parent = models.CharField(
        max_length=100, editable=True, default='', verbose_name='父评论ID')
    AC_Like = models.IntegerField(verbose_name='赞', default="0")
    AC_Dislike = models.IntegerField(verbose_name='怼', default="0")
    AC_EditDate = models.DateTimeField(auto_now=True, verbose_name='编辑时间')
    AC_UserNickName = models.ForeignKey(
        User, to_field='username', default='flysafely', on_delete=models.CASCADE, verbose_name='用户名')
    AC_Readstatus = models.CharField(
        max_length=1, default="N", choices=Readstatus, verbose_name='是否阅读')

    class Meta:
        verbose_name = '评论'
        # 末尾不加s
        verbose_name_plural = '**1**文章评论**1**'

    def __str__(self):
        return self.AC_Comment

# 文章立场统计


class ArticleUserLikesOrDislikesTable(models.Model):
    """docstring for ArticleLikseIP"""
    ALD_UserNickName = models.ForeignKey(
        User, to_field='username', default='flysafely', on_delete=models.CASCADE, verbose_name='用户名')
    ALD_StandPoint = models.IntegerField(blank=False, verbose_name='立场代码')
    # ALD_ArticleID = models.CharField(max_length=100, null=True,
    #                                 blank=True, verbose_name='文章ID')
    ALD_EditDate = models.DateField(auto_now=True, verbose_name='时间')
    ALD_ArticleID = models.ForeignKey(
        TopicArticleStatistic, to_field='TAS_Title', on_delete=models.CASCADE, verbose_name='文章ID')

    class Meta:
        verbose_name = '立场记录'
        # 末尾不加s
        verbose_name_plural = '**1**文章立场统计**1**'

# 评论立场统计


class CommentUserLikesOrDislikesTable(models.Model):
    """docstring for ArticleLikseIP"""
    CLD_UserNickName = models.ForeignKey(
        User, to_field='username', default='flysafely', on_delete=models.CASCADE, verbose_name='用户名')
    CLD_StandPoint = models.IntegerField(blank=False, verbose_name='立场代码')
    # ALD_ArticleID = models.CharField(max_length=100, null=True,
    #                                 blank=True, verbose_name='文章ID')
    CLD_EditDate = models.DateField(auto_now=True, verbose_name='时间')
    CLD_CommentID = models.ForeignKey(
        ArticleComment, to_field='AC_ID', on_delete=models.CASCADE, verbose_name='评论ID')

    class Meta:
        verbose_name = '评论立场记录'
        # 末尾不加s
        verbose_name_plural = '**1**评论立场统计**1**'

# 阅读IP统计


class ArticleReadsIP(models.Model):
    """docstring for ArticleLikseIP"""
    AR_IP = models.CharField(max_length=100, null=True,
                             blank=True, verbose_name='IP')
    AR_EditDate = models.DateField(auto_now=True, verbose_name='时间')
    # AR_ArticleID = models.CharField(max_length=100, null=True,
    #                                blank=True, verbose_name='文章ID')
    AR_ArticleID = models.ForeignKey(
        TopicArticleStatistic, to_field='TAS_Title', on_delete=models.CASCADE, verbose_name='文章ID')

    class Meta:
        verbose_name = '阅读IP记录'
        # 末尾不加s
        verbose_name_plural = '**1**文章阅读IP统计**1**'

    def __str__(self):
        return self.AR_IP

# 用户关注


class UserLink(models.Model):
    """docstring for UserLink"""
    UL_UserBeLinked = models.ForeignKey(
        User, to_field='username', null=False, blank=False, on_delete=models.CASCADE, verbose_name='被关注用户')
    UL_UserLinking = models.ForeignKey(
        User, to_field='username', related_name='UserNameLinking', null=False, blank=False, on_delete=models.CASCADE, verbose_name='关注用户')
    UL_LinkTime = models.DateField(auto_now=True, verbose_name='时间')

    class Meta:
        verbose_name = '关注信息'
        verbose_name_plural = '**4**用户关注信息**4**'


class UserCollect(models.Model):
    """docstring for UserCollect"""
    UC_UserNickName = models.ForeignKey(
        User, to_field='username', default='flysafely', on_delete=models.CASCADE, verbose_name='用户名')
    UC_Article = models.ForeignKey(
        TopicArticleStatistic, to_field='TAS_ID', on_delete=models.CASCADE, verbose_name='文章ID')
    UC_CollectTime = models.DateField(auto_now=True, verbose_name='时间')

    class Meta:
        verbose_name = '文章收藏'
        verbose_name_plural = '**1**文章用户收藏**1**'


class RollCallInfo(models.Model):
    """docstring for RollCallInfo"""
    RCI_ID = models.UUIDField(
        primary_key=True, auto_created=True, default=uuid.uuid4, verbose_name='点名ID')
    RCI_Title = models.CharField(
        max_length=35, unique=True, verbose_name='点名标题')
    RCI_EditDate = models.DateField(auto_now=True, verbose_name='编辑时间')
    RCI_Publisher = models.ForeignKey(
        User, to_field='username', related_name='Publisher_User', on_delete=models.CASCADE, verbose_name='点名者')
    RCI_Target = models.ForeignKey(
        User, to_field='username', related_name='Target_User', on_delete=models.CASCADE, verbose_name='被点名者')
    RCI_LeftLike = models.IntegerField(
        default=0, blank=False, verbose_name='点名者支持数')
    RCI_RightLike = models.IntegerField(
        default=0, blank=False, verbose_name='被点名者支持数')
    RCI_Read = models.IntegerField(
        default=0, blank=False, verbose_name='点名阅读量')

    class Meta:
        verbose_name = '点名信息'
        # 末尾不加s
        verbose_name_plural = '**2**点名基础信息**2**'
        pass

    def __str__(self):
        return self.RCI_Title


class RollCallDialogue(models.Model):
    RCD_ID = models.ForeignKey(
        RollCallInfo, to_field='RCI_ID', on_delete=models.CASCADE, verbose_name='点名信息')
    RCD_EditDate = models.DateField(auto_now=True, verbose_name='编辑时间')
    RCD_Query = models.CharField(
        max_length=30, default='', blank=False, verbose_name='询问内容')
    RCD_Reply = models.CharField(
        max_length=30, default='', blank=False, verbose_name='回复内容')

    class Meta:
        verbose_name = '对话记录'
        # 末尾不加s
        verbose_name_plural = '**2**点名对话明细**2**'
        pass

    def __str__(self):
        return str(self.RCD_ID.RCI_ID)


class RollCallReadsIP(models.Model):
    """docstring for RollCallReadsIP"""
    RCR_IP = models.CharField(max_length=100, null=True,
                              blank=True, verbose_name='IP')
    RCR_EditDate = models.DateField(auto_now=True, verbose_name='时间')
    # AR_ArticleID = models.CharField(max_length=100, null=True,
    #                                blank=True, verbose_name='文章ID')
    RCR_ArticleID = models.ForeignKey(
        RollCallInfo, to_field='RCI_Title', on_delete=models.CASCADE, verbose_name='围观ID')

    class Meta:
        verbose_name = 'IP记录'
        # 末尾不加s
        verbose_name_plural = '**2**围观IP统计**2**'

    def __str__(self):
        return self.RCR_IP


class UserCircuseeCollect(models.Model):
    UCC_UserNickName = models.ForeignKey(
        User, to_field='username', default='flysafely', on_delete=models.CASCADE, verbose_name='用户名')
    UCC_RollCall = models.ForeignKey(
        RollCallInfo, to_field='RCI_ID', on_delete=models.CASCADE, verbose_name='点名ID')
    UCC_CollectTime = models.DateField(auto_now=True, verbose_name='时间')

    class Meta:
        verbose_name = '围观'
        verbose_name_plural = '**2**用户围观**2**'


class SpecialTopicInfo(models.Model):
    """docstring for SpecialTopicInfo"""
    STI_ID = models.UUIDField(
        primary_key=True, auto_created=True, default=uuid.uuid4, verbose_name='专题ID')
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
        pass

    def __str__(self):
        return self.STI_Title


class SpecialTopicFollow(models.Model):
    STF_UserNickName = models.ForeignKey(
        User, to_field='username', default='flysafely', on_delete=models.CASCADE, verbose_name='用户名')
    STF_SpecialTopic = models.ForeignKey(
        SpecialTopicInfo, to_field='STI_ID', on_delete=models.CASCADE, verbose_name='专题ID')
    STF_CollectTime = models.DateField(auto_now=True, verbose_name='时间')

    class Meta:
        verbose_name = '关注'
        verbose_name_plural = '**3**专题关注**3**'


class SpecialTopicReadsIP(models.Model):
    """docstring for SpecialTopicReadsIP"""
    STR_IP = models.CharField(max_length=100, null=True,
                              blank=True, verbose_name='IP')
    STR_EditDate = models.DateField(auto_now=True, verbose_name='时间')
    # AR_ArticleID = models.CharField(max_length=100, null=True,
    #                                blank=True, verbose_name='文章ID')
    STR_SpecialTopicID = models.ForeignKey(
        SpecialTopicInfo, to_field='STI_ID', on_delete=models.CASCADE, verbose_name='专题ID')

    class Meta:
        verbose_name = 'IP记录'
        # 末尾不加s
        verbose_name_plural = '**3**专题阅读IP统计**3**'

    def __str__(self):
        return self.STR_IP

# 专题评论表


class SpecialTopicComment(models.Model):
    """docstring for ArticleComment"""
    Readstatus = (("Y", "已阅"), ("N", "未读"))

    STC_ID = models.UUIDField(
        primary_key=True, editable=False, auto_created=True, default=uuid.uuid4, verbose_name='专题评论ID')
    STC_SpecialTopicID = models.ForeignKey(
        SpecialTopicInfo, to_field='STI_ID', on_delete=models.CASCADE, verbose_name='专题ID')
    STC_Comment = models.TextField(verbose_name="评论内容")
    STC_Parent = models.CharField(
        max_length=100, editable=True, default='', verbose_name='父评论ID')
    #STC_Like = models.IntegerField(verbose_name='赞', default="0")
    #STC_Dislike = models.IntegerField(verbose_name='怼', default="0")
    STC_EditDate = models.DateTimeField(auto_now=True, verbose_name='编辑时间')
    STC_UserNickName = models.ForeignKey(
        User, to_field='username', default='flysafely', on_delete=models.CASCADE, verbose_name='用户名')
    STC_Readstatus = models.CharField(
        max_length=1, default="N", choices=Readstatus, verbose_name='是否阅读')

    class Meta:
        verbose_name = '评论'
        # 末尾不加s
        verbose_name_plural = '**3**专题评论**3**'

    def __str__(self):
        return self.STC_Comment


class RecommendAuthor(models.Model):
    RA_Author = models.ForeignKey(
        User, to_field='username', default='flysafely', on_delete=models.CASCADE, verbose_name='用户名')
    RA_Rank = models.IntegerField(
        default=0, blank=False, verbose_name='顺序')

    class Meta:
        verbose_name = '用户'
        # 末尾不加s
        verbose_name_plural = '**1**推荐用户**1**'

    def __str__(self):
        return self.RA_Author.UT_Nick


class NotificationTable(models.Model):

    NT_ID = models.UUIDField(
        primary_key=True, auto_created=True, default=uuid.uuid4, verbose_name='通知ID')
    NT_KeyID = models.CharField(
        max_length=100, blank=False, default='', verbose_name='关键ID')
    NT_AnchorID = models.CharField(
        max_length=100, blank=False, default='', verbose_name='定位ID')
    NT_Title = models.CharField(
        max_length=100, blank=False, default='', verbose_name='标题')
    NT_URL = models.CharField(max_length=30, blank=False, verbose_name='URL')
    NT_Part = models.CharField(
        max_length=30, blank=False, default='', verbose_name='板块')
    NT_Sign = models.CharField(
        max_length=30, blank=False, default='', verbose_name='标记')
    NT_SourceUser = models.ForeignKey(
        User, to_field='username', related_name='SourceUser', on_delete=models.CASCADE, verbose_name='通知者', default='')
    NT_TargetUser = models.ForeignKey(
        User, to_field='username', related_name='TargetUser', on_delete=models.CASCADE, verbose_name='被通知者')

    class Meta:
        verbose_name = '信息'
        # 末尾不加s
        verbose_name_plural = '**4**通知信息**4**'

    def __str__(self):
        return str(self.NT_ID)


class BlackList(models.Model):
    """docstring for blacklist"""

    BL_ID = models.UUIDField(
        primary_key=True, auto_created=True, default=uuid.uuid4, verbose_name='黑名单ID')
    BL_User = models.ForeignKey(
        User, to_field='username', related_name='BL_User', on_delete=models.CASCADE, verbose_name='被添加用户')
    BL_Handler = models.ForeignKey(
        User, to_field='username', related_name='BL_Handler', on_delete=models.CASCADE, verbose_name='操作用户')

    class Meta:
        verbose_name = '记录'
        # 末尾不加s
        verbose_name_plural = '**6**黑名单**6**'

    def __str__(self):
        return str(self.BL_User.UT_Nick)
