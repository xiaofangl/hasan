#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu


import json
import uuid

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from passport.models import userInfo
from passport.models import operLog
from apps import run_is_admin

# Create your views here.


@csrf_exempt
def login(request):
    json_data = json.loads(request.body)
    username = json_data.get('username', '')
    password = json_data.get('password', '')
    users = User.objects.filter(username=username)
    if users:
        user = authenticate(username=username, password=password)
        if user:
            print 'user2', user
            if user.is_active:
                # login(request, user)
                hash_key = uuid.uuid1()
                user_id = User.objects.filter(username=user).values('id')
                # #print 'user_id', user_id, user_id[0].get('id')
                obj = userInfo.objects.create(user_id=user_id[0].get('id'), hashKey=hash_key)
                is_admin = run_is_admin(obj.hashKey)
                res = {'status': True, 'msg': '登录成功。。', 'user_id': user.pk, 'userhashid': obj.hashKey, 'code': '0', 'username': username, 'is_admin': is_admin}
            else:
                res = {'status': False, 'msg': '登录失败。。', 'user_id': '', 'userhashid': '', 'code': '2'}
        else:
            res = {'status': False, 'msg': '登录失败。。', 'user_id': '', 'userhashid': '', 'code': '1'}
    else:
        res = {'status': False, 'msg': '用户不存在，请注册。。', 'user_id': '', 'userhashid': '', 'code': '1'}
    #print 'login', res
    operLog.objects.create(user=username, type='login', status=res['status'], desc=res['msg'], code=res['code'])
    return JsonResponse(res)


@csrf_exempt
def signup(request):
    json_data = json.loads(request.body)
    username = json_data.get('username', '')
    password = json_data.get('password', '')
    email = json_data.get('email', '')
    res = {
        'status': True,
        'msg': ''
    }
    # print 'json_data', json_data
    try:
        user = User.objects.get(username=username)
        res['code'] = '1'
        res['user_id'] = user.id
        res['userhashid'] = ''
        res['msg'] = '用户已经存在，请直接登入..'
        #print 'user1', user
    except User.DoesNotExist:
        user = User.objects.create_user(username, email, password)
        # print 'user2', user
        if user is not None:
            user.is_active = True
            user.save()
            # todo 新用户，并绑定
            hash_key = uuid.uuid1()
            user_id = User.objects.filter(username=user).values('id')
            #print 'user_id', user_id, user_id[0].get('id')
            obj = userInfo.objects.create(user_id=user_id[0].get('id'), hashKey=hash_key)
            is_admin = run_is_admin(obj.hashKey)
            # print 'obj', obj.hashKey
            res['username'] = username
            res['is_admin'] = is_admin
            res['code'] = '0'
            res['userhashid'] = obj.hashKey
            res['user_id'] = obj.user_id
            res['msg'] = '用户创建成功..'
        else:
            res['status'] = False
            res['code'] = '2'
            res['userhashid'] = ''
            res['msg'] = '用户创建失败..'
    print 'res1', res
    operLog.objects.create(user=username, type='signup', status=res['status'], desc=res['msg'], code=res['code'])
    return JsonResponse(res)


@csrf_exempt
def reset_password(request):
    json_data = json.loads(request.body)
    username = json_data.get('username', '')
    first_pwd = json_data.get('firstPwd', '')
    second_pwd = json_data.get('secondPwd', '')
    print 'json_data', json_data

    if first_pwd == second_pwd:
        print 'password'
        user = User.objects.filter(username=username)
        if user:
            user = User.objects.get(username=username)
            user.set_password(second_pwd)
            user.save()
            print 'user3', user
            hash_key = uuid.uuid1()
            user_id = User.objects.filter(username=username).values('id')
            # print 'user_id', user_id, user_id[0].get('id')
            obj = userInfo.objects.create(user_id=user_id[0].get('id'), hashKey=hash_key)
            is_admin = run_is_admin(obj.hashKey)
            res = {'status': True, 'msg': '修改成功。。', 'user_id': obj.user_id, 'userhashid': obj.hashKey, 'code': '0', 'username': username, 'is_admin': is_admin}
        else:
            res = {'status': False, 'msg': '用户不存在。。', 'user_id': '', 'userhashid': '', 'code': '1'}
    else:
        res = {'status': False, 'msg': '修改失败。。', 'user_id': '', 'userhashid': '', 'code': '2'}

    operLog.objects.create(user=username, type='reset_password', status=res['status'], desc=res['msg'], code=res['code'])
    return JsonResponse(res)