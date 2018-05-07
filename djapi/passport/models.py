#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu
from __future__ import unicode_literals

import uuid
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

# Create your models here.


class userInfo(models.Model):
    user = models.ForeignKey(User)
    hashKey = models.UUIDField(u"", default=uuid.uuid1)
    created = models.DateTimeField(auto_now_add=True)


class operLog(models.Model):
    user = models.CharField(max_length=30, null=True, default='')
    type = models.CharField(max_length=30, null=True, default='')
    status = models.CharField(max_length=30, null=True, default='')
    desc = models.CharField(max_length=125, null=True, default='')
    code = models.CharField(max_length=30, null=True, default='')
    created = models.DateTimeField(auto_now_add=True)


# 默认创建 与group
class GroupExtend(models.Model):
    group = models.OneToOneField(Group)
    be_app = models.CharField(max_length=125, null=True, default='')
    desc = models.CharField(max_length=125, null=True, default='')
    is_del = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)


class AccessControl(models.Model):
    """
    自定义权限
    """
    PERMISSIONS = (
        ('access_dashboard', u'控制面板'),
        ('access_log', u'日志管理'),

        ('access_super_manage', u'超级用户'),
        ('access_user_manage', u'用户管理'),
        ('access_role_manage', u'角色管理'),

        ('access_operate_role', u'操作角色'),
    )

    group = models.ManyToManyField(Group)
    codename = models.CharField(max_length=125, default='')
    name = models.CharField(max_length=125, default='')
    created = models.DateTimeField(auto_now_add=True, null=True)
    desc = models.CharField(max_length=125, default='', null=True)


class ModifyPermissionsLog(models.Model):
    user = models.CharField(max_length=30, null=True, default='')
    type = models.CharField(max_length=256, null=True, default='')
    status = models.CharField(max_length=256, null=True, default='')
    desc = models.CharField(max_length=256, null=True, default='')
    code = models.CharField(max_length=2048, null=True, default='')
    created = models.DateTimeField(auto_now_add=True)


class User2Group(models.Model):
    user = models.ForeignKey(User)
    group = models.ForeignKey(Group)
    is_del = models.BooleanField(default=False)