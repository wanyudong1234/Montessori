# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-09 15:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managesystem', '0007_auto_20170109_1434'),
    ]

    operations = [
        migrations.AddField(
            model_name='trystudent',
            name='birth_date',
            field=models.CharField(default=b'0\xe4\xb8\xaa\xe6\x9c\x88', max_length=200),
        ),
    ]
