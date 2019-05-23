from NTWebsite.MainMethods import QueryRedisCache as QRC
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
                dataDict['Region'] = Notice.Region
                dataDict['ObjectID'] = Notice.ObjectID
                dataDict['AnchorID'] = Notice.AnchorID
                dataDict['Title'] = QRC(dataDict['Region'].replace('Special', '') + 'Info.objects.get(ObjectID=%s)', None, dataDict[
                                        'ObjectID']).Title[0:10] + '...'
                dataDict['PageNumber'] = GetPageNumber(dataDict['Region'], dataDict[
                                                       'ObjectID'], dataDict['AnchorID'])
                dataDict['TargetURL'] = '/' + dataDict['Region'] + '/Content/' + dataDict[
                    'ObjectID'] + '/LE/' + dataDict['PageNumber'] + '/' + dataDict['AnchorID']
                dataDict['SourceUser'] = Notice.SourceUser.Nick
                dataList.append(dataDict)
            jsondata = json.dumps(dataList, ensure_ascii=False)
            return HttpResponse(jsondata)
        else:
            return HttpResponse('None')
    else:
        return HttpResponse('login')

def NoticeDelete(request):
    if RequestDataUnbox(request).get('IDs'):
        IDs = RequestDataUnbox(request).get('IDs').split(',')
        if request.user.is_authenticated:
            if len(IDs) == 1:
                try:
                    QRC('Notification.objects.get(ID=%s)',
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