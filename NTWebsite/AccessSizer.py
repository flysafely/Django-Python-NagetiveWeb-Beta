from .improtFiles.models_import_head import *
from NTWebsite.MainMethods import QueryRedisCache as QRC
from collections import Iterable
#from NTWebsite import MainMethods as mMs


def PermissionConfirm(type, Object, request, URLParams):
    ReturnList = []
    items = []

    if isinstance(Object, Iterable):
        items = Object
    else:
        if Object:
            items.append(Object)
        else:
            return 0
    for item in items:
        Permission_Sizer = {}
        if type != 'UserProfileInfo':
            if request.user.is_authenticated:
                if request.user == item.Publisher:
                    Permission_Sizer['VoteBtn'] = 'disabled'
                    Permission_Sizer['Vote1Status'] = ''
                    Permission_Sizer['Vote0Status'] = ''
                    Permission_Sizer['DonateBtn'] = 'hidden'
                    Permission_Sizer['TipOffBtn'], Permission_Sizer[
                        'TipOffStatus'] = ('hidden', '投诉')
                    Permission_Sizer['CloseBtn'] = 'Close' if URLParams[
                        'Region'] in 'SpecialTopic' else 'Delete'
                    Permission_Sizer['ShareBtn'] = ''
                    Permission_Sizer['CollectBtn'], Permission_Sizer[
                        'CollectStatus'] = ('hidden', '收藏')
                    Permission_Sizer['EditBtn'] = ''
                    # Comment特有
                    Permission_Sizer['ChatBtn'] = ''
                    Permission_Sizer['ReplayBtn'] = 'hidden'
                    # RollCall特有
                    Permission_Sizer['ReplayBlock'] = ''
                    Permission_Sizer['ReplayBlockSite'] = ''
                else:
                    Permission_Sizer['VoteBtn'] = ''
                    Permission_Sizer['Vote1Status'] = 'is-active' if QRC('Comment' if URLParams[
                                                                         'Part'] == 'Content' else 'Topic' + 'Attitude.objects.filter(ObjectID=%s,Point=1,Publisher=%s)', 0, item.ObjectID, request.user) else ''
                    Permission_Sizer['Vote0Status'] = 'is-active' if QRC('Comment' if URLParams[
                                                                         'Part'] == 'Content' else 'Topic' + 'Attitude.objects.filter(ObjectID=%s,Point=0,Publisher=%s)', 0, item.ObjectID, request.user) else ''
                    Permission_Sizer['DonateBtn'] = ''
                    Permission_Sizer['TipOffBtn'], Permission_Sizer['TipOffStatus'] = ('', '已投诉') if QRC(
                        'TipOffBox.objects.filter(ObjectID=%s,Publisher=%s)', 0, item.ObjectID, request.user) else ('', '投诉')
                    Permission_Sizer['CloseBtn'] = 'Close'
                    Permission_Sizer['ShareBtn'] = ''
                    Permission_Sizer['CollectBtn'], Permission_Sizer['CollectStatus'] = ('', '取消收藏') if QRC(
                        'Collection.objects.filter(ObjectID=%s,Publisher=%s)', 0, item.RollCallID.ObjectID if hasattr(item, 'RollCallID') else item.ObjectID, request.user) else ('', '收藏')
                    Permission_Sizer['EditBtn'] = 'hidden'
                    # Comment特有
                    Permission_Sizer['ChatBtn'] = ''
                    Permission_Sizer['ReplayBtn'] = ''
                    # RollCall特有
                    Permission_Sizer['ReplayBlock'] = '' if request.user == (
                        item.RollCallID.Target if hasattr(item, 'RollCallID') else '') else 'hidden'
                    Permission_Sizer['ReplayBlockSite'] = 'right' if request.user == (
                        item.RollCallID.Target if hasattr(item, 'RollCallID') else '') else ''
            else:
                Permission_Sizer['VoteBtn'] = ''
                Permission_Sizer['Vote1Status'] = ''
                Permission_Sizer['Vote0Status'] = ''
                Permission_Sizer['DonateBtn'] = ''
                Permission_Sizer['TipOffBtn'], Permission_Sizer[
                    'TipOffStatus'] = ('', '投诉')
                Permission_Sizer['CloseBtn'] = 'Close'
                Permission_Sizer['ShareBtn'] = ''
                Permission_Sizer['CollectBtn'], Permission_Sizer[
                    'CollectStatus'] = ('', '收藏')
                Permission_Sizer['EditBtn'] = 'hidden'
                # Comment特有
                Permission_Sizer['ChatBtn'] = ''
                Permission_Sizer['ReplayBtn'] = ''
                # RollCall特有
                Permission_Sizer['ReplayBlock'] = 'hidden'
                Permission_Sizer['ReplayBlockSite'] = ''
        else:
            TargetUser = QRC('User.objects.get(id=%s)',
                             None, URLParams['FilterValue'])
            if TargetUser == request.user:
                Permission_Sizer['VisitorIdentity'] = 'Self'
                Permission_Sizer['VisitorOAuth-Read'] = '1'
                Permission_Sizer['VisitorOAuth-Edit'] = ''
                Permission_Sizer['VisitorOAuth-Link'] = ''
                Permission_Sizer['VisitorOAuth-Block'] = ''
            else:
                Permission_Sizer['VisitorIdentity'] = 'Others'
                Permission_Sizer['VisitorOAuth-Read'] = 'readonly'
                Permission_Sizer['VisitorOAuth-Edit'] = 'hidden'
                Permission_Sizer['VisitorOAuth-Link'] = 'Linked' if QRC(
                    'UserLink.objects.filter(UserBeLinked=%s,UserLinking=%s)', 0, TargetUser, request.user) else 'Link'
                Permission_Sizer['VisitorOAuth-Block'] = 'Blocked' if QRC(
                    'BlackList.objects.filter(Enforceder=%s,Handler=%s)', 0, TargetUser, request.user) else 'Block'
        ReturnList.append((item, Permission_Sizer))
    return ReturnList
