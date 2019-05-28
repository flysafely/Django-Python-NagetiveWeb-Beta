"""nagetiveSite URL Configuration

The `urlpatterns` list routes URLs to V. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', V.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include
from NTWebsite import views as V
from NTWebsite import Processor as P
from django.conf.urls.static import static
from django.views.generic.base import RedirectView
from NTConfig import settings
from django.views.static import serve
import re
import xadmin

urlpatterns = [
    # views中有返回页面的导航
    #path('admin/', admin.site.urls),
    path('admin19901101/', xadmin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),    
    # Processor中没有返回页面的操作
    path('', P.indexView),
    path('logout/', P.Logout),
    path('PublishTopic/', P.PublishTopic),# RUST POST
    path('AttitudeOperate/', P.AttitudeOperate),# RUST POST
    path('PublishRollCall/', P.PublishRollCall),# RUST POST
    path('UserProfileUpdate/', P.UserProfileUpdate),# RUST POST
    path('UserLink/', P.UserLink),# RUST POST
    path('TipOff/', P.TipOff),# RUST POST
    path('Collect/', P.Collect),# RUST POST
    path('Replay/', P.Replay),# RUST POST
    path('Notice/', P.NoticeOpreate),
    path('BlackListOperation/', P.BlackListOperation),
    path('regist/', P.Regist),# RUST POST
    path('Param/', P.Param),
    re_path(r'^activate/(?P<UserID>.*)/(?P<Key>.*)/$', V.Activate),
    path('FetchTopic/', P.FetchTopic),# RUST GET
    re_path(r'^%s(?P<path>.*)$' % re.escape(settings.MEDIA_URL.lstrip('/')), serve, kwargs={'document_root':settings.MEDIA_ROOT}),# RUST GET
    re_path(r'^(?P<Region>.*)/(?P<Part>.*)/(?P<FilterValue>.*)/(?P<Order>.*)/(?P<PageNumber>.*)/(?P<ExtraParam>.*)$', V.Launcher),# main URL # RUST
    re_path(r'^login/.*$', P.Login),# RUST GET
    re_path(r'^uploadImg/.*', P.UploadImg),# RUST POST
    re_path(r'^favicon.ico$',RedirectView.as_view(url=r'media/favicon.ico'))# RUST GET
]

# + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# 不在urlpatterns后+ 的原因是，urlpatterns顺序是有影响的，位置在前的path或者re_path先匹配
# list 的 + 是组合成一个新的list，加入的对象在最后，这里要确保首先匹配media/***/***内容后做静态资源的指向，然后再匹配后面获取网站信息内容的re_path
# 由于我的media下资源有个内容路径比较深，刚好有一个上传专题封面图自动生成的路径为media/CACHE/images/Cover/***/****.png  这个长度刚好和 我的 main URL 匹配条件吻合
# 如果我只是在urlpatterns  后面+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  那这里的资源就没办法获取到