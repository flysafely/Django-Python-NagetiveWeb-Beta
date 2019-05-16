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
    TopicObjects = A.PermissionConfirm(URLParams['Part'], QRC(
        DBConf.QueryString, None, URLParams['Region'], URLParams['FilterValue']), request, URLParams)
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
    print('获取指定文章对象',QRC(DBConf.QueryString, None, URLParams['FilterValue']))
    TopicObject = A.PermissionConfirm(URLParams['Part'], QRC(
        DBConf.QueryString, None, URLParams['FilterValue']), request, URLParams)
    # 获取评论对象
    print('************',TopicObject[0][0])
    CommentObjects = P.CommentPackage(A.PermissionConfirm(URLParams['Part'],
                                                          QRC("CommentInfo.objects.filter(TopicID=%s).order_by('-EditDate')",
                                                              None,
                                                              TopicObject[0][0]),
                                                          request,
                                                          URLParams))
    # 评论分页器
    PaginatorDict = P.PaginatorInfoGet(
        CommentObjects, APPConf.CommentsPageLimit, URLParams)

    # 返回上下文信息
    return render(request, DBConf.Template, P.ContextConfirm(request, URLParams=URLParams, Object=TopicObject, PaginatorDict=PaginatorDict, APPConf=APPConf))


def SearchInfoGet(request, DBConf, APPConf, URLParams):
    # 获取符合条件的文章对象并且获取权限
    ResultObjects = A.PermissionConfirm(URLParams['Part'] if URLParams['Part'] != 'User' else 'UserProfileInfo', QRC(
        DBConf.QueryString, None, URLParams['FilterValue'], URLParams['FilterValue'], URLParams['Part']) if URLParams['Part'] in 'SpecialTopic' else QRC(
        DBConf.QueryString, None, URLParams['FilterValue']), request, URLParams)
    # 文章分页器
    PaginatorDict = P.PaginatorInfoGet(
        ResultObjects, APPConf.TopicsPageLimit, URLParams)
    # 返回上下文信息
    return render(request, DBConf.Template, P.ContextConfirm(request, URLParams=URLParams, PaginatorDict=PaginatorDict, APPConf=APPConf))


def RollCallsInfoGet(request, DBConf, APPConf, URLParams):
    RollCallObjects = A.PermissionConfirm(URLParams['Part'], QRC(
        DBConf.QueryString, None, URLParams['FilterValue']), request, URLParams)
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
    # 获取指定文章对象
    DialogueObject = A.PermissionConfirm(URLParams['Part'], QRC(
        DBConf.QueryString, None, URLParams['FilterValue']), request, URLParams)
    # 分页器
    # 返回上下文信息
    return render(request, DBConf.Template, P.ContextConfirm(request, URLParams=URLParams, Object=DialogueObject, APPConf=APPConf))


def UserProfileInfoGet(request, DBConf, APPConf, URLParams):
    # 获取用户主题信息
    TargetUser = A.PermissionConfirm('UserProfileInfo', QRC(
        'User.objects.get(id=%s)', None, URLParams['FilterValue']), request, URLParams)
    # 获取用户Selection内容
    # 直接获取文章
    if URLParams['Part'] in 'SpecialTopic':
        Objects = A.PermissionConfirm(URLParams['Region'], QRC(
            DBConf.QueryString, None, URLParams['FilterValue']), request, URLParams)
    elif URLParams['Part'] in ['Commit', 'Like', 'Dislike', 'Collect', 'Concern', 'Circusee']:
        Topics = []
        for item in QRC(DBConf.QueryString, None, URLParams['FilterValue']):
            Object = QRC('TopicInfo.objects.get(ObjectID=%s)' if URLParams[
                         'Part'] != 'Circusee' else 'RollCallInfo.objects.get(ObjectID=%s)', 0, item.ObjectID)
            if Object != None:
                Topics.append(Object)
        Objects = A.PermissionConfirm(
            URLParams['Region'], set(Topics), request, URLParams)
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
