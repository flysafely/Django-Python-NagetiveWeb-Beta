from django.db.models.signals import post_save, post_delete, pre_save, pre_delete
from NTWebsite.MainMethods import QueryRedisCache as QRC
from NTWebsite.improtFiles.models_import_head import *
from NTWebsite import MainMethods as mMs
from django.dispatch import receiver

@receiver(post_save, dispatch_uid=User)
def user_create_handler(sender, instance, created, **kwargs):
    if created and isinstance(instance, User):
        print('新建超级账户：',instance.username)
        mMs.QueryFilterCreate()


@receiver(post_save, dispatch_uid=TopicInfo)
def topic_create_handler(sender, instance, created, **kwargs):
    if created and isinstance(instance, TopicInfo):
        mMs.CounterOperate(
            instance.Publisher, 'TCount' if instance.Type == 'Topic' else 'SCount', '+')

@receiver(post_delete, dispatch_uid=TopicInfo)
def topic_delete_handler(sender, instance, **kwargs):
    if isinstance(instance, TopicInfo):
        mMs.CounterOperate(
            instance.Publisher, 'TCount' if instance.Type == 'Topic' else 'SCount', '-')


@receiver(post_save, dispatch_uid=RollCallInfo)
def rollcall_create_handler(sender, instance, created, **kwargs):
    if created and isinstance(instance, RollCallInfo):
        mMs.CounterOperate(instance.Publisher, 'RCount', '+')
        mMs.AddNotification('R', instance)

@receiver(post_delete, dispatch_uid=RollCallInfo)
def rollcall_delete_handler(sender, instance, **kwargs):
    if isinstance(instance, RollCallInfo):
        mMs.CounterOperate(instance.Publisher, 'RCount', '-')


@receiver(post_save, dispatch_uid=RollCallDialogue)
def rollcalldialogue_create_handler(sender, instance, created, **kwargs):
    if created and isinstance(instance, RollCallDialogue):
        mMs.CounterOperate(instance.RollCallID, 'Comment', '+')
        mMs.CounterOperate(instance.Publisher, 'RRCount', '+')

@receiver(pre_delete, dispatch_uid=RollCallDialogue)
def rollcalldialogue_delete_handler(sender, instance, **kwargs):
    if isinstance(instance, RollCallDialogue):
        mMs.CounterOperate(instance.RollCallID, 'Comment', '-')
        mMs.CounterOperate(instance.Publisher, 'RRCount', '-')


@receiver(post_save, dispatch_uid=CommentInfo)
def comment_create_handler(sender, instance, created, **kwargs):
    if created and isinstance(instance, CommentInfo):
        mMs.CounterOperate(instance.TopicID, 'Comment', '+')
        mMs.CounterOperate(
            instance.Publisher, 'TRCount' if instance.Type == 'Topic' else 'SRCount', '+')
        mMs.AddNotification('CR' if instance.Parent else 'C', instance)

@receiver(post_delete, dispatch_uid=CommentInfo)
def comment_delete_handler(sender, instance, **kwargs):
    if isinstance(instance, CommentInfo):
        mMs.CounterOperate(instance.TopicID, 'Comment', '-')
        mMs.CounterOperate(
            instance.Publisher, 'TRCount' if instance.Type == 'Topic' else 'SRCount', '-')


@receiver(post_save, dispatch_uid=Collect)
def collect_create_handler(sender, instance, created, **kwargs):
    if created and isinstance(instance, Collect):
        mMs.CounterOperate(instance.ObjectID, 'Collect', '+')

@receiver(post_delete, dispatch_uid=Collect)
def collect_delete_handler(sender, instance, **kwargs):
    if isinstance(instance, Collect):
        mMs.CounterOperate(instance.ObjectID, 'Collect', '-')


@receiver(post_save, dispatch_uid=Concern)
def concern_create_handler(sender, instance, created, **kwargs):
    if created and isinstance(instance, Concern):
        mMs.CounterOperate(instance.ObjectID, 'Collect', '+')

@receiver(post_delete, dispatch_uid=Concern)
def concern_delete_handler(sender, instance, **kwargs):
    if isinstance(instance, Concern):
        mMs.CounterOperate(instance.ObjectID, 'Collect', '-')


@receiver(post_save, dispatch_uid=Circusee)
def circusee_create_handler(sender, instance, created, **kwargs):
    if created and isinstance(instance, Circusee):
        mMs.CounterOperate(instance.ObjectID, 'Collect', '+')

@receiver(post_delete, dispatch_uid=Circusee)
def circusee_delete_handler(sender, instance, **kwargs):
    if isinstance(instance, Circusee):
        mMs.CounterOperate(instance.ObjectID, 'Collect', '-')


@receiver(post_save, dispatch_uid=UserLink)
def userlink_create_handler(sender, instance, created, **kwargs):
    if created and isinstance(instance, UserLink):
        mMs.CounterOperate(instance.UserBeLinked, 'FansCount', '+')
        mMs.CounterOperate(instance.UserLinking, 'FocusCount', '+')
        mMs.AddNotification('L', instance)

@receiver(post_delete, dispatch_uid=UserLink)
def userlink_delete_handler(sender, instance, **kwargs):
    if isinstance(instance, UserLink):
        mMs.CounterOperate(instance.UserBeLinked, 'FansCount', '-')
        mMs.CounterOperate(instance.UserLinking, 'FocusCount', '-')


@receiver(post_save, dispatch_uid=TopicAttitude)
def TopicAttitude_create_handler(sender, instance, created, **kwargs):
    if created and isinstance(instance, TopicAttitude):
        print("Topic Create Point")
        mMs.CounterOperate(instance.ObjectID, 'Like' if instance.Point == 1 else 'Dislike', '+')
        mMs.AddNotification('TAL' if instance.Point == 1 else 'TAD', instance)
    elif (not created) and isinstance(instance, TopicAttitude):
        mMs.CounterOperate(instance.ObjectID, 'Like' if int(instance.Point) == 1 else 'Dislike', '+')
        mMs.CounterOperate(instance.ObjectID, 'Like' if abs(int(instance.Point) - 1) == 1 else 'Dislike', '-')
        mMs.AddNotification('TAL' if instance.Point == 1 else 'TAD', instance)


@receiver(pre_delete, dispatch_uid=TopicAttitude)
def TopicAttitude_delete_handler(sender, instance, **kwargs):
    if isinstance(instance, TopicAttitude):
        mMs.CounterOperate(instance.ObjectID, 'Like' if int(instance.Point) == 1 else 'Dislike', '-')


@receiver(post_save, dispatch_uid=CommentAttitude)
def CommentAttitude_create_handler(sender, instance, created, **kwargs):
    if created and isinstance(instance, CommentAttitude):
        print("Comment Create Point")
        mMs.CounterOperate(instance.ObjectID, 'Like' if instance.Point == 1 else 'Dislike', '+')
        mMs.AddNotification('CAL' if instance.Point == 1 else 'CAD', instance)
    elif (not created) and isinstance(instance, CommentAttitude):
        mMs.CounterOperate(instance.ObjectID, 'Like' if int(instance.Point) == 1 else 'Dislike', '+')
        mMs.CounterOperate(instance.ObjectID, 'Like' if abs(int(instance.Point) - 1) == 1 else 'Dislike', '-')
        mMs.AddNotification('CAL' if instance.Point == 1 else 'CAD', instance)

@receiver(pre_delete, dispatch_uid=CommentAttitude)
def CommentAttitude_delete_handler(sender, instance, **kwargs):
    if isinstance(instance, CommentAttitude):
        mMs.CounterOperate(instance.ObjectID, 'Like' if int(instance.Point) == 1 else 'Dislike', '-')
