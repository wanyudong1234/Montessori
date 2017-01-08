# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-19 12:50
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('managesystem', '0002_auto_20161119_0253'),
    ]

    operations = [
        migrations.CreateModel(
            name='HoursDailyClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mons_hours', models.IntegerField(default=0)),
                ('music_hours', models.IntegerField(default=0)),
                ('art_hours', models.IntegerField(default=0)),
                ('english_hours', models.IntegerField(default=0)),
                ('consume_date', models.DateField(default=b'2016-11-11')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='managesystem.HoursStudent')),
            ],
        ),
    ]
