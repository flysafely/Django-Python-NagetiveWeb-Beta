# Generated by Django 2.0.6 on 2019-05-22 09:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('NTWebsite', '0035_auto_20190520_1758'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentinfo',
            name='Parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='NTWebsite.CommentInfo', verbose_name='父评论'),
        ),
    ]