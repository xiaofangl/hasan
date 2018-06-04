#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from passport.apps import login_required_permission
from passport.apps import login_required_hasan
from views import OperateResource


# @login_required_hasan
def list(request):
    print 'list', list
    res = {}
    user = request.META.get('HTTP_AUTHORIZATION', '')
    _oper_resource = OperateResource(user, res)
    res = _oper_resource._list()
    return JsonResponse(res)


@csrf_exempt
@login_required_hasan
def add_item(request):
    res = {}
    json_data = json.loads(request.body)
    ip_address = json_data.get('address', '')
    admin = json_data.get('owner', '')
    apps = json_data.get('be_app', '')
    os = json_data.get('os', '')
    hostname = json_data.get('hostname', '')
    run_env = json_data.get('host_env', '')
    host_type = json_data.get('host_type', '')
    pyh_machine = json_data.get('pyh_host', '')
    is_del = json_data.get('is_del', '')
    status = json_data.get('status', '')
    user = request.META.get('HTTP_AUTHORIZATION', '')
    print 'add_item', ip_address, admin, apps, os, hostname, run_env, host_type, pyh_machine, is_del, status, user, res
    _oper_resource = OperateResource(user, res)
    res = _oper_resource._add(ip_address, admin, apps, os, hostname, run_env, host_type, pyh_machine, is_del, status)
    return JsonResponse(res)


@csrf_exempt
@login_required_hasan
def del_item(request):
    res = {}
    json_data = json.loads(request.body)
    id = json_data.get('id', '')
    user = request.META.get('HTTP_AUTHORIZATION', '')
    # print 'add_item', ip_address, admin, apps, os, hostname, run_env, host_type, pyh_machine, is_del, status, user, res
    print 'del_item', id
    _oper_resource = OperateResource(user, res)
    res = _oper_resource._del(id)
    return JsonResponse(res)


@csrf_exempt
@login_required_hasan
def mod_item(request):
    res = {}
    json_data = json.loads(request.body)
    id = json_data.get('id', '')
    ip_address = json_data.get('address', '')
    admin = json_data.get('owner', '')
    apps = json_data.get('be_app', '')
    os = json_data.get('os', '')
    hostname = json_data.get('hostname', '')
    run_env = json_data.get('host_env', '')
    host_type = json_data.get('host_type', '')
    pyh_machine = json_data.get('pyh_host', '')
    is_del = json_data.get('is_del', '')
    status = json_data.get('status', '')
    user = request.META.get('HTTP_AUTHORIZATION', '')
    print 'mod_item', id, ip_address, admin, apps, os, hostname, run_env, host_type, pyh_machine, is_del, status, user, res
    _oper_resource = OperateResource(user, res)
    res = _oper_resource._mod(id, ip_address, admin, apps, os, hostname, run_env, host_type, pyh_machine)
    return JsonResponse(res)


@csrf_exempt
@login_required_hasan
def search_one(request):
    res = {}
    json_data = json.loads(request.body)
    apps = json_data.get('be_app', '')
    run_env = json_data.get('host_env', '')
    admin = json_data.get('owner', '')
    user = request.META.get('HTTP_AUTHORIZATION', '')
    _oper_resource = OperateResource(user, res)
    res = _oper_resource._search(admin, apps, run_env)
    return JsonResponse(res)