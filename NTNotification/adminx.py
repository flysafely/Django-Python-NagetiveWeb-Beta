from django.contrib import admin
from NTNotification.models import CommentNotification
# Register your models here.
from xadmin import views
import xadmin

class CommentNotificationAdminView(object):
    """docstring for CommentNotification"""
    list_display = ('ID',)

xadmin.site.register(CommentNotification,CommentNotificationAdminView)