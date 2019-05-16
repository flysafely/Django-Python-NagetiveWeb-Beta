from .improtFiles.models_import_head import *
from xadmin import views
import xadmin
# --------------Comment-----------------
class CommentInfoAdminView(object):
    """docstring for CommentInfo"""
    list_display = ('Content', 'Publisher',
                    'EditDate', 'Type')
    search_fields = ['Content','Publisher__Nick','CommentID']

# --------------Configuration-----------------
class ConfigParamsAdminView(object):
    """docstring for ConfigParams"""
    list_display = ('Name',)

class PreferredConfigNameAdminView(object):
    """docstring for PreferredConfigName"""
    list_display = ('Name',)    

class FilterQueryStringAdminView(object):
    """docstring for FilterQueryString"""
    list_display = ('Name',)

# -------------------Opreation------------
class AttitudeAdminView(object):
    """docstring for Attitude"""
    list_display = ('Publisher',)

class ReadsIPAdminView(object):
    """docstring for ReadsIP"""
    list_display = ('IP', 'Type')    

class UserLinkAdminView(object):
    """docstring for ArticleComment"""
    list_display = ('UserBeLinked', 'UserLinking', 'LinkTime')  

class CollectionAdminView(object):
    """docstring for Collection"""
    list_display = ('Publisher', 'Type', 'ObjectID', 'CollectTime')  

class PublisherListAdminView(object):
    list_display = ('Order',)      

class NotificationAdminView(object):
    list_display = ('TargetUser',)    

class BlackListAdminView(object):
    list_display = ('Enforceder', 'Handler',)

class TipOffBoxAdminView(object):
    """docstring for TipOffBox"""
    list_display = ('Type', 'ObjectID')

# ----------------RollCall-------------------
class RollCallInfoAdminView(object):
    """docstring for RollCallInfo"""
    list_display = ('Title', 'Publisher', 'Target',)
    search_fields = ['Publisher__Nick','Title']

class RollCallDialogueAdminView(object):
    list_display = ('RollCallID', 'EditDate',)
    search_fields = ['Publisher__Nick','RollCallID__Title','Content']

# -----------------Search-------------------
class SearchIndexAdminView(object):
    list_display = ('Content', 'Type',)

# ------------------Topic--------------------
class TopicThemeInfoAdminView(object):
    """docstring for TopicThemeInfo"""
    list_display = ('Name',)

class TopicCategoryInfoAdminView(object):
    """docstring for TopicCategoryInfo"""
    list_display = ('Name',)
    list_editable =('Name','SVG')

class TopicInfoAdminView(object):
    """docstring for TopicInfo"""
    readonly_fields = ('EditTime',)
    list_display = ('Title','Publisher','Recommend','EditTime')
    search_fields = ['Title','Publisher__Nick','ObjectID']

class UserAdminView(object):
    """docstring for ClassName"""
    list_display = ('id','Nick',)

class GlobalSetting(object):
    # 后台管理系统的名字
    site_title = '球莫名堂后台管理'
    # 管理系统的设计者，当然你可以改成其他内容
    site_footer = 'Design by Flysafely'
    # 左侧菜单栏是否可隐藏
    menu_style = 'accordion'
class BaseSetting(object):
    # 启用主题
    enable_themes = True
    use_bootswatch = True        

xadmin.site.register(CommentInfo,CommentInfoAdminView)
xadmin.site.register(ConfigParams,ConfigParamsAdminView)
xadmin.site.register(PreferredConfigName,PreferredConfigNameAdminView)
xadmin.site.register(FilterQueryString,FilterQueryStringAdminView)
xadmin.site.register(Attitude,AttitudeAdminView)
xadmin.site.register(ReadsIP,ReadsIPAdminView)
xadmin.site.register(UserLink,UserLinkAdminView)
xadmin.site.register(Collection,CollectionAdminView)
xadmin.site.register(PublisherList,PublisherListAdminView)
xadmin.site.register(Notification,NotificationAdminView)
xadmin.site.register(BlackList,BlackListAdminView)
xadmin.site.register(TipOffBox,TipOffBoxAdminView)
xadmin.site.register(RollCallInfo,RollCallInfoAdminView)
xadmin.site.register(RollCallDialogue,RollCallDialogueAdminView)
xadmin.site.register(SearchIndex,SearchIndexAdminView)
xadmin.site.register(TopicThemeInfo,TopicThemeInfoAdminView)
xadmin.site.register(TopicCategoryInfo,TopicCategoryInfoAdminView)
xadmin.site.register(TopicInfo,TopicInfoAdminView)
xadmin.site.register(views.CommAdminView,GlobalSetting)
xadmin.site.register(views.BaseAdminView,BaseSetting)












