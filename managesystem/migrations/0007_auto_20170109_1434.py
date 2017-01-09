# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-09 14:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managesystem', '0006_coursedailyclass'),
    ]

    operations = [
        migrations.AddField(
            model_name='trystudent',
            name='accompany_username',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AddField(
            model_name='trystudent',
            name='register_date',
            field=models.DateField(default=b'2016-11-11'),
        ),
        migrations.AddField(
            model_name='trystudent',
            name='source',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AddField(
            model_name='trystudent',
            name='try_class_one_time',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AddField(
            model_name='trystudent',
            name='try_class_two_time',
            field=models.CharField(default=b'', max_length=200),
        ),
        migrations.AddField(
            model_name='trystudent',
            name='unRegister_reason',
            field=models.CharField(default=b'', max_length=200),
        ),
    ]
