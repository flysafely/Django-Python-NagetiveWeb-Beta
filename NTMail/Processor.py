from NTWebsite.MainMethods import QueryRedisCache as QRC
from NTWebsite.MainMethods import RedisCacheOperation as RCO
from NTWebsite.MainMethods import CreateUUIDstr as CUD
from NTConfig import settings as ST
from django.http import HttpResponse
from django.core.mail import send_mail

def SendMail(scene, user):
    MB = QRC("MailBody.objects.get(Scene=%s)", None, scene)
    try:
        CodeNumber = CUD()
        send_mail(MB.Title, MB.Message, ST.EMAIL_FROM, [str(user.email), ], html_message=(
            MB.Html % ('127.0.0.1:8000' if ST.DEBUG else 'www.nagetive.com', user.username, CodeNumber)))
        RCO('set', TimeOut=60,
            key=(user.username + '&' + scene), value=CodeNumber)
    except Exception as e:
        print(e)
