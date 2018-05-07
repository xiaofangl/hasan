#!/usr/bin/env python
# coding=utf-8

from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Resource(models.Model):
    PROJECT_TYPE_CHOICES = (
        ('0', u'active'),
        ('1', u'')
    )
    REPOSITORY_USER = (
        ('0', u'root')
    )
    PROJECT_ENV = (
        ('0', u'dev测试环境'),
        ('1', u'pre预上线环境'),
        ('2', u'pro线上环境')
    )

    address = models.CharField(u'IP地址', max_length=30, null=True)

    owner = models.CharField(u'管理员', max_length=120, default='', null=True)
    be_app = models.CharField(u'业务线', max_length=30, default=0, null=True)
    os = models.CharField(u'系统版本', max_length=30, default='',null=True)
    hostname = models.CharField(u'主机域名', max_length=120, null=True)
    host_type = models.CharField(u'主机类型', max_length=30, null=True)
    pyh_host = models.CharField(u'宿主机', max_length=120, null=True)

    host_env = models.CharField(u'运行环境', max_length=30, null=True)
    is_del = models.BooleanField(default=False)
    status = models.CharField(u'状态', max_length=30, choices=PROJECT_TYPE_CHOICES, null=0)
    created = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-pk']


class ResourceLog(models.Model):
    user = models.CharField(max_length=30, null=True)
    type = models.CharField(max_length=30, null=True)
    status = models.BooleanField(default=True)
    desc = models.CharField(max_length=256, null=True)