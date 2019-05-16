from NTWebsite.improtFiles.processor_import_head import *
from NTWebsite.improtFiles.models_import_head import *
from NTWebsite.Config import AppConfig as AC
from NTWebsite.Config import DBConfig as DC


def indexView(request):
    APPConf = AC()
    return HttpResponseRedirect(APPConf.IndexURL)


def PaginatorInfoGet(objects, number, URLParams):
    if objects:
        ObjectsPaginator = Paginator(list(objects), number)
        ObjectList = Paginator(list(objects), number).page(
            int(URLParams['PageNumber']))
        Paginator_num_pages = ObjectsPaginator.num_pages
        Paginator_href = "/%s/%s/%s/%s/" % (
            URLParams['Region'], URLParams['Part'], URLParams['FilterValue'], URLParams['Order'])
        return {'ObjectList': ObjectList, 'ObjectsPaginator': ObjectsPaginator, 'Paginator_num_pages': Paginator_num_pages, 'Paginator_Href': Paginator_href}
    else:
        return {'ObjectList': [], 'ObjectsPaginator': '', 'Paginator_num_pages': 0, 'Paginator_Href': ''}


def GetNotificationCount(requestObject):
    if requestObject.user.is_authenticated:
        return str(QRC('Notification.objects.filter(TargetUser=%s).count()', None, requestObject.user))
    else:
        return '0'


def FetchTopic(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            TopicObject = QRC('TopicInfo.objects.get(ObjectID=%s)',
                              0, request.POST.get('TopicID'))
            TopicID = str(TopicObject.ObjectID)
            Title = TopicObject.Title
            Content = TopicObject.Content
            Category = TopicObject.Category.Name
            themes = []
            for theme in TopicObject.Theme.all():
                themes.append(theme.Name)
            Themes = '&'.join(themes)
            jsondata = json.dumps({'TopicID': TopicID, 'Title': Title, 'Content': Content,
                                   'Category': Category, 'Themes': Themes}, ensure_ascii=False)
            return HttpResponse(jsondata)


def PublishTopic(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            InsertDataDict = {'Title': request.POST.get('Title'),
                              'Category': request.POST.get('Category'),
                              'Content': request.POST.get('Content'),
                              'Description': request.POST.get('Description'), }
            TopicID = request.POST.get('TopicID')
            Themes = request.POST.get('Themes')
            InsertDataDict['Category'] = QRC(
                'TopicCategoryInfo.objects.get(Name=%s)', None, InsertDataDict['Category'])
            # 将主题按&分割后使用get_or_create有就返回，没有就创建了返回
            ThemeObjects = []
            for Theme in Themes.split('&'):
                ThemeObjects.append(
                    QRC('TopicThemeInfo.objects.get_or_create(Name=%s)', None, Theme)[0])
            try:
                # 放在try里面执行，避免图片被移动后，检查出标题重复的问题
                InsertDataDict['Content'] = mMs.MovePicToSavePath(
                    InsertDataDict['Content'])
                # 如果Topic有值则为编辑文章
                if TopicID:
                    mMs.RemovePicFromSavePath(
                        TopicID, InsertDataDict['Content'])
                    Topic = TopicInfo.objects.filter(
                        ObjectID=TopicID).update(**InsertDataDict)
                    Topic = TopicInfo.objects.get(ObjectID=TopicID)
                else:
                    # 不用QRC的原因是ContentText文章中的引号容易出现问题!
                    Topic = TopicInfo.objects.create(ObjectID=mMs.CreateUUIDstr(),
                                                     Title=InsertDataDict[
                                                         'Title'],
                                                     Content=InsertDataDict[
                                                         'Content'],
                                                     Description=InsertDataDict[
                                                         'Description'],
                                                     Category=InsertDataDict[
                                                         'Category'],
                                                     Publisher=request.user,)
                Topic.Theme.clear()
                Topic.Theme.add(*ThemeObjects)
                Topic.save()
                return HttpResponse('ok')
            except Exception as e:
                return HttpResponse(str(e) + "验证！")
        else:
            return HttpResponse('login')


def PublishRollCall(request):
    if request.user.is_authenticated:
        RollCallTitle = request.POST.get('RollCallTitle')
        TargetUserNick = request.POST.get('TargetUserNick')
        RollCallContent = request.POST.get('RollCallContent')
        TargetUser = QRC('User.objects.get(Nick=%s)', None, TargetUserNick)
        BlackListRecord = QRC(
            'BlackList.objects.filter(Enforceder=%s,Handler=%s)', None, request.user, TargetUser)
        if TargetUser:
            if BlackListRecord:
                return HttpResponse("用户:'" + TargetUserNick + "'" + '已经屏蔽您!')
            else:
                try:
                    NewRollCall = QRC('RollCallInfo.objects.create(Title=%s,Publisher=%s,Target=%s,ObjectID=%s)', 0,
                                      RollCallTitle, request.user, QRC('User.objects.get(Nick=%s)', None, TargetUserNick), mMs.CreateUUIDstr())
                    NewDialogue = QRC(
                        'RollCallDialogue.objects.create(RollCallID=%s,Publisher=%s,Content=%s,ObjectID=%s)', 0, NewRollCall, request.user, RollCallContent, mMs.CreateUUIDstr())
                    AddNotification('RollCall', NewRollCall.ObjectID, NewDialogue.ObjectID, QRC(
                        'User.objects.get(Nick=%s)', None, TargetUserNick), request.user)
                    return HttpResponse('publishok')
                except Exception as e:
                    if 'UNIQUE' in str(e):
                        return HttpResponse('titleisexisted')
                    else:
                        raise e
        else:
            return HttpResponse("用户:'" + TargetUserNick + "'" + '不存在!')
    else:
        return HttpResponse('login')

'''
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
                    Permission_Sizer['Vote1Status'] = 'is-active' if QRC(
                        'Attitude.objects.filter(ObjectID=%s,Point=1,Publisher=%s)', 0, item.ObjectID, request.user) else ''
                    Permission_Sizer['Vote0Status'] = 'is-active' if QRC(
                        'Attitude.objects.filter(ObjectID=%s,Point=0,Publisher=%s)', 0, item.ObjectID, request.user) else ''
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
            print(URLParams['FilterValue'])
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

def ContextConfirm(request, **Params):
    NotificationCount = GetNotificationCount(request)
    # 文章分类信息获取
    CategoryList = QRC('TopicCategoryInfo.objects.all()', None)
    # 推荐发布者信息获取
    PublisherList = QRC("PublisherList.objects.all()", None)
    # 生成上下文字典
    ContextDict = {"Layout_Sizer": Params['URLParams'],
                   "Main_URL_Sizer": {'Topic': ('is-active', '', ''), 'RollCall': ('', 'is-active', ''), 'SpecialTopic': ('', '', 'is-active'), 'UserProfile': ('', '', '')}[Params['URLParams']['Region']],
                   "ExportItem_UserInfo": Params['User'] if 'User' in Params else '',
                   "ExportList_Topic": Params['Object'] if 'Object' in Params else '',
                   "ExportList_Cards": Params['PaginatorDict']['ObjectList'] if 'PaginatorDict' in Params else '',
                   "ExportList_Categorys": CategoryList,
                   "ExportList_Publishers": PublisherList,
                   "Paginator_num_pages": Params['PaginatorDict']['Paginator_num_pages'] if 'PaginatorDict' in Params else '',
                   "Current_Pagenumber": Params['URLParams']['PageNumber'] if 'URLParams' in Params else '',
                   "Paginator_Href": Params['PaginatorDict']['Paginator_Href'] if 'PaginatorDict' in Params else '',
                   "Search_Placeholder": Params['APPConf'].TopicHotKeyWord if 'APPConf' in Params else '',
                   "NotificationCount": NotificationCount}
    return ContextDict


def CommentPackage(CommentObjects):
    if CommentObjects:
        CommentCards = []
        for CommentObject in CommentObjects:
            if CommentObject[0].Parent:
                ParentCommentObject = QRC(
                    'CommentInfo.objects.get(ObjectID=%s)', 0, CommentObject[0].Parent)
                CommentCards.append(
                    ('1', ParentCommentObject, CommentObject))
            else:
                CommentCards.append(('0', '', CommentObject))
        return CommentCards
    else:
        return 0


def ReadIPRecord(IP, ID, type):
    ReadsIP.objects.get_or_create(IP=IP, ObjectID=ID, Type=type)


def AttitudeOperate(request):
    Type = 'Topic' if request.POST.get(
        'Type') in 'SpecialTopic' else request.POST.get('Type')
    Object = QRC(Type + 'Info.objects.get('+ ('Comment' if Type == 'Comment' else 'Object') +'ID=%s)', None, request.POST.get('ObjectID'))
    Point = request.POST.get('Point')

    if request.user.is_authenticated:
        record = QRC(('Topic' if Type in 'SpecialTopic' else 'Comment') +
                     'Attitude.objects.filter(ObjectID=%s,Type=%s,Publisher=%s)', 0, Object, Type, request.user)
        if record and len(record) < 2:
            if record[0].Point == int(Point):
                record[0].delete()
                return HttpResponse('Cancel')
            else:
                record[0].Point=int(Point)
                record[0].save()
                return HttpResponse('Become')
        elif record and len(record) > 2:
            for item in record:
                item.delete() 
        else:
            QRC(('Topic' if Type in 'SpecialTopic' else 'Comment') +
                     'Attitude.objects.create(ObjectID=%s,Type=%s,Publisher=%s,Point=%s)', 0, Object, Type, request.user, int(Point))
            return HttpResponse('Confirm')
    else:
        return HttpResponse('login')


@csrf_exempt
def UploadImg(request):
    if request.method == 'POST':
        return HttpResponse(mMs.PicUploadOperate(request.FILES['upload']))


def TipOff(request):
    if request.method == 'POST':
        Type = request.POST.get('Type')
        TopicID = request.POST.get('TopicID')
        Content = request.POST.get('Content')
        if request.user.is_authenticated:
            userObject = QRC('User.objects.get(id=%s)', None, request.user.id)
            TipOffObject = QRC(
                'TipOffBox.objects.filter(ObjectID=%s,Publisher=%s)', 0, TopicID, userObject)
            if TipOffObject:
                return HttpResponse('cancel')
            else:
                QRC('TipOffBox.objects.create(ObjectID=%s, Publisher=%s, Type=%s, Content=%s)',
                    0, TopicID, userObject, Type, Content)
                return HttpResponse('success')
        else:
            return HttpResponse('login')


def Replay(request):
    if request.method == 'POST':
        temp_Map = {'Topic': 'TRCount',
                    'SpecialTopic': 'SRCount', 'RollCall': 'RCount'}
        Type = request.POST.get('Type')
        ObjectID = request.POST.get('ObjectID')
        Content = request.POST.get('Content')
        ParentID = request.POST.get('ParentID')
        if request.user.is_authenticated:
            if Type in 'SpecialTopic':
                ReplayObject = QRC('CommentInfo.objects.create(ObjectID=%s, ObjectID=%s,Content=%s,Parent=%s,Type=%s,Publisher=%s)',
                                   0, mMs.CreateUUIDstr(), ObjectID, Content, ParentID, Type, request.user)

                # AddNotification(Type, ObjectID, ReplayObject.ObjectID, QRC('CommentInfo.objects.get(ObjectID=%s)', None,
                # ParentID).Publisher if ParentID else QRC(Type +
                # 'Info.objects.get(ObjectID=%s)', None, ObjectID).Publisher,
                # request.user)
            else:
                RollCall = QRC(
                    'RollCallInfo.objects.get(ObjectID=%s)', None, ObjectID)
                ReplayObject = QRC('RollCallDialogue.objects.create(ObjectID=%s,RollCallID=%s,Content=%s,Display=%s,Publisher=%s)',
                                   0, mMs.CreateUUIDstr(), RollCall, Content, '' if RollCall.Publisher == request.user else 'right', request.user)
                if not RollCall.Publisher == request.user:
                    AddNotification(Type, ObjectID, ReplayObject.ObjectID, QRC('CommentInfo.objects.get(ObjectID=%s)', None,
                                                                               ParentID).Publisher if ParentID else QRC(Type + 'Info.objects.get(ObjectID=%s)', None, ObjectID).Publisher, request.user)
            return HttpResponse('replayok')
        else:
            return HttpResponse('login')


def Collect(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            ObjectID = request.POST.get('ObjectID')
            Type = request.POST.get('Type')
            result = QRC(
                'Collection.objects.filter(Publisher=%s,Type=%s,ObjectID=%s)', 0, request.user, Type, ObjectID)
            if not result:
                QRC('Collection.objects.create(Publisher=%s,Type=%s,ObjectID=%s)',
                    0, request.user, Type, ObjectID)
                return HttpResponse('collect')
            else:
                result[0].delete()
                return HttpResponse('cancel')
        else:
            return HttpResponse('login')


def StatisticalDataUpdata(objectStr, methodDsc):
    exec(objectStr + methodDsc)
    exec(objectStr + '.save()')


def Param(request):
    if request.method == "GET":
        KeyWord = request.GET.get('KeyWord')
        if KeyWord == 'SecretKey':
            APPConf = AC()
            jsondata = json.dumps(
                [APPConf.SecretKey, APPConf.SecretVI], ensure_ascii=False)
            return HttpResponse(jsondata)
        else:
            pass


def Login(request):
    if request.method == 'POST':
        # 注册信息获取
        username = mMs.Decrypt(mMs.DecodeWithBase64(
            request.POST.get('username')))
        userpassword = mMs.Decrypt(
            mMs.DecodeWithBase64(request.POST.get('password')))
        user = auth.authenticate(username=username, password=userpassword)

        if user:
            login(request, user)
            return HttpResponse(True)
        else:
            return HttpResponse("")
# 注册界面


def Regist(request):
    APPConf = AC()
    if request.method == 'POST':
        username = mMs.Decrypt(mMs.DecodeWithBase64(
            request.POST.get('username')))
        usernickname = mMs.Decrypt(mMs.DecodeWithBase64(
            request.POST.get('usernickname')))
        password = mMs.Decrypt(mMs.DecodeWithBase64(
            request.POST.get('password')))
        email = mMs.Decrypt(mMs.DecodeWithBase64(request.POST.get('email')))
        try:
                # 这里通过前端注册账号一定要是要create_user 不然后期登录的时候
                # auth.authenticate无法验证用户名和密码
            newUser = User.objects.create_user(
                username, Nick=usernickname, password=password, email=email)

            newUser.Avatar = mMs.UserAvatarOperation(request.POST.get(
                'userimagedata'), request.POST.get('userimageformat'), APPConf.DefaultAvatar.url.replace(settings.MEDIA_URL, ''))['Path']
            newUser.save()
            return HttpResponse('ok')

        except Exception as e:
            return HttpResponse(str(e))


def Logout(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            auth.logout(request)
            return HttpResponse('Logout')
        else:
            return HttpResponse('logouted')
    else:
        return HttpResponse('not get')


def AddNotification(Region, ObjectID, AnchorID, TargetUser, SourceUser):
    try:
        QRC('Notification.objects.create(ID=%s, Region=%s, ObjectID=%s, AnchorID=%s, TargetUser=%s, SourceUser=%s)',
            0, mMs.CreateUUIDstr(), Region, ObjectID, AnchorID, TargetUser, SourceUser)
    except Exception as e:
        raise e


@csrf_exempt
def NotificationInfo(request):
    print(request.method)
    if request.method == 'GET':
        if request.user.is_authenticated:
            try:
                NotificationObjects = QRC(
                    'Notification.objects.filter(TargetUser=%s)', 0, request.user)
                if NotificationObjects:
                    dataList = []
                    for Object in NotificationObjects:
                        dataDict = {}
                        dataDict['ID'] = str(Object.ID)
                        dataDict['Region'] = Object.Region
                        dataDict['ObjectID'] = Object.ObjectID
                        dataDict['AnchorID'] = Object.AnchorID
                        dataDict['Title'] = QRC(dataDict['Region'].replace('Special', '') + 'Info.objects.get(ObjectID=%s)', None, dataDict[
                                                'ObjectID']).Title[0:10] + '...'
                        dataDict['PageNumber'] = GetPageNumber(dataDict['Region'], dataDict[
                                                               'ObjectID'], dataDict['AnchorID'])
                        dataDict['TargetURL'] = '/' + dataDict['Region'] + '/Content/' + dataDict[
                            'ObjectID'] + '/LE/' + dataDict['PageNumber'] + '/' + dataDict['AnchorID']
                        dataDict['SourceUser'] = Object.SourceUser.Nick
                        dataList.append(dataDict)
                    jsondata = json.dumps(dataList, ensure_ascii=False)
                    return HttpResponse(jsondata)
                else:
                    return HttpResponse('None')
            except Exception as e:
                raise e
        else:
            return HttpResponse('login')
    else:
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
                        QRC('Notification.objects.get(ID=%s)', 0, ID).delete()
                    return HttpResponse('AllDeleteOk')
        else:
            return HttpResponse('DeleteFail')


def RequestDataUnbox(request):
    qd = QueryDict(request.body)
    data_dict = {k: v[0] if len(v) == 1 else v for k, v in qd.lists()}
    return data_dict


def GetPageNumber(Region, ObjectID, AnchorID):
    APPConf = AC()
    if Region in 'SpecialTopic':
        CommentObjects = QRC(
            "CommentInfo.objects.filter(ObjectID=%s).order_by('-EditDate')", 0, ObjectID)
        Number = 0
        for CommentObject in CommentObjects:
            Number += 1
            if str(CommentObject.ObjectID) == AnchorID:
                break
        PageNumber = Number // APPConf.CommentsPageLimit if Number % APPConf.CommentsPageLimit == 0 else Number // APPConf.CommentsPageLimit + 1
        return str(PageNumber)
    else:
        return '1'


def BlackListOperation(request):
    if request.method == 'POST':
        UserID = request.POST.get('UserID')
        Operation = request.POST.get('Operation')
        UserObject = QRC('User.objects.get(id=%s)', None, UserID)
        if request.user.is_authenticated and Operation == 'add':
            try:
                if not QRC('BlackList.objects.filter(Enforceder=%s, Handler=%s)', 0, UserObject, request.user):
                    BlackList.objects.create(ID=mMs.CreateUUIDstr(
                    ), Enforceder=UserObject, Handler=request.user)
                return HttpResponse('add')
            except Exception as e:
                return HttpResponse(e)

        elif request.user.is_authenticated and Operation == 'delete':
            try:
                QRC('BlackList.objects.get(Enforceder=%s,Handler=%s)',
                    0, UserObject, request.user).delete()
                return HttpResponse('delete')
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse('login')


def UserLink(request):
    Operation = request.POST.get('Operation')
    if request.method == 'POST':
        if request.user.is_authenticated:
            UserID = request.POST.get('UserID')
            UserObject = QRC('User.objects.get(id=%s)', None, UserID)
            try:
                if Operation == 'add':
                    QRC('UserLink.objects.get_or_create(UserBeLinked=%s,UserLinking=%s)',
                        0, UserObject, request.user)
                    #UserLink.objects.get_or_create(UserBeLinked=UserObject, UserLinking=request.user)
                    return HttpResponse('add')
                elif Operation == 'delete':
                    QRC('UserLink.objects.get(UserBeLinked=%s,UserLinking=%s)',
                        0, UserObject, request.user).delete()
                    return HttpResponse('delete')
            except Exception as e:
                return HttpResponse(e)
        else:
            return HttpResponse('login')


def UserProfileUpdate(request):
    APPConf = AC()
    if request.method == 'POST':
        UserImageData = request.POST.get('UserImageData')
        UserImageFormat = request.POST.get('UserImageFormat')
        UserNickName = request.POST.get('UserNickName')
        UserDescription = request.POST.get('UserDescription')
        UserSex = request.POST.get('UserSex')
        UserConstellation = request.POST.get('UserConstellation')
        UserEmail = request.POST.get('UserEmail')
        UserRegion = request.POST.get('UserRegion')
        userObject = QRC('User.objects.get(Nick=%s)', 0, request.user.Nick)
        print('UserImageFormat', UserImageFormat)
        if QRC('User.objects.get(Nick=%s)', 0, UserNickName) and QRC('User.objects.get(Nick=%s)', 0, UserNickName) != request.user:
            return HttpResponse('Nick')
        else:
            UploadImage_Operated = ''
            UploadImage_Operated = mMs.UserAvatarOperation(
                UserImageData, UserImageFormat, userObject.Avatar)
            userObject.Avatar = UploadImage_Operated['Path']
            userObject.Nick = UserNickName
            userObject.Sex = UserSex
            userObject.Region = UserRegion
            userObject.email = UserEmail
            userObject.Description = UserDescription
            userObject.Constellation = UserConstellation
            userObject.save()
            return HttpResponse(UploadImage_Operated['Status'])


if __name__ == "__main__":
    print('%s' % 'abc')
