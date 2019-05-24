from .improtFiles.models_import_head import *
from NTWebsite.MainMethods import QueryRedisCache as QRC
from collections import Iterable
from NTWebsite.Config import PermissionOption as POD
from NTWebsite.Config import PermissionDict as PD
import copy
#from NTWebsite import MainMethods as mMs

def Assign(Objects, ObjectType, request):
    Objects_Assigned = []
    for Object in Objects:
        PGDict = copy.deepcopy(PD[ObjectType])
        for k, v in PGDict.items():
            PGDict[k] = POD[k]['True'] if eval(
                POD[k]['Condition']) else POD[k]['False']
        Objects_Assigned.append((Object, PGDict))
    return Objects_Assigned


def Empower(ObjectType, Objects, request):
    # 待授权对象序列化
    PGList = []
    if Objects and isinstance(Objects, Model):
        PGList.append(Objects)
    elif Objects and isinstance(Objects, (QuerySet,Iterable)):
        PGList += list(Objects)
    else:
        return 0
    # 待授权对象属性赋值
    return Assign(PGList, ObjectType, request)


def CheckVoteStatus(type, Object, point, request):
    if request.user.is_authenticated:
        return True if QRC(type + 'Attitude.objects.filter(ObjectID=%s,Point=%s,Publisher=%s)', 0, Object.ObjectID, point, request.user) else False
    else:
        return False

def CheckTipOffStatus(Object, request):
    if request.user.is_authenticated:
        return True if QRC('TipOffBox.objects.filter(ObjectID=%s,Publisher=%s)', 0, Object.ObjectID, request.user) else False
    else:
        return False

def CheckCollectStatus(type, Object, request):
    if request.user.is_authenticated:
        return True if QRC(type + '.objects.filter(ObjectID=%s,Publisher=%s)', 0, Object, request.user) else False
    else:
        return False

def CheckUserLinkStatus(Object, request):
    if request.user.is_authenticated:
        return True if QRC('UserLink.objects.filter(UserBeLinked=%s,UserLinking=%s)', 0, Object, request.user) else False
    else:
        return False

def CheckUserBlockStatus(Object, request):
    if request.user.is_authenticated:
        return True if QRC('BlackList.objects.filter(Enforceder=%s,Handler=%s)', 0, Object, request.user) else False
    else:
        return False