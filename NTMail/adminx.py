from django.contrib import admin
from NTMail.models import *
# Register your models here.
from xadmin import views
import xadmin

class MailBodyAdminView(object):
    """docstring for PublishNotification"""
    list_display = ('Scene',)

xadmin.site.register(MailBody,MailBodyAdminView)