from django.db.models.signals import post_save, post_delete, pre_save, pre_delete
from NTWebsite.MainMethods import QueryRedisCache as QRC
from NTWebsite.improtFiles.models_import_head import *
from NTWebsite import MainMethods as mMs
from django.dispatch import receiver


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
        mMs.CounterOperate(QRC('TopicInfo.objects.get(ObjectID=%s)',
                               0, instance.ObjectID.replace('-', '')), 'Comment', '+')
        mMs.CounterOperate(
            instance.Publisher, 'TRCount' if instance.Type == 'Topic' else 'SRCount', '+')


@receiver(post_delete, dispatch_uid=CommentInfo)
def comment_delete_handler(sender, instance, **kwargs):
    if isinstance(instance, CommentInfo):
        mMs.CounterOperate(QRC('TopicInfo.objects.get(ObjectID=%s)',
                               0, instance.ObjectID.replace('-', '')), 'Comment', '-')
        mMs.CounterOperate(
            instance.Publisher, 'TRCount' if instance.Type == 'Topic' else 'SRCount', '-')


@receiver(post_save, dispatch_uid=Collection)
def collection_create_handler(sender, instance, created, **kwargs):
    if created and isinstance(instance, Collection):
        mMs.CounterOperate(QRC((instance.Type if instance.Type not in 'SpecialTopic' else 'Topic') +
                               'Info.objects.get(ObjectID=%s)', 0, instance.ObjectID.replace('-', '')), 'Collect', '+')


@receiver(post_delete, dispatch_uid=Collection)
def collection_delete_handler(sender, instance, **kwargs):
    if isinstance(instance, Collection):
        mMs.CounterOperate(QRC((instance.Type if instance.Type not in 'SpecialTopic' else 'Topic') +
                               'Info.objects.get(ObjectID=%s)', 0, instance.ObjectID.replace('-', '')), 'Collect', '-')


@receiver(post_save, dispatch_uid=UserLink)
def userlink_create_handler(sender, instance, created, **kwargs):
    if created and isinstance(instance, UserLink):
        mMs.CounterOperate(instance.UserBeLinked, 'FansCount', '+')
        mMs.CounterOperate(instance.UserLinking, 'FocusCount', '+')


@receiver(post_delete, dispatch_uid=UserLink)
def userlink_delete_handler(sender, instance, **kwargs):
    if isinstance(instance, UserLink):
        mMs.CounterOperate(instance.UserBeLinked, 'FansCount', '-')
        mMs.CounterOperate(instance.UserLinking, 'FocusCount', '-')


@receiver(post_save, dispatch_uid=Attitude)
def Attitude_create_handler(sender, instance, created, **kwargs):
    if created and isinstance(instance, Attitude):
        mMs.CounterOperate(QRC((instance.Type if instance.Type not in 'SpecialTopic' else 'Topic') +
                               'Info.objects.get(ObjectID=%s)', 0, instance.ObjectID.replace('-', '')), 'Like' if int(instance.Point) == 1 else 'Dislike', '+')
    elif not created and isinstance(instance, Attitude):
        mMs.CounterOperate(QRC((instance.Type if instance.Type not in 'SpecialTopic' else 'Topic') +
                               'Info.objects.get(ObjectID=%s)', 0, instance.ObjectID.replace('-', '')), 'Like' if int(instance.Point) == 1 else 'Dislike', '+')
        mMs.CounterOperate(QRC((instance.Type if instance.Type not in 'SpecialTopic' else 'Topic') +
                               'Info.objects.get(ObjectID=%s)', 0, instance.ObjectID.replace('-', '')),
                           'Like' if abs(int(instance.Point) - 1) == 1 else 'Dislike', '-')


@receiver(pre_delete, dispatch_uid=Attitude)
def Attitude_delete_handler(sender, instance, **kwargs):
    if isinstance(instance, Attitude):
        mMs.CounterOperate(QRC((instance.Type if instance.Type not in 'SpecialTopic' else 'Topic') +
                               'Info.objects.get(ObjectID=%s)', 0, instance.ObjectID.replace('-', '')), 'Like' if int(instance.Point) == 1 else 'Dislike', '-')