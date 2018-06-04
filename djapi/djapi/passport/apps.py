#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

import os
import sys
print os.getcwd()
reload(sys)
sys.setdefaultencoding('utf-8')

# os.environ.update({"DJANGO_SETTINGS_MODULE": "djapi.settings"})
# pro_dir = os.getcwd()  # 如果放在project目录，就不需要在配置绝对路径了
# sys.path.append('/Users/xiaofangl/Downloads/huasheng/hasan/djapi')
#
os.environ['DJANGO_SETTINGS_MODULE'] = 'djapi.settings.settings'  # 项目的settings

import django
django.setup()
print sys.path
sys.path.append(os.path.dirname(__file__))

import json
import uuid
import time
import datetime
from log.logging_conf import *
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from models import User2Group
from models import GroupExtend
from models import ModifyPermissionsLog
from passport.models import userInfo
from passport.models import operLog


from django.apps import AppConfig
from django.conf import settings
from tools.send_mail import Mail


class PassportConfig(AppConfig):
    name = 'passport'

"""
INSTALLED_APPS
给上面应用的每个应用创建四个组
admin, operate, guest, standby
"""
loger = logging.getLogger(__file__)


def login_required_hasan(func):
    def _wrapper(request, *args, **kwargs):
        # if login
        if request.META.get('HTTP_AUTHORIZATION', ''):
            return func(request, *args, **kwargs)
        # else:
        #     res = {'status': False, 'msg': '登录失败。。', 'user_id': '', 'userhashid': 'login_required_hasan', 'code': '2'}
        #     return res
    return _wrapper


def run_is_admin(username):
    username = '' if not username else username
    user_id = userInfo.objects.filter(hashKey=username).values('user_id')
    groups = User2Group.objects.filter(is_del=False, user_id=user_id).values('group__name')

    for item in groups:
        if 'admin' in item['group__name']:
            return True
        else:
            break
    return False


# 访问用户是否在这个组
def login_required_permission(group):
    def wrapped(func):
        def _wrapper(request, *args, **kwargs):
            username = request.META.get('HTTP_AUTHORIZATION', '')
            username = '' if not username else username
            user_id = userInfo.objects.filter(hashKey=username).values('user_id')
            user_group = get_user_group(user_id) #用户已有权限组
            _group = group.split('_')[:-1]
            _group = '_'.join(_group)
            # print '_group', _group, type(_group)
            _group = _group + '_admin'
            # print _group
            if user_group:
                for m in user_group['data']:
                    if group in m['group__name']:
                        return func(request, *args, **kwargs)

                    elif _group in m['group__name']:
                        return func(request, *args, **kwargs)
            print 'not permission..'
            res = {'status': False, 'msg': '权限不足，操作失败。请申请权限', 'user_id': username, 'code': '21', 'data': group}
            return HttpResponse(json.dumps(res))
        return _wrapper
    return wrapped


def get_user_group(user_id):
    try:
        groups = User2Group.objects.filter(is_del=False, user_id=user_id).values('group_id', 'group__name', 'group__groupextend__be_app')
        group_name = []
        for item in groups:
            group_name.append(item)
        res = {'status': True, 'msg': '获取权限组成功。。', 'user_id': user_id, 'code': '1', 'data': group_name}
    except User.groups:
        res = {'status': False, 'msg': '没有权限。。', 'user_id': user_id, 'code': '1', 'data': group_name}
    loger.warning(res)
    ModifyPermissionsLog.objects.create(user=user_id, type='5', status=res['status'], desc=res['msg'], code=res['data'])
    return res


def get_admin_group(request):
    username = request.META.get('HTTP_AUTHORIZATION', '')
    username = '' if not username else username
    user_id = userInfo.objects.filter(hashKey=username).values('user_id')
    user_group = get_user_group(user_id)  # 用户已有权限组
    # print 'user_group', user_group
    apps = []
    for m in user_group['data']:
        if 'admin' in m['group__name']:
            apps.append(m['group__groupextend__be_app'])
    app_list = set(apps)
    list_group = []
    print app_list
    for item in app_list:
        tmp = GroupExtend.objects.filter(is_del=False, be_app=item).values('group_id', 'group__name', 'be_app')
        for n in tmp:
            list_group.append(n)
    # print 'get_admin_group', list_group
    return list_group


#
@login_required_hasan
def add_group(request):
    username = request.META.get('HTTP_AUTHORIZATION', '')
    username = '' if not username else username
    print 'add_group_username', username
    # 第一次,
    apps = settings.__getattr__('INSTALLED_APPS')
    # 每创建一个APP
    # apps = settings.__getattr__('ADD_APP')
    # groups = settings.APP_DEFAULT_GROUP.get().keys()
    group_list = ['admin', 'operate', 'guest', 'standby']
    # print 'add_group', settings.APP_DEFAULT_GROUP.get('admin')
    app_list = []
    for item in apps:
        # print item
        if 'django' not in item:
            app_list.append(item)
        else:
            continue
    print 'applist', app_list, group_list
    all_data = []
    for app in app_list:
        name_row = []
        row_data = {'group_id': ''}
        for group in group_list:
            name_row.append(app + '_' + group)
        row_data['be_app'] = app
        row_data['created'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        row_data['name'] = name_row
        all_data.append(row_data)
    # print 'all_data', all_data
    for _n in all_data:
        for _name in _n['name']:
            try:
                group = Group.objects.get(name=_name)
                is_extend = GroupExtend.objects.filter(group_id=group.id)
                if not is_extend:
                    is_extend = GroupExtend.objects.create(be_app=_n['be_app'], group_id=group.id, created=_n['created'])
                res = {'status': False, 'msg': 'group 已经存在。。', 'user_id': username, 'code': '1', 'is_extend': is_extend}
            except Group.DoesNotExist:
                group = Group.objects.create(name=_name)
                is_extend = GroupExtend.objects.create(be_app=_n['be_app'], group_id=group.id, created=_n['created'])
                res = {'status': True, 'msg': 'group 创建成功。。', 'user_id': username, 'code': '0', 'is_extend': is_extend}
    operLog.objects.create(user=username, type='add_group', status=res['status'], desc=res['msg'], code=res['is_extend'])
    print 'add_group', res
    return HttpResponse(res)

"""
# group => PERMISSIONS(super)
# @get_group_user('passport_operate')
def group_add_permissions(request):
    username = request.META.get('HTTP_AUTHORIZATION', '')
    username = '' if not username else username


# (super)
# @get_group_user('passport_operate')
def group_del_permissions(request):
    username = request.META.get('HTTP_AUTHORIZATION', '')
    username = '' if not username else username
"""


# @login_required_hasan
def get_users(request, *args, **kwargs):
    username = request.META.get('HTTP_AUTHORIZATION', '')
    username = '' if not username else username
    try:
        data = []
        user = User.objects.filter(is_active=True).values('id', 'username', 'email')
        # print type(user)
        for item in user:
            data.append(item)

    except User.DoesNotExist:
        res = {'status': False, 'msg': 'get_groups failed..'}
        ModifyPermissionsLog.objects.create(user=username, type='get_users', status=res['status'], desc=res['msg'], code='')
    # print type(data)
    return data


def get_groups(request, *args, **kwargs):
    username = request.META.get('HTTP_AUTHORIZATION', '')
    username = '' if not username else username

    try:
        data = []
        group = Group.objects.filter(groupextend__is_del=False).values('id', 'groupextend__be_app', 'name')
        # print 'data', data
        for item in group:
            data.append(item)
    except Group.DoesNotExist:
        res = {'status': False, 'msg': 'get_groups failed..'}
        ModifyPermissionsLog.objects.create(user=username, type='get_groups', status=res['status'], desc=res['msg'], code='')
    print type(data)
    return data


# (admin)
# @get_group_user('admin')
def run_add_group(request, user_list, group):
    username = request.META.get('HTTP_AUTHORIZATION', '')
    username = '' if not username else username
    res = {'status': True, 'msg': '', 'data': ''}
    print 'receive', user_list, group
    for item in user_list:
        is_exist = User2Group.objects.filter(is_del=False, group_id=group, user_id=item)
        if not is_exist:
            try:
                obj = User2Group.objects.create(group_id=group, user_id=item)
                res = {'status': True, 'msg': 'user added group success..', 'data': obj.id}
            except User2Group.DoesNotExist as e:
                res = {'status': False, 'msg': 'user added group failed..', 'data': e}
            ModifyPermissionsLog.objects.create(user=username, type='run_add_group', status=res['status'], desc=res['msg'],
                                                code=res['data'])
        else:
            continue
    return res


# (admin)
# @get_group_user('admin')
def run_del_group(request, group_list, user):
    username = request.META.get('HTTP_AUTHORIZATION', '')
    username = '' if not username else username
    res = {'status': True, 'msg': '', 'data': ''}
    print 'receive', group_list, user
    for item in group_list:
        is_exist = User2Group.objects.filter(is_del=False, group_id=item, user_id=user)
        if is_exist:
            try:
                is_exist.update(is_del=True)
                res = {'status': True, 'msg': 'user deleted group success..', 'data': ''}
            except User2Group.DoesNotExist as e:
                res = {'status': False, 'msg': 'user deleted group failed..', 'data': e}
            ModifyPermissionsLog.objects.create(user=username, type='run_add_group', status=res['status'],
                                                desc=res['msg'],
                                                code=res['data'])
        else:
            continue
    return res


@csrf_exempt
def run_pwd_mail(title, sender, addressee, content, source_ip):
    print 'this run_send_mail'
    # 写一个urls 专用来 重置密码的
    title = 'Reset Password' if not title else title
    sender = 'Hasan(哈桑)' if not sender else sender
    # urls = "http://hasan.huashenghaoche.work"
    reset = "/reset_pwd"
    urls = "http://" + source_ip + reset
    # urls = "http://www.baidu.com"
    content = """
        <html> 
          <head>请重置密码</head> 
          <body> 
            <p>Hi! %s<br> 
               请点击链接重置密码.<br> 
               链接地址为 <a href=%s mce_href=%s>点我</a>  
            </p>
             <p>You Dear Shawna..</p>
          </body> 
        </html> 
        """ % (addressee, urls, urls)
    addressee = addressee + '@huashenghaoche.com'
    mail = Mail(title, sender, addressee, content)
    res = mail._send()
    return res


def run_apply_permission(apply_user, app, text, source_ip):
    # print type(apply_user), type(app), type(text)
    title = 'APPLY PERMISSION'
    # app_group_id = GroupExtend.objects.filter(is_del=False, be_app=app).values('group__name', 'group_id')
    # #print 'app_group_id', app_group_id
    # for item in app_group_id:
    #     if 'admin' in item['group__name']:
    #         admin_group = item['group_id']
    # print 'admin_group', admin_group
    # addressees = User2Group.objects.filter(is_del=False, group_id=admin_group).values('user__username')
    # print 'addressees', addressees
    # for c in addressees:
        # print type(c['user__username']), c['user__username']
    addressee = 'ops' + '@huashenghaoche.com'
    urls = "http://" + source_ip
    content = """
            <html> 
              <head>申请权限</head> 
              <body> 
                <p>Hi! %s<br> 
                   因访问%s:<br>
                   %s<br> 
                </p>
                <p>链接地址为 <a href=%s mce_href=%s>去往Hasan</a> </p>
                 <p>You Dear Shawna..</p>
              </body> 
            </html> 
        """ % (addressee, app, text, urls, urls)
    # print content
    mail = Mail(title, apply_user, addressee, content)
    res = mail._send()

    return res


def run_apply_dbmain(apply_user, text, source_ip):
    # print type(apply_user), type(app), type(text)
    title = 'APPLY DBMAIN'
    addressee = settings.DB_MAIN.get('addressee')
    addressee = 'ops@huashenghaoche.com' if not addressee else addressee
    source_ip = 'http://dbmain.huashenghaoche.work/accounts/login/?next=/' if not source_ip else source_ip
    urls = source_ip
    content = """
            <html> 
              <head>申请dbmain账号</head> 
              <body> 
                <p>Hi! %s<br> 
                   %s<br> 
                </p>
                <p><a href=%s mce_href=%s>去往dbmain</a> </p>
                 <p>You Dear Shawna..</p>
              </body> 
            </html> 
        """ % (addressee, text, urls, urls)
    # print content
    mail = Mail(title, apply_user, addressee, content)
    res = mail._send()

    return res

if __name__ == '__main__':
    get_groups('')