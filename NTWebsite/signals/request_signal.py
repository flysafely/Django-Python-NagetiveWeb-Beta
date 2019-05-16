from django.db.models.signals import post_save
#from django.dispatch import receiver
from NTWebsite.improtFiles.models_import_head import *
#from django.db.models import F

from django.dispatch import receiver
from django.core.signals import request_finished


@receiver(request_finished, dispatch_uid="request_finished")
def request_finished_handler(sender, **kwargs):
    print("Request finished!================================")

