from .improtFiles.models_import_head import *
from NTWebsite.MainMethods import QueryRedisCache as QRC
from collections import Iterable
from NTConfig.config import PermissionOption as POD
from NTConfig.config import PermissionDict as PD
import copy
#from NTWebsite import MainMethods as mMs


def Assign(Objects, ObjectType, request):
    Objects_Assigned = []
    for Object in Objects:
        PGDict = copy.deepcopy(PD[ObjectType])
        for k, v in PGDict.items():
            PGDict[k] = POD[k]['True'] if eval(
                POD[k]['Condition']) else POD[k]['False']
            #print('%sPGDict[%s]:%s,%s' % (Object.Title,k,PGDict[k],eval(POD[k]['Condition'])))
        Objects_Assigned.append((Object, PGDict))
    return Objects_Assigned


def Empower(ObjectType, Objects, request):
    # 待授权对象序列化
    PGList = []
    if Objects and isinstance(Objects, Model):
        PGList.append(Objects)
    elif Objects and isinstance(Objects, QuerySet):
        PGList += list(Objects)
    else:
        return 0
    # 待授权对象属性赋值
    return Assign(PGList, ObjectType, request)


def CheckVoteStatus(type, Object, point, request):
    return True if QRC(type + 'Attitude.objects.filter(ObjectID=%s,Point=%s,Publisher=%s)', 0, Object.ObjectID, point, request.user) else False


def CheckTipOffStatus(Object, request):
    return True if QRC('TipOffBox.objects.filter(ObjectID=%s,Publisher=%s)', 0, Object.ObjectID, request.user) else False


def CheckCollectStatus(type, Object, request):
    return True if QRC(type + '.objects.filter(ObjectID=%s,Publisher=%s)', 0, Object, request.user) else False


def CheckUserLinkStatus(Object, request):
    return True if QRC('UserLink.objects.filter(UserBeLinked=%s,UserLinking=%s)', 0, Object, request.user) else False


def CheckUserBlockStatus(Object, request):
    return True if QRC('BlackList.objects.filter(Enforceder=%s,Handler=%s)', 0, Object, request.user) else False

'''
def PermissionConfirm(type, Object, request, URLParams):
    ReturnList = []
    items = []

    # test=[]
    #testobject = User.objects.get(id="1")
    # test+=testobject
    # print(test)
    #print('isinstance(testobject, QuerySet):',isinstance(testobject, Model))
    #print('isinstance(Object, QuerySet):',isinstance(Object, QuerySet))
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
                    Permission_Sizer['TVoteBtn'] = 'disabled'
                    Permission_Sizer['TVote1Status'] = ''
                    Permission_Sizer['TVote0Status'] = ''
                    Permission_Sizer['CVoteBtn'] = 'disabled'
                    Permission_Sizer['CVote1Status'] = ''
                    Permission_Sizer['CVote0Status'] = ''
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
                    Permission_Sizer['TVoteBtn'] = ''
                    Permission_Sizer['TVote1Status'] = 'is-active' if QRC(
                        'TopicAttitude.objects.filter(ObjectID=%s,Point=1,Publisher=%s)', 0, item.ObjectID, request.user) else ''
                    Permission_Sizer['TVote0Status'] = 'is-active' if QRC(
                        'TopicAttitude.objects.filter(ObjectID=%s,Point=0,Publisher=%s)', 0, item.ObjectID, request.user) else ''
                    Permission_Sizer['CVoteBtn'] = ''
                    Permission_Sizer['CVote1Status'] = 'is-active' if QRC(
                        'CommentAttitude.objects.filter(ObjectID=%s,Point=1,Publisher=%s)', 0, item.ObjectID, request.user) else ''
                    Permission_Sizer['CVote0Status'] = 'is-active' if QRC(
                        'CommentAttitude.objects.filter(ObjectID=%s,Point=0,Publisher=%s)', 0, item.ObjectID, request.user) else ''
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
'''