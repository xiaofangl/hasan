# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-05-28 03:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('deploy', '0012_auto_20180528_1124'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='deployinfo',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='deployinfo',
            name='packges',
        ),
        migrations.RemoveField(
            model_name='deployinfo',
            name='star_time',
        ),
        migrations.AddField(
            model_name='deployinfo',
            name='created',
            field=models.DateField(auto_now_add=True),
            preserve_default=False,
        ),
    ]
