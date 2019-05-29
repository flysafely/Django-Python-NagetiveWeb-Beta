from django.db.models.signals import post_save, post_delete, pre_save, pre_delete
from django.dispatch import receiver
from NTWebsite.MainMethods import QueryRedisCache as QRC
from NTWebsite.improtFiles.models_import_head import *
from NTWebsite import MainMethods as mMs


@receiver(post_save, dispatch_uid=User)
def user_create(sender, instance, created, **kwargs):
    if created and isinstance(instance,User): # instance 是一个log对象,里面的user属性才是存储的新建用户对象实例
        if instance.is_superuser:
            mMs.QueryFilterCreate()


@receiver(post_save, dispatch_uid=TopicInfo)
def topic_create(sender, instance, created, **kwargs):
    if created and isinstance(instance, TopicInfo):
        mMs.CounterOperate(
            instance.Publisher, 'TCount' if instance.Type == 'Topic' else 'SCount', '+')
        for item in QRC('UserLink.objects.filter(UserBeLinked=%s)', None, instance.Publisher):
            mMs.AddNotification('TP' if instance.Type == 'Topic' else 'SP', instance, instance.Publisher, item.UserLinking)

@receiver(post_delete, dispatch_uid=TopicInfo)
def topic_delete(sender, instance, **kwargs):
    if isinstance(instance, TopicInfo):
        mMs.CounterOperate(
            instance.Publisher, 'TCount' if instance.Type == 'Topic' else 'SCount', '-')


@receiver(post_save, dispatch_uid=RollCallInfo)
def rollcall_create(sender, instance, created, **kwargs):
    if created and isinstance(instance, RollCallInfo):
        mMs.CounterOperate(instance.Publisher, 'RCount', '+')
        mMs.AddNotification('R', instance, instance.Publisher, instance.Target)

@receiver(post_delete, dispatch_uid=RollCallInfo)
def rollcall_delete(sender, instance, **kwargs):
    if isinstance(instance, RollCallInfo):
        mMs.CounterOperate(instance.Publisher, 'RCount', '-')


@receiver(post_save, dispatch_uid=RollCallDialogue)
def rollcalldialogue_create(sender, instance, created, **kwargs):
    if created and isinstance(instance, RollCallDialogue):
        mMs.CounterOperate(instance.RollCallID, 'Comment', '+')
        mMs.CounterOperate(instance.Publisher, 'RRCount', '+')
        if not instance.RollCallID.Publisher == instance.Publisher:
            mMs.AddNotification('RD', instance.RollCallID, instance.Publisher, instance.RollCallID.Target)

@receiver(pre_delete, dispatch_uid=RollCallDialogue)
def rollcalldialogue_delete(sender, instance, **kwargs):
    if isinstance(instance, RollCallDialogue):
        mMs.CounterOperate(instance.RollCallID, 'Comment', '-')
        mMs.CounterOperate(instance.Publisher, 'RRCount', '-')


@receiver(post_save, dispatch_uid=CommentInfo)
def comment_create(sender, instance, created, **kwargs):
    if created and isinstance(instance, CommentInfo):
        mMs.CounterOperate(instance.TopicID, 'Comment', '+')
        mMs.CounterOperate(
            instance.Publisher, 'TRCount' if instance.TopicID.Type == 'Topic' else 'SRCount', '+')
        if instance.TopicID.Type == 'Topic':
            mMs.AddNotification('TCR' if instance.Parent else 'TC', instance, instance.Publisher, instance.Parent.Publisher if instance.Parent else instance.TopicID.Publisher)
        else:
            mMs.AddNotification('SCR' if instance.Parent else 'SC', instance, instance.Publisher, instance.Parent.Publisher if instance.Parent else instance.TopicID.Publisher)


@receiver(post_delete, dispatch_uid=CommentInfo)
def comment_delete(sender, instance, **kwargs):
    if isinstance(instance, CommentInfo):
        mMs.CounterOperate(instance.TopicID, 'Comment', '-')
        mMs.CounterOperate(
            instance.Publisher, 'TRCount' if instance.Type == 'Topic' else 'SRCount', '-')


@receiver(post_save, dispatch_uid=Collect)
def collect_create(sender, instance, created, **kwargs):
    if created and isinstance(instance, Collect):
        mMs.CounterOperate(instance.ObjectID, 'Collect', '+')

@receiver(post_delete, dispatch_uid=Collect)
def collect_delete(sender, instance, **kwargs):
    if isinstance(instance, Collect):
        mMs.CounterOperate(instance.ObjectID, 'Collect', '-')


@receiver(post_save, dispatch_uid=Concern)
def concern_create(sender, instance, created, **kwargs):
    if created and isinstance(instance, Concern):
        mMs.CounterOperate(instance.ObjectID, 'Collect', '+')

@receiver(post_delete, dispatch_uid=Concern)
def concern_delete(sender, instance, **kwargs):
    if isinstance(instance, Concern):
        mMs.CounterOperate(instance.ObjectID, 'Collect', '-')


@receiver(post_save, dispatch_uid=Circusee)
def circusee_create(sender, instance, created, **kwargs):
    if created and isinstance(instance, Circusee):
        mMs.CounterOperate(instance.ObjectID, 'Collect', '+')

@receiver(post_delete, dispatch_uid=Circusee)
def circusee_delete(sender, instance, **kwargs):
    if isinstance(instance, Circusee):
        mMs.CounterOperate(instance.ObjectID, 'Collect', '-')


@receiver(post_save, dispatch_uid=UserLink)
def userlink_create(sender, instance, created, **kwargs):
    if created and isinstance(instance, UserLink):
        mMs.CounterOperate(instance.UserBeLinked, 'FansCount', '+')
        mMs.CounterOperate(instance.UserLinking, 'FocusCount', '+')
        mMs.AddNotification('L', instance, instance.UserLinking, instance.UserBeLinked)

@receiver(post_delete, dispatch_uid=UserLink)
def userlink_delete(sender, instance, **kwargs):
    if isinstance(instance, UserLink):
        mMs.CounterOperate(instance.UserBeLinked, 'FansCount', '-')
        mMs.CounterOperate(instance.UserLinking, 'FocusCount', '-')


@receiver(post_save, dispatch_uid=TopicAttitude)
def TopicAttitude_create(sender, instance, created, **kwargs):
    if created and isinstance(instance, TopicAttitude):
        mMs.CounterOperate(instance.ObjectID, 'Like' if instance.Point == 1 else 'Dislike', '+')
        mMs.AddNotification('TAL' if instance.Point == 1 else 'TAD', instance.ObjectID, instance.Publisher, instance.ObjectID.Publisher)
    elif (not created) and isinstance(instance, TopicAttitude):
        mMs.CounterOperate(instance.ObjectID, 'Like' if int(instance.Point) == 1 else 'Dislike', '+')
        mMs.CounterOperate(instance.ObjectID, 'Like' if abs(int(instance.Point) - 1) == 1 else 'Dislike', '-')
        mMs.AddNotification('TAL' if instance.Point == 1 else 'TAD', instance.ObjectID, instance.Publisher, instance.ObjectID.Publisher)


@receiver(pre_delete, dispatch_uid=TopicAttitude)
def TopicAttitude_delete(sender, instance, **kwargs):
    if isinstance(instance, TopicAttitude):
        mMs.CounterOperate(instance.ObjectID, 'Like' if int(instance.Point) == 1 else 'Dislike', '-')


@receiver(post_save, dispatch_uid=CommentAttitude)
def CommentAttitude_create(sender, instance, created, **kwargs):
    if created and isinstance(instance, CommentAttitude):
        mMs.CounterOperate(instance.ObjectID, 'Like' if instance.Point == 1 else 'Dislike', '+')
        mMs.AddNotification('CAL' if instance.Point == 1 else 'CAD', instance.ObjectID, instance.Publisher, instance.ObjectID.Publisher)
    elif (not created) and isinstance(instance, CommentAttitude):
        mMs.CounterOperate(instance.ObjectID, 'Like' if int(instance.Point) == 1 else 'Dislike', '+')
        mMs.CounterOperate(instance.ObjectID, 'Like' if abs(int(instance.Point) - 1) == 1 else 'Dislike', '-')
        mMs.AddNotification('CAL' if instance.Point == 1 else 'CAD', instance.ObjectID, instance.Publisher, instance.ObjectID.Publisher)

@receiver(pre_delete, dispatch_uid=CommentAttitude)
def CommentAttitude_delete(sender, instance, **kwargs):
    if isinstance(instance, CommentAttitude):
        mMs.CounterOperate(instance.ObjectID, 'Like' if int(instance.Point) == 1 else 'Dislike', '-')
