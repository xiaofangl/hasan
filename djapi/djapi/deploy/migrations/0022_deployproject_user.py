# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2018-06-05 08:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('deploy', '0021_deployproject_package'),
    ]

    operations = [
        migrations.AddField(
            model_name='deployproject',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
