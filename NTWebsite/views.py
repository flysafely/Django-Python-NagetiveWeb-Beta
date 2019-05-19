from NTWebsite.improtFiles.views_import_head import *
from NTWebsite.improtFiles.models_import_head import *


def Launcher(request, **URLParams):
    # 获取查询模式中的对应方法String
    DBConf = DC(
        '-'.join([URLParams['Region'], URLParams['Part'], URLParams['Order']]))
    MethodSwitcher = eval(DBConf.MethodString)
    # 执行对应的方法
    return MethodSwitcher(request, DBConf, AC(), URLParams)


def TopicsInfoGet(request, DBConf, APPConf, URLParams):
    # 获取符合条件的文章对象并且获取权限
    TopicObjects = A.Empower(URLParams['Region'], QRC(
        DBConf.QueryString, None, URLParams['Region'], URLParams['FilterValue']), request)
    print(TopicObjects[0])
    # 多对多数据反向获取
    #tag = TopicThemeInfo.objects.get(TT_Name = '测试标签1')
    # print(tag.Topic.all())
    # 注意:在模板中可以通过TopicList[0].TS_Topic.TI_Theme.all 获取所有的多对多 对象

    # 文章分页器
    PaginatorDict = P.PaginatorInfoGet(
        TopicObjects, APPConf.TopicsPageLimit, URLParams)
    # 返回上下文信息
    return render(request, DBConf.Template, P.ContextConfirm(request, URLParams=URLParams, Object=TopicObjects, PaginatorDict=PaginatorDict, APPConf=APPConf))


def TopicContentInfoGet(request, DBConf, APPConf, URLParams):
    # 分享链入统计
    if URLParams['ExtraParam'] == 'Share':
        mMs.CounterOperate(QRC('TopicInfo.objects.get(ObjectID=%s)',
                             None, URLParams['FilterValue']), 'Share', '+')

    # 阅读量、热度统计
    if not QRC('ReadsIP.objects.filter(IP=%s,ObjectID=%s)', None, mMs.GetUserIP(request), URLParams['FilterValue']):
        P.ReadIPRecord(mMs.GetUserIP(request),
                       URLParams['FilterValue'], URLParams['Region'])
        mMs.CounterOperate(QRC('TopicInfo.objects.get(ObjectID=%s)',
                               0, URLParams['FilterValue']), 'Hot', '+')
    # 获取指定文章对象

    #print('获取指定文章对象', QRC(DBConf.QueryString, None, URLParams['FilterValue']))
    TopicObject = A.Empower(URLParams['Region'], QRC(
        DBConf.QueryString, None, URLParams['FilterValue']), request)
    # 获取评论对象
    CommentObjects = P.CommentPackage(A.Empower('Comment',
                                                QRC("CommentInfo.objects.filter(TopicID=%s).order_by('-EditDate')",
                                                    None,
                                                    TopicObject[0][0]),
                                                request))
    # 评论分页器
    PaginatorDict = P.PaginatorInfoGet(
        CommentObjects, APPConf.CommentsPageLimit, URLParams)

    # 返回上下文信息
    return render(request, DBConf.Template, P.ContextConfirm(request, URLParams=URLParams, Object=TopicObject, PaginatorDict=PaginatorDict, APPConf=APPConf))


def SearchInfoGet(request, DBConf, APPConf, URLParams):
    # 获取符合条件的文章对象并且获取权限
    ResultObjects = A.Empower(URLParams['Part'] if URLParams['Part'] != 'User' else 'UserProfileInfo', QRC(
        DBConf.QueryString, None, URLParams['FilterValue'], URLParams['FilterValue'], URLParams['Part']) if URLParams['Part'] in 'SpecialTopic' else QRC(
        DBConf.QueryString, None, URLParams['FilterValue']), request)
    # 文章分页器
    PaginatorDict = P.PaginatorInfoGet(
        ResultObjects, APPConf.TopicsPageLimit, URLParams)
    # 返回上下文信息
    return render(request, DBConf.Template, P.ContextConfirm(request, URLParams=URLParams, PaginatorDict=PaginatorDict, APPConf=APPConf))


def RollCallsInfoGet(request, DBConf, APPConf, URLParams):
    RollCallObjects = A.Empower(URLParams['Region'], QRC(
        DBConf.QueryString, None, URLParams['FilterValue']), request)
    PaginatorDict = P.PaginatorInfoGet(
        RollCallObjects, APPConf.TopicsPageLimit, URLParams)
    return render(request, DBConf.Template, P.ContextConfirm(request, URLParams=URLParams, PaginatorDict=PaginatorDict, APPConf=APPConf))


def RollCallInfoContentInfoGet(request, DBConf, APPConf, URLParams):
    # 分享链入统计
    if URLParams['ExtraParam'] == 'Share':
        mMs.CounterOperate(QRC('RollCallInfo.objects.get(ObjectID=%s)',
                               None, URLParams['FilterValue']), 'Share', '+')
    # 阅读量、热度统计
    if not QRC('ReadsIP.objects.filter(IP=%s,ObjectID=%s)', None, mMs.GetUserIP(request), URLParams['FilterValue']):
        P.ReadIPRecord(mMs.GetUserIP(request),
                       URLParams['FilterValue'], URLParams['Region'])
        mMs.CounterOperate(QRC('RollCallInfo.objects.get(ObjectID=%s)',
                               0, URLParams['FilterValue']), 'Hot', '+')
    # 获取指定文章对话对象
    RollCallObject = A.Empower('RollCall', QRC('RollCallInfo.objects.get(ObjectID=%s)', None, URLParams['FilterValue']), request)[0]
    # 获取指定文章对话对象
    DialogueObject = QRC(DBConf.QueryString, None, URLParams['FilterValue'])
    # 分页器
    # 返回上下文信息
    return render(request, DBConf.Template, P.ContextConfirm(request, URLParams=URLParams, Object=DialogueObject, MainObject= RollCallObject, APPConf=APPConf))


def UserProfileInfoGet(request, DBConf, APPConf, URLParams):
    # 获取用户主题信息
    TargetUser = A.Empower('UserProfile', QRC(
        'User.objects.get(id=%s)', None, URLParams['FilterValue']), request)
    # 获取用户Selection内容
    # 直接获取文章
    if URLParams['Part'] in 'SpecialTopic':
        Objects = A.Empower(URLParams['Part'], QRC(
            DBConf.QueryString, None, URLParams['FilterValue']), request)
    elif URLParams['Part'] in ['Comment']:
        Topics = []
        for item in QRC(DBConf.QueryString, None, URLParams['FilterValue']):
            if item != None:
                Topics.append(item.TopicID)
        Objects = A.Empower('Topic', list(set(Topics)), request)
    elif URLParams['Part'] in ['TopicLike','TopicDislike','CommentLike','CommentDislike']:
        Topics = []
        for item in QRC(DBConf.QueryString, None, URLParams['FilterValue']):
            if item != None:
                Topics.append(item.ObjectID if URLParams['Part'] in ['TopicLike','TopicDislike'] else item.ObjectID.TopicID)
        Objects = A.Empower('Topic', list(set(Topics)), request)
    elif URLParams['Part'] in ['Collect', 'Concern', 'Circusee']:
        ObjectType = {'Collect':'Topic', 'Concern':'SpecialTopic', 'Circusee':'RollCall'}
        Topics = []
        for item in QRC(DBConf.QueryString, None, URLParams['FilterValue']):
            if item != None:
                Topics.append(item.ObjectID)
        Objects = A.Empower(ObjectType[URLParams['Part']], list(set(Topics)), request)
    elif URLParams['Part'] in ['Focus', 'Fans']:
        Objects = []
        for UserObject in QRC(DBConf.QueryString, None, QRC('User.objects.get(id=%s)', 0, URLParams['FilterValue'])):
            if UserObject != None:
                Objects.append(UserObject)
    # 分页器
    PaginatorDict = P.PaginatorInfoGet(
        Objects, APPConf.CommonPageLimit, URLParams)

    return render(request, DBConf.Template, P.ContextConfirm(request, User=TargetUser, PaginatorDict=PaginatorDict, URLParams=URLParams, APPConf=APPConf))

if __name__ == "__main__":
    print('%s')
