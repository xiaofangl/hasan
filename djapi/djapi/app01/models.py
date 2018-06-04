#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

from django.db import models
"""
    dns_api models ..
"""


class DnsHost(models.Model):
    host = models.CharField(max_length=60, default='', null=True)
    desc = models.CharField(max_length=60, default='', null=True)


class DnsFiles(models.Model):
    file_to_host = models.ManyToManyField(DnsHost)
    filename = models.CharField(max_length=120, default='', null=True)
    desc = models.CharField(max_length=30, default='', null=True)
    # created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=120, null=True, default='')


class UpdateFiles(models.Model):
    dnsfiles = models.OneToOneField(DnsFiles)
    path = models.CharField(max_length=120, default='', null=True)
    filename = models.CharField(max_length=120, default='', null=True)
    img = models.ImageField(max_length=256, default='', null=True)
    created = models.DateField(null=True, auto_now_add=True)
    status = models.CharField(max_length=120, null=True, default='')