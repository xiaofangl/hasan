# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-03-05 07:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app01', '0003_auto_20180305_1444'),
    ]

    operations = [
        migrations.RenameField(
            model_name='dnsfiles',
            old_name='host',
            new_name='file_to_host',
        ),
    ]
