#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

import json
from django.views.decorators.csrf import csrf_exempt


from django.http import JsonResponse
from django.http import HttpResponse

from apps import get_groups
from apps import get_users
from apps import login_required_hasan
from apps import get_user_group
from apps import get_admin_group
from apps import run_add_group
from apps import run_del_group
from apps import run_pwd_mail
from apps import run_apply_permission
from apps import run_apply_dbmain
from passport.models import userInfo
from django.conf import settings
from log.logging_conf import *

loger = logging.getLogger(__file__)


@login_required_hasan
def list(request):
    res = {
        'status': True,
        'message': ''
    }
    user_group = get_admin_group(request)
    all_group = get_groups(request)
    all_user = get_users(request)
    if all_user and all_group:
        res['permission_data'] = all_group
        res['all_user'] = all_user
        res['user_group'] = user_group
    else:
        res['status'] = False
        res['permission_data'] = ''
        res['all_user'] = ''
        res['user_group'] = ''
    # print 'allapi', res
    return JsonResponse(res)


@csrf_exempt
def is_group(request):
    # print 'is_group', request.GET.get('0', '')
    user_id = request.GET.get('0', '')
    res = get_user_group(user_id)
    # print 'is_group', res
    return JsonResponse(res)


@csrf_exempt
@login_required_hasan
def user_group(request):
    username = request.META.get('HTTP_AUTHORIZATION', '')
    username = '' if not username else username
    user_id = userInfo.objects.filter(hashKey=username).values('user_id')
    print 'user_id', user_id[0]['user_id']
    user = user_id[0]['user_id']
    loger.warning('user_group')
    loger.warning(user)
    user_id = user_id[0]['user_id']
    res = get_user_group(user_id)
    print 'is_group', res
    loger.warning(res)
    return JsonResponse(res)


@csrf_exempt
@login_required_hasan
def user_add_group(request):
    json_data = json.loads(request.body)
    group = json_data.get('permission_group', '')
    user_list = json_data.get('user', '')
    print 'jsondata', json_data, user_list, group
    user_list = set(user_list)
    res = run_add_group(request, user_list, group)
    return JsonResponse(res)


@csrf_exempt
@login_required_hasan
def user_del_group(request):
    json_data = json.loads(request.body)
    group_list = json_data.get('permission_group', '')
    user = json_data.get('user', '')
    print 'jsondata', json_data, group_list, user
    group_list = set(group_list)
    res = run_del_group(request, group_list, user)
    return JsonResponse(res)


@csrf_exempt
def reset_pawd_api(request):
    print 'this send_mail'
    # print request.body, type(request.body)
    """
    """

    json_data = json.loads(request.body)
    title = json_data.get('title', '')
    sender = json_data.get('username', '')
    addressee = json_data.get('mail', '')
    content = json_data.get('content', '')
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        source_ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        source_ip = request.META['REMOTE_ADDR']
    print source_ip
    # this test
    env = settings.ENV.get('env')
    if env == 'dev':
        source_ip = source_ip + ":8080"
    else:
        source_ip ="hasan.huashenghaoche.work"
    # sender = ''
    # all = request.body
    # all_list = all.split('&')
    # title = all_list[0].split('=')[1]
    # # sender = all_list[1].split('=')[1]
    # addressee = all_list[1].split('=')[1]
    # content = all_list[2].split('=')[1]
    # print title, sender, addressee, content
    res = {}
    recode = run_pwd_mail(title, sender, addressee, content, source_ip)
    if recode:
        pass
    else:
        res['status'] = False
        res['msg'] = 'send_mail failed..'
        print 'send_mail', res
    return JsonResponse(res)


@csrf_exempt
@login_required_hasan
def apply_permission(request):
    json_data = json.loads(request.body)
    apply_user = json_data.get('user', '')
    text = json_data.get('text', '')
    app = json_data.get('app', '')
    print apply_user, text, app
    if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        source_ip = request.META['HTTP_X_FORWARDED_FOR']
    else:
        source_ip = request.META['REMOTE_ADDR']
    print source_ip
    # this test
    env = settings.ENV.get('env')
    if env == 'dev':
        source_ip = source_ip + ":8080"
    else:
        source_ip = "hasan.huashenghaoche.work"
    res = run_apply_permission(apply_user, app, text, source_ip)
    return HttpResponse(res)


@csrf_exempt
@login_required_hasan
def apply_dbmain(request):
    json_data = json.loads(request.body)
    apply_user = json_data.get('user', '')
    text = json_data.get('text', '')

    source_ip = settings.DB_MAIN.get('dbmain')
    print apply_user, text, source_ip
    res = run_apply_dbmain(apply_user, text, source_ip)
    return HttpResponse(res)