# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-19 02:53
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managesystem', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hoursstudent',
            name='register_date',
            field=models.DateField(default=b'2016-11-11'),
        ),
        migrations.AlterField(
            model_name='hoursstudent',
            name='phone_num',
            field=models.CharField(max_length=200),
        ),
    ]
