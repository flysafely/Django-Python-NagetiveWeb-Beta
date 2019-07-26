from django.contrib import admin
from NTNotification.models import *
# Register your models here.
from xadmin import views
import xadmin

class NoticeAdminView(object):
    """docstring for PublishNotification"""
    list_display = ('ID',)

xadmin.site.register(Notice,NoticeAdminView)
