#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import os
import json
import sys

from oper import read_files, write_files, mod_files
from oper import query_list
from oper_dns import sync_file
from oper_dns import go_sync
from oper_dns import del_sync
from oper_dns import go_register
from oper_dns import go_del_register
from oper import create_files
from oper import delete_files
from oper import rsync_files
from oper import get_file_list
from oper import format_files

from passport.apps import login_required_permission
from passport.apps import login_required_hasan


def test(request):
    pass
"""
local_DNS_SERVER
name_list = ['172_huashenghaoche.com.zone', '192_huashenghaoche.com.zone', '192_huashenghaoche.net.zone', '192_huashenghaoche.work.zone']
test_list = [{'1': '01'}, {'2': '011'}]

"""


@login_required_hasan
# @login_required_permission('dns_api_operate')
def list(request):
    print request, request.META.get('HTTP_AUTHORIZATION', ''), type(request.method)
    res = get_file_list()
    file_name_list = res.get('data')
    print 'file_name_list', file_name_list
    print os.getcwd()

    result = {}
    for i in file_name_list:
        tmp = []
        tmp.append(i)
        tmp.append(read_files(i))
        result[i] = tmp
    #print result
    return JsonResponse(result)


@csrf_exempt
@login_required_permission('dns_api_operate')
def add_item(request):
    json_data = json.loads(request.body)
    file_name = json_data.get('file_name', '')
    host = json_data.get('host', '')
    type = json_data.get('type', '')
    value = json_data.get('value', '')
    res = write_files(file_name, host, type, value)
    # res['code'] = sync_file(file_name)
    if res['status']:
        recode = sync_file(file_name)
        res['code'] = recode
    # print 'get_data', res
    return JsonResponse(res)


@csrf_exempt
@login_required_permission('dns_api_operate')
def mod_item(request):
    json_data = json.loads(request.body)
    file_name = json_data.get('file_name', '')
    host = json_data.get('host', '')
    type = json_data.get('type', '')
    value = json_data.get('value', '')

    res = mod_files(file_name, host, type, value)
    if res['status']:
        recode = sync_file(file_name)
        res['code'] = recode
    return JsonResponse(res)


@login_required_hasan
# @login_required_permission('dns_api_operate')
def file_list(request):
    print request, request.META.get('HTTP_AUTHORIZATION', '')
    # html 当前文件
    # print sys.path
    results = query_list()
    return JsonResponse(results)


@csrf_exempt
@login_required_permission('dns_api_operate')
def add_file(request):
    print request
    json_data = json.loads(request.body)
    host_group = json_data.get('host', '')
    file_name = json_data.get('name', '')
    print 'data', json_data, host_group, file_name
    # res = go_register(host_group, file_name)
    res = create_files(host_group, file_name)
    if res['status']:
        res['code'] = go_register(host_group, file_name)
        recode = go_sync(host_group, file_name)
        res['recode'] = recode
    return JsonResponse(res)


@csrf_exempt
@login_required_permission('dns_api_operate')
def del_file(request):
    json_data = json.loads(request.body)
    host_group = json_data.get('host', '')
    file_name = json_data.get('name', '')
    file_id = json_data.get('id', '')
    print 'data', json_data, host_group, file_name, file_id
    res = delete_files(host_group, file_name, file_id)
    print res
    if res['status']:
        res['code'] = go_del_register(host_group, file_name)
        recode = del_sync(host_group, file_name)
    res['code'] = recode
    return JsonResponse(res)


@csrf_exempt
@login_required_permission('dns_api_operate')
def copy_file(request):
    json_data = json.loads(request.body)
    host_group = json_data.get('host', '')
    file_name = json_data.get('name', '')
    is_exist = json_data.get('isExist', '')
    print 'data', json_data, host_group, file_name, is_exist
    res = rsync_files(host_group, file_name, is_exist)
    if res['status']:
        recode = go_sync(host_group, file_name)
        res['code'] = recode
    return JsonResponse(res)


@csrf_exempt
@login_required_permission('dns_api_operate')
def upload_file(request):
    json_data = json.loads(request.body)
    host_group = json_data.get('host', '')
    file_name = json_data.get('name', '')
    res = format_files(host_group, file_name)
    if res['status']:
        res['code'] = go_register(host_group, file_name)
        recode = go_sync(host_group, file_name)
        res['recode'] = recode
    return JsonResponse(res)