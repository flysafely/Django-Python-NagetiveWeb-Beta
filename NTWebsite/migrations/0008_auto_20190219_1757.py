# Generated by Django 2.0.6 on 2019-02-19 09:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('NTWebsite', '0007_auto_20190219_1750'),
    ]

    operations = [
        migrations.RenameField(
            model_name='rollcalldialogue',
            old_name='ObjectIDID',
            new_name='ObjectID',
        ),
    ]