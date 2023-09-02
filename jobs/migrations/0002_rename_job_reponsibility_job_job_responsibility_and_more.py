# Generated by Django 4.2.2 on 2023-06-23 17:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobs', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='job',
            old_name='job_reponsibility',
            new_name='job_responsibility',
        ),
        migrations.AlterField(
            model_name='job',
            name='create_date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='创建日期'),
        ),
        migrations.AlterField(
            model_name='job',
            name='modified_date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='修改时间'),
        ),
    ]
