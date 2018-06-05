#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

import json
from models import ProjectInfo
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from views import Oper_ProjectInfo
from admin import get_package_list
from admin import format_url
from run_ansible import _start_deploy

from passport.apps import login_required_hasan
from passport.models import userInfo


@login_required_hasan
def list(request):
    # print request.GET.get('0', '')

    name = request.GET.get('0', '')
    name = '' if not name else name
    projecttalbe = Oper_ProjectInfo()
    results = projecttalbe._list_project(name)
    return JsonResponse(results)


@csrf_exempt
@login_required_hasan
def add_item(request):
    json_data = json.loads(request.body)
    name = json_data.get('name', '')
    type = json_data.get('type', '')
    repository = json_data.get('repository', '')
    server_port = json_data.get('server_port', '')
    server_path = json_data.get('server_path', '')
    download_path = json_data.get('download_path', '')
    host_list = json_data.get('host_list', '')
    describe = json_data.get('describe', '')

    operation = Oper_ProjectInfo()
    res = operation._create_project(name, type, repository, server_port, server_path, download_path, host_list,
                                    describe)

    return JsonResponse(res)


@csrf_exempt
@login_required_hasan
def mod_item(request):
    # print request

    if request.method == 'GET':
        ids = request.GET.get('0', '')
        ids = '' if not ids else ids
        operation = Oper_ProjectInfo()
        res = operation._modify_project_list(ids)
    elif request.method == 'POST':
        json_data = json.loads(request.body)
        print 'mod_item', json_data
        user_id = json_data.get('user_id', '')
        host = json_data.get('host', '')
        ids = json_data.get('id', '')
        operation = Oper_ProjectInfo()
        res = operation._modify_project_info(ids, user_id, host)
    elif request.method == 'PUT':
        # print request.body
        json_data = json.loads(request.body)
        # print 'mod_item', json_data
        user_id = json_data.get('user_id', '')
        hostname = json_data.get('hostname', '')
        ids = json_data.get('id', '')
        operation = Oper_ProjectInfo()
        res = operation._modify_project_del(ids, user_id, hostname)
    return JsonResponse(res)


@csrf_exempt
@login_required_hasan
def del_item(request):
    print 'del_item'
    print request.GET.get('0', '')
    ids = request.GET.get('0', '')
    operation = Oper_ProjectInfo()
    res = operation._delete_project(ids)
    return JsonResponse(res)


@csrf_exempt
@login_required_hasan
def package_list(request):
    json_data = json.loads(request.body)
    print 'json_data', json_data
    download_path = json_data.get('download_path', '')
    ids = json_data.get('id', '')
    name = json_data.get('name', '')
    server_path = json_data.get('server_path', '')
    server_port = json_data.get('server_port', '')

    urls = format_url('http://', download_path, '/') + format_url('', name, '/')
    # print 'urls', urls
    res = get_package_list(urls)
    # print '--------', res
    return JsonResponse(res)


@csrf_exempt
@login_required_hasan
def run_deploy(request):
    username = request.META.get('HTTP_AUTHORIZATION', '')
    username = '' if not username else username
    user_id = userInfo.objects.filter(hashKey=username).values('user_id', 'user__username')
    print 'user_id', user_id, type(user_id[0]['user_id'])
    json_data = json.loads(request.body)
    # print 'run_deploy', json_data
    id = json_data.get('id', '')
    project = ProjectInfo.objects.get(is_del=False, id=id)
    project.user.all()
    _res = project.user.filter(id=user_id[0]['user_id'])
    print 'project', _res
    if _res:
        json_data['user_id'] = user_id[0]['user_id']
        res = _start_deploy(json_data, '')
    else:
        res = {
            'status': False,
            'msg': '%s 用户没有发布权限，请联系本项目的业务运维管理员 添加本业务的发布权限。。。' % user_id[0]['user__username']
        }
    # print res
    return JsonResponse(res)


if __name__ == '__main__':
    pass
