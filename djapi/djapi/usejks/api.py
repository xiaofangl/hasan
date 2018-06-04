#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

from django.http import JsonResponse

from oper_jks import jenkins_tools
from log.logging_conf import *

loger = logging.getLogger(__file__)


def test(request):
    pass


def list_jobs(request):
    res = {}
    jks_tools = jenkins_tools('test')
    tmp = jks_tools._jobs_list()
    print 'tmp', type(tmp)
    res['data'] = tmp
    res['status'] = True
    return JsonResponse(res)