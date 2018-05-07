#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.


# 项目信息
class ProjectInfo(models.Model):
    PROJECT_TYPE_CHOICES = (
        ('0', u'java'),
        ('1', u'其他')
    )
    REPOSITORY_USER = (
        ('0', u'root')
    )
    PROJECT_ENV = (
        ('0', u'dev测试环境'),
        ('1', u'pre预上线环境'),
        ('2', u'pro线上环境')
    )
    user = models.ManyToManyField(User)
    name = models.CharField(u'项目名称', max_length=30, null=False)
    type = models.CharField(u'项目类型', max_length=30, choices=PROJECT_TYPE_CHOICES, default=0)

    repository = models.CharField(u'代码库地址', max_length=120, default='', null=True)
    server_port = models.CharField(u'服务端口', max_length=30, default=0, null=True)

    server_path = models.CharField(max_length=256, default='', null=True)
    download_path = models.CharField(u'下载路径', max_length=120, default=0)

    is_del = models.BooleanField(default=False)
    status = models.CharField(u'状态', max_length=30, default='', null=True)
    created = models.DateField(auto_now_add=True)
    describe = models.CharField(u'描述', max_length=120, default='', null=True)

    def format_date(self):
        pass

    class Meta:
        ordering = ['-pk']


class HostWithProject(models.Model):
    project = models.ManyToManyField(ProjectInfo)
    hostname = models.CharField(u'主机地址', max_length=120, default='', null=True)

    created = models.DateField(auto_now_add=True)
    is_del = models.BooleanField(default=False)


# 项目日志
class ProjectLog(models.Model):
    project = models.CharField(max_length=30, null=True)
    oper_type = models.CharField(max_length=30, null=True)
    oper_user = models.CharField(max_length=30, null=True)
    code = models.CharField(max_length=512, null=True)
    status = models.CharField(max_length=124, null=True)


# 发布信息
class DeployInfo(models.Model):
    packges = models.CharField(max_length=30, null=True)
    deploy_env = models.CharField(max_length=30, null=True)
    deploy_ip = models.CharField(max_length=30, null=True)


