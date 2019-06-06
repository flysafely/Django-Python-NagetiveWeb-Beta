from django.http import HttpResponse, QueryDict
from NTWebsite.MainMethods import QueryRedisCache as QRC
from NTWebsite.MainMethods import RequestDataUnbox as RD
from NTWebsite.Config import NotificationDict as ND
from NTWebsite.Config import AppConfig as AC
import json

def NoticeGet(request):
    if request.user.is_authenticated:
        Notices = QRC(
            'Notice.objects.filter(TargetUser=%s)', 0, request.user)
        if Notices:
            dataList = []
            for Notice in Notices:
                dataDict = {}
                dataDict['ID'] = Notice.ID
                dataDict['Region'] = ND[Notice.Type]['Region']
                dataDict['ObjectID'] = eval('Notice.%s.%sObjectID' % (ND[Notice.Type]['Table'], 'TopicID.' if 'C' in Notice.Type else '')) if Notice.Type != 'L' else ''
                dataDict['AnchorID'] = Notice.CommentInfo.ObjectID if 'C' in Notice.Type and Notice.CommentInfo else ''
                dataDict['Title'] = eval('Notice.%s.%sTitle' % (ND[Notice.Type]['Table'], 'TopicID.' if 'C' in Notice.Type else ''))[0:10] if Notice.Type != 'L' else ''
                dataDict['PageNumber'] = GetPageNumber(ND[Notice.Type]['Table'], dataDict['ObjectID'], Notice.CommentInfo if 'C' in Notice.Type and Notice.CommentInfo else '')
                dataDict['TargetURL'] = '/' + dataDict['Region'] + '/Content/' + dataDict[
                    'ObjectID'] + '/LE/' + dataDict['PageNumber'] + '/' + dataDict['AnchorID']
                dataDict['Connector'] = ND[Notice.Type]['Connector']
                dataDict['SourceUserID'] = Notice.SourceUser.id
                dataDict['SourceUserNick'] = Notice.SourceUser.Nick
                dataList.append(dataDict)
            jsondata = json.dumps(dataList, ensure_ascii=False)
            return HttpResponse(jsondata)
        else:
            return HttpResponse('None')
    else:
        return HttpResponse('login')

def NoticeDelete(request):
    if RD(request).get('IDs'):
        IDs = RD(request).get('IDs').split(',')
        if request.user.is_authenticated:
            if len(IDs) == 1:
                try:
                    QRC('Notice.objects.get(ID=%s)',
                        0, IDs[0]).delete()
                    return HttpResponse('OneDeleteOk')
                except Exception as e:
                    raise e
            else:
                for ID in IDs:
                    QRC('Notice.objects.get(ID=%s)', 0, ID).delete()
                return HttpResponse('AllDeleteOk')
    else:
        return HttpResponse('DeleteFail')

def GetPageNumber(Tabel, TopicID, Object):
    APPConf = AC()
    if Tabel == 'CommentInfo':
        CommentObjects = list(QRC("CommentInfo.objects.filter(TopicID__ObjectID=%s).order_by('-EditDate')", 0, TopicID))
        Number = CommentObjects.index(Object) + 1
        PageNumber = Number // APPConf.CommentsPageLimit if Number % APPConf.CommentsPageLimit == 0 else Number // APPConf.CommentsPageLimit + 1
        return str(PageNumber)
    else:
        return '1'
