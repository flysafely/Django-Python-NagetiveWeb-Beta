# Generated by Django 2.0.6 on 2019-05-16 10:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NTWebsite', '0029_auto_20190516_1602'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentattitude',
            name='Point',
            field=models.IntegerField(null=True, verbose_name='立场代码'),
        ),
        migrations.AlterField(
            model_name='topicattitude',
            name='Point',
            field=models.IntegerField(null=True, verbose_name='立场代码'),
        ),
    ]
