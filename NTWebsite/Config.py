import os
from .improtFiles.models_import_head import *
from django.shortcuts import get_object_or_404

class AppConfig(object):
    """docstring for DBConfig"""
    _instance = None

    def __new__(cls, *args, **kwargs):  # 这里不能使用__init__，因为__init__是在instance已经生成以后才去调用的
        if cls._instance is None:
            cls._instance = super(AppConfig, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        SelectedConfigName = PreferredConfigName.objects.all()[
            0].Name.Name
        ConfigObject = ConfigParams.objects.get(Name=SelectedConfigName)
        FieldNames = []
        for f in ConfigObject._meta.get_fields():
            if f.related_model is None:
                exec("self.%s = ConfigObject.%s" % (f.name, f.name))
                FieldNames.append(f.name)
        self.ConfigNames = FieldNames


class DBConfig(object):
    """docstring for AppConfig"""
    _instance = None

    def __new__(cls, *args, **kwargs):  # 这里不能使用__init__，因为__init__是在instance已经生成以后才去调用的
        if cls._instance is None:
            cls._instance = super(DBConfig, cls).__new__(cls)
        return cls._instance

    def __init__(self, keyword):
        QueryObject = get_object_or_404(FilterQueryString, Name=keyword)
        self.MethodString = QueryObject.MethodString
        self.QueryString = QueryObject.QueryString
        self.Template = QueryObject.Template


DefualtFilterDict = {"Search-User-LE": {"MethodString": "lambdaR,D,A,U:SearchInfoGet(R,D,A,U)", "QueryString": "User.objects.filter(Nick__contains=%s).order_by('-FansCount')", "Template": "Main-Frame.html"},
                     "Search-RollCall-LE": {"MethodString": "lambdaR,D,A,U:SearchInfoGet(R,D,A,U)", "QueryString": "RollCallInfo.objects.filter(Title__contains=%s).order_by('-EditDate')", "Template": "Main-Frame.html"},
                     "UserProfile-Fans-LE": {"MethodString": "lambdaR,D,A,U:UserProfileInfoGet(R,D,A,U)", "QueryString": "UserLink.objects.filter(UserBeLinked=%s).order_by('-LinkTime')", "Template": "Main-Frame.html"},
                     "UserProfile-Focus-LE": {"MethodString": "lambdaR,D,A,U:UserProfileInfoGet(R,D,A,U)", "QueryString": "UserLink.objects.filter(UserLinking=%s).order_by('-LinkTime')", "Template": "Main-Frame.html"},
                     "SpecialTopic-Category-LE": {"MethodString": "lambdaR,D,A,U:TopicsInfoGet(R,D,A,U)", "QueryString": "TopicInfo.objects.filter(Type=%s,Category=%s).order_by('-EditTime')", "Template": "Main-Frame.html"},
                     "UserProfile-Concern-LE": {"MethodString": "lambdaR,D,A,U:UserProfileInfoGet(R,D,A,U)", "QueryString": "Collection.objects.filter(Publisher=%s,Type='SpecialTopic').order_by('-CollectTime')", "Template": "Main-Frame.html"},
                     "UserProfile-Circusee-LE": {"MethodString": "lambdaR,D,A,U:UserProfileInfoGet(R,D,A,U)", "QueryString": "Collection.objects.filter(Publisher=%s,Type='RollCall').order_by('-CollectTime')", "Template": "Main-Frame.html"},
                     "UserProfile-Collect-LE": {"MethodString": "lambdaR,D,A,U:UserProfileInfoGet(R,D,A,U)", "QueryString": "Collection.objects.filter(Publisher=%s,Type='Topic').order_by('-CollectTime')", "Template": "Main-Frame.html"},
                     "UserProfile-TopicDislike-LE": {"MethodString": "lambdaR,D,A,U:UserProfileInfoGet(R,D,A,U)", "QueryString": "TopicAttitude.objects.filter(Publisher=%s,Point=0).order_by('-EditTime')", "Template": "Main-Frame.html"},
                     "UserProfile-TopicLike-LE": {"MethodString": "lambdaR,D,A,U:UserProfileInfoGet(R,D,A,U)", "QueryString": "TopicAttitude.objects.filter(Publisher=%s,Point=1).order_by('-EditTime')", "Template": "Main-Frame.html"},
                     "UserProfile-CommentDislike-LE": {"MethodString": "lambdaR,D,A,U:UserProfileInfoGet(R,D,A,U)", "QueryString": "CommentAttitude.objects.filter(Publisher=%s,Point=0).order_by('-EditTime')", "Template": "Main-Frame.html"},
                     "UserProfile-CommentLike-LE": {"MethodString": "lambdaR,D,A,U:UserProfileInfoGet(R,D,A,U)", "QueryString": "CommentAttitude.objects.filter(Publisher=%s,Point=1).order_by('-EditTime')", "Template": "Main-Frame.html"},
                     "UserProfile-Commit-LE": {"MethodString": "lambdaR,D,A,U:UserProfileInfoGet(R,D,A,U)", "QueryString": "CommentInfo.objects.filter(Publisher=%s).order_by('-EditDate')", "Template": "Main-Frame.html"},
                     "UserProfile-SpecialTopic-LE": {"MethodString": "lambdaR,D,A,U:UserProfileInfoGet(R,D,A,U)", "QueryString": "TopicInfo.objects.filter(Publisher=%s,Type='SpecialTopic').order_by('-EditTime')", "Template": "Main-Frame.html"},
                     "UserProfile-Topic-LE": {"MethodString": "lambdaR,D,A,U:UserProfileInfoGet(R,D,A,U)", "QueryString": "TopicInfo.objects.filter(Publisher=%s,Type='Topic').order_by('-EditTime')", "Template": "Main-Frame.html"},
                     "RollCall-Time-LE": {"MethodString": "lambdaR,D,A,U:RollCallsInfoGet(R,D,A,U)", "QueryString": "RollCallInfo.objects.filter(EditDate=%s).order_by('-Hot')", "Template": "Main-Frame.html"},
                     "RollCall-Content-LE": {"MethodString": "lambdaR,D,A,U:RollCallInfoContentInfoGet(R,D,A,U)", "QueryString": "RollCallDialogue.objects.filter(RollCallID=%s).order_by('EditDate')", "Template": "Main-Frame.html"},
                     "RollCall-List-HT": {"MethodString": "lambdaR,D,A,U:RollCallsInfoGet(R,D,A,U)", "QueryString": "RollCallInfo.objects.filter(Hot__gte=%s).order_by('-Hot')", "Template": "Main-Frame.html"},
                     "RollCall-List-RC": {"MethodString": "lambdaR,D,A,U:RollCallsInfoGet(R,D,A,U)", "QueryString": "RollCallInfo.objects.filter(Hot__gte=%s).order_by('-Recommend')", "Template": "Main-Frame.html"},
                     "RollCall-List-CL": {"MethodString": "lambdaR,D,A,U:RollCallsInfoGet(R,D,A,U)", "QueryString": "RollCallInfo.objects.filter(Hot__gte=%s).order_by('-Collect')", "Template": "Main-Frame.html"},
                     "RollCall-List-LE": {"MethodString": "lambdaR,D,A,U:RollCallsInfoGet(R,D,A,U)", "QueryString": "RollCallInfo.objects.filter(Hot__gte=%s).order_by('-EditDate')", "Template": "Main-Frame.html"},
                     "Search-SpecialTopic-HT": {"MethodString": "lambdaR,D,A,U:SearchInfoGet(R,D,A,U)", "QueryString": "TopicInfo.objects.filter(Q(Title__contains=%s)|Q(Description__contains=%s),Type=%s).order_by('-Hot')", "Template": "Main-Frame.html"},
                     "Search-SpecialTopic-CL": {"MethodString": "lambdaR,D,A,U:SearchInfoGet(R,D,A,U)", "QueryString": "TopicInfo.objects.filter(Q(Title__contains=%s)|Q(Description__contains=%s),Type=%s).order_by('-Collect')", "Template": "Main-Frame.html"},
                     "Search-SpecialTopic-RC": {"MethodString": "lambdaR,D,A,U:SearchInfoGet(R,D,A,U)", "QueryString": "TopicInfo.objects.filter(Q(Title__contains=%s)|Q(Description__contains=%s),Type=%s).order_by('-Recommend')", "Template": "Main-Frame.html"},
                     "Search-SpecialTopic-LE": {"MethodString": "lambdaR,D,A,U:SearchInfoGet(R,D,A,U)", "QueryString": "TopicInfo.objects.filter(Q(Title__contains=%s)|Q(Description__contains=%s),Type=%s).order_by('-EditTime')", "Template": "Main-Frame.html"},
                     "SpecialTopic-Theme-LE": {"MethodString": "lambdaR,D,A,U:TopicsInfoGet(R,D,A,U)", "QueryString": "TopicInfo.objects.filter(Type=%s,Theme=TopicThemeInfo.objects.get(Name=%s)).order_by('-EditTime')", "Template": "Main-Frame.html"},
                     "SpecialTopic-Time-LE": {"MethodString": "lambdaR,D,A,U:TopicsInfoGet(R,D,A,U)", "QueryString": "TopicInfo.objects.filter(Type=%s,EditTime__contains=%s)", "Template": "Main-Frame.html"},
                     "SpecialTopic-List-RC": {"MethodString": "lambdaR,D,A,U:TopicsInfoGet(R,D,A,U)", "QueryString": "TopicInfo.objects.filter(Type=%s,Recommend__gte=%s).order_by('-Recommend')", "Template": "Main-Frame.html"},
                     "SpecialTopic-List-CL": {"MethodString": "lambdaR,D,A,U:TopicsInfoGet(R,D,A,U)", "QueryString": "TopicInfo.objects.filter(Type=%s,Collect__gte=%s).order_by('-Collect')", "Template": "Main-Frame.html"},
                     "SpecialTopic-List-HT": {"MethodString": "lambdaR,D,A,U:TopicsInfoGet(R,D,A,U)", "QueryString": "TopicInfo.objects.filter(Type=%s,Hot__gte=%s).order_by('-Hot')", "Template": "Main-Frame.html"},
                     "SpecialTopic-List-LE": {"MethodString": "lambdaR,D,A,U:TopicsInfoGet(R,D,A,U)", "QueryString": "TopicInfo.objects.filter(Type=%s,Hot__gte=%s).order_by('-EditTime')", "Template": "Main-Frame.html"},
                     "SpecialTopic-Content-LE": {"MethodString": "lambdaR,D,A,U:TopicContentInfoGet(R,D,A,U)", "QueryString": "TopicInfo.objects.get(ObjectID=%s)", "Template": "Main-Frame.html"},
                     "Search-Topic-LE": {"MethodString": "lambdaR,D,A,U:SearchInfoGet(R,D,A,U)", "QueryString": "TopicInfo.objects.filter(Q(Title__contains=%s)|Q(Description__contains=%s),Type=%s).order_by('-EditTime')", "Template": "Main-Frame.html"},
                     "Topic-Content-LE": {"MethodString": "lambdaR,D,A,U:TopicContentInfoGet(R,D,A,U)", "QueryString": "TopicInfo.objects.get(ObjectID=%s)", "Template": "Main-Frame.html"},
                     "Topic-List-HT": {"MethodString": "lambdaR,D,A,U:TopicsInfoGet(R,D,A,U)", "QueryString": "TopicInfo.objects.filter(Type=%s,Hot__gte=%s).order_by('-Hot')", "Template": "Main-Frame.html"},
                     "Topic-List-CL": {"MethodString": "lambdaR,D,A,U:TopicsInfoGet(R,D,A,U)", "QueryString": "TopicInfo.objects.filter(Type=%s,Collect__gte=%s).order_by('-Collect')", "Template": "Main-Frame.html"},
                     "Topic-List-RC": {"MethodString": "lambdaR,D,A,U:TopicsInfoGet(R,D,A,U)", "QueryString": "TopicInfo.objects.filter(Type=%s,Recommend__gte=%s).order_by('-Recommend')", "Template": "Main-Frame.html"},
                     "Topic-Time-LE": {"MethodString": "lambdaR,D,A,U:TopicsInfoGet(R,D,A,U)", "QueryString": "TopicInfo.objects.filter(Type=%s,EditTime__contains=%s)", "Template": "Main-Frame.html"},
                     "Topic-Theme-LE": {"MethodString": "lambdaR,D,A,U:TopicsInfoGet(R,D,A,U)", "QueryString": "TopicInfo.objects.filter(Type=%s,Theme=TopicThemeInfo.objects.get(Name=%s)).order_by('-EditTime')", "Template": "Main-Frame.html"},
                     "Topic-Category-LE": {"MethodString": "lambdaR,D,A,U:TopicsInfoGet(R,D,A,U)", "QueryString": "TopicInfo.objects.filter(Type=%s,Category=%s).order_by('-EditTime')", "Template": "Main-Frame.html"},
                     "Topic-List-LE": {"MethodString": "lambdaR,D,A,U:TopicsInfoGet(R,D,A,U)", "QueryString": "TopicInfo.objects.filter(Type=%s,Hot__gte=%s).order_by('-EditTime')", "Template": "Main-Frame.html"}, }


PermissionOption = {
    'TVoteBtn': {'Condition': 'Object.Publisher==request.user', 'True': 'disabled', 'False': ''},
    'TVote1Status': {'Condition': "CheckVoteStatus('Topic',Object,1,request)", 'True': 'is-active', 'False': ''},
    'TVote0Status': {'Condition': "CheckVoteStatus('Topic',Object,0,request)", 'True': 'is-active', 'False': ''},
    'CVoteBtn': {'Condition': 'Object.Publisher==request.user', 'True': 'disabled', 'False': ''},
    'CVote1Status': {'Condition': "CheckVoteStatus('Comment',Object,1,request)", 'True': 'is-active', 'False': ''},
    'CVote0Status': {'Condition': "CheckVoteStatus('Comment',Object,0,request)", 'True': 'is-active', 'False': ''},
    'DonateBtn': {'Condition': 'Object.Publisher==request.user', 'True': 'hidden', 'False': ''},
    'TipOffBtn': {'Condition': 'Object.Publisher==request.user', 'True': 'hidden', 'False': ''},
    'TipOffStatus': {'Condition': 'CheckTipOffStatus(Object,request)', 'True': '已投诉', 'False': '投诉'},
    'CollectBtn': {'Condition': 'Object.Publisher==request.user', 'True': 'hidden', 'False': ''},
    'CollectStatus': {'Condition': "CheckCollectStatus('Collect',Object,request)", 'True': '取消收藏', 'False': '收藏'},
    'ConcernBtn': {'Condition': 'Object.Publisher==request.user', 'True': 'hidden', 'False': ''},
    'ConcernStatus': {'Condition': "CheckCollectStatus('Concern',Object,request)", 'True': '取消关注', 'False': '关注'},
    'CircuseeBtn': {'Condition': 'Object.Publisher==request.user', 'True': 'hidden', 'False': ''},
    'CircuseeStatus': {'Condition': "CheckCollectStatus('Circusee',Object,request)", 'True': '取消围观', 'False': '围观'},
    'EditBtn': {'Condition': 'Object.Publisher==request.user', 'True': '', 'False': 'hidden'},
    'ReplayBtn': {'Condition': 'Object.Publisher==request.user', 'True': 'hidden', 'False': ''},
    'ReplayBlock': {'Condition': 'request.user in (Object.Target,Object.Publisher)', 'True': '', 'False': 'hidden'},
    'ReplayBlockSite': {'Condition': 'Object.Target==request.user', 'True': 'right', 'False': ''},
    'VisitorIdentity': {'Condition': 'Object==request.user', 'True': 'Self', 'False': 'Others'},
    'VisitorOAuth-Read': {'Condition': 'Object==request.user', 'True': '1', 'False': 'readonly'},
    'VisitorOAuth-Edit': {'Condition': 'Object==request.user', 'True': '', 'False': 'hidden'},
    'VisitorOAuth-Link': {'Condition': 'CheckUserLinkStatus(Object,request)', 'True': 'Linked', 'False': 'Link'},
    'VisitorOAuth-Block': {'Condition': 'CheckUserBlockStatus(Object,request)', 'True': 'Blocked', 'False': 'Block'},
}

PermissionDict = {
    "Topic": {
        'TVoteBtn': '',
        'TVote1Status': '',
        'TVote0Status': '',
        'DonateBtn': '',
        'TipOffBtn': '',
        'TipOffStatus': '',
        'CollectBtn': '',
        'CollectStatus': '',
        'EditBtn': '',
        'ReplayBtn': '',
    },
    "SpecialTopic": {
        'TVoteBtn': '',
        'TVote1Status': '',
        'TVote0Status': '',
        'DonateBtn': '',
        'TipOffBtn': '',
        'TipOffStatus': '',
        'ConcernBtn': '',
        'ConcernStatus': '',
        'EditBtn': '',
        'ReplayBtn': '',
    },
    "RollCall": {
        'DonateBtn': '',
        'TipOffBtn': '',
        'TipOffStatus': '',
        'CircuseeBtn': '',
        'CircuseeStatus': '',
        'ReplayBtn': '',
        'ReplayBlock': '',
        'ReplayBlockSite': ''
    },
    "Comment": {
        'CVoteBtn': '',
        'CVote1Status': '',
        'CVote0Status': '',
        'DonateBtn': '',
        'TipOffBtn': '',
        'TipOffStatus': '',
        'ReplayBtn': '',
        'EditBtn': '',
    },
    "UserProfile": {
        'VisitorIdentity': '',
        'VisitorOAuth-Read': '',
        'VisitorOAuth-Edit': '',
        'VisitorOAuth-Link': '',
        'VisitorOAuth-Block': '',
    },
    "User": {
        'VisitorIdentity': '',
        'VisitorOAuth-Link': '',
        'VisitorOAuth-Block': '',
    }
}
