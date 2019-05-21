from django.contrib import admin
from NTNotification.models import *
# Register your models here.
from xadmin import views
import xadmin

class CommentNotificationAdminView(object):
    """docstring for CommentNotification"""
    list_display = ('ID',)

class RollCallNotificationAdminView(object):
    """docstring for RollCallNotification"""
    list_display = ('ID',)

class LinkNotificationAdminView(object):
    """docstring for LinkNotification"""
    list_display = ('ID',)

class PublishNotificationAdminView(object):
    """docstring for PublishNotification"""
    list_display = ('ID',)

xadmin.site.register(CommentNotification,CommentNotificationAdminView)
xadmin.site.register(RollCallNotification,RollCallNotificationAdminView)
xadmin.site.register(LinkNotification,LinkNotificationAdminView)
xadmin.site.register(PublishNotification,PublishNotificationAdminView)