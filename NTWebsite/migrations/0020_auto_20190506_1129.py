# Generated by Django 2.0.6 on 2019-05-06 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NTWebsite', '0019_topicinfo_createtime'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topicinfo',
            name='EditDate',
            field=models.DateTimeField(auto_now=True, verbose_name='编辑时间'),
        ),
    ]