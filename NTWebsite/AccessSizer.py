from .improtFiles.models_import_head import *
from NTWebsite.MainMethods import QueryRedisCache as QRC
from collections import Iterable
from NTWebsite.AppConfig import PermissionOption as POD
from NTWebsite.AppConfig import PermissionDict as PD
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
    return True if QRC(type + 'Attitude.objects.filter(ObjectID=%s,Point=%s,Publisher=%s)', 0, Object.ObjectID, point, request.user) else False


def CheckTipOffStatus(Object, request):
    return True if QRC('TipOffBox.objects.filter(ObjectID=%s,Publisher=%s)', 0, Object.ObjectID, request.user) else False


def CheckCollectStatus(type, Object, request):
    return True if QRC(type + '.objects.filter(ObjectID=%s,Publisher=%s)', 0, Object, request.user) else False


def CheckUserLinkStatus(Object, request):
    return True if QRC('UserLink.objects.filter(UserBeLinked=%s,UserLinking=%s)', 0, Object, request.user) else False


def CheckUserBlockStatus(Object, request):
    return True if QRC('BlackList.objects.filter(Enforceder=%s,Handler=%s)', 0, Object, request.user) else False
