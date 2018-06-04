#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

import os
from helper import add_host
from helper import del_host
from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from models import ProjectInfo
from models import ProjectLog
from models import DeployInfo
from models import HostWithProject


# Create your views here.


class Oper_ProjectInfo(object):
    def __init__(self):
        self.res = {
            'msg': '',
            'status': True
        }

    def _list_project(self, name):
        print 'data-class', name
        if name:
            data = ProjectInfo.objects.filter(is_del=False, name=name).values('id', 'name', 'type', 'server_port',
                                                                              'created', 'describe', 'download_path',
                                                                              'server_path')
            print 'data', data
            if len(data):
                tmp = []
                for item in data:
                    tmp.append(item)
                self.res['data'] = tmp
                self.res['status'] = False
                self.res['msg'] = 'This Project Name is Exist, Please Change Your Project Name...'
        else:
            tmp = []
            data = ProjectInfo.objects.filter(is_del=False).values('id', 'name', 'type', 'server_port', 'created',
                                                                   'describe')
            for item in data:
                tmp.append(item)
            self.res['data'] = tmp

        # print self.res
        ProjectLog.objects.create(project=name, code=data, oper_type='_list_project', oper_user='',
                                  status=self.res['status'])
        return self.res

    def _create_project(self, name, type, repository, server_port, server_path, download_path, host_list, describe):
        # print name, type, repository, server_port, project_admin, download_path, host_list, describe
        try:
            data = ProjectInfo.objects.create(name=name, type=type, repository=repository, server_port=server_port,
                                              server_path=server_path, \
                                              download_path=download_path, describe=describe)
            self.res['msg'] = 'create success...'
        except IOError as data:
            self.res['msg'] = data
            self.res['status'] = False
        ProjectLog.objects.create(project=name, code=data, oper_type='_create_project', oper_user='',
                                  status=self.res['status'])
        # print self.res

        return self.res

    def _modify_project_list(self, ids):
        print 'ids', ids
        data = ProjectInfo.objects.filter(is_del=False, id=ids).values('id', 'name', 'type', 'server_port', 'created',
                                                                       'describe', 'repository', 'download_path',
                                                                       'server_path')
        # print '_modify_project', data
        if len(data):
            tmp = []
            for item in data:
                tmp.append(item)
            self.res['data'] = tmp

        user_list = ProjectInfo.objects.filter(is_del=False, id=ids).values('user__username', 'user__email')
        if len(user_list):
            _tmp = []
            for _item in user_list:
                _item['title'] = 'Technology'
                _item['status'] = 'Active'
                _tmp.append(_item)
            self.res['users'] = _tmp

        host_list = HostWithProject.objects.filter(is_del=False, project=ids).values('hostname', 'created')
        if len(host_list):
            _tmps = []
            for _items in host_list:
                _tmps.append(_items)
            self.res['hosts'] = _tmps
        print 'res', self.res
        ProjectLog.objects.create(project=ids, code=data, oper_type='_modify_project_list', oper_user='', \
                                  status=self.res['status'])
        return self.res

    # 传ids 多对多插入,基础表中有数据的和基础表中无数据的
    def _modify_project_info(self, ids, user_id, host):
        print '+++++++++++++'
        print ids, user_id, host
        project_name = ProjectInfo.objects.filter(is_del=False, id=ids).values('name')
        print project_name[0]['name'], type(project_name[0]['name'])
        if user_id:
            try:
                data = ProjectInfo.objects.get(is_del=False, id=ids)
                data.user.add(user_id)
                self.res['msg'] = 'Add User Success...'
            except Exception as data:
                self.res['msg'] = data
                self.res['status'] = False
            ProjectLog.objects.create(project=ids, code=data, oper_type='_modify_project_info', oper_user='', \
                                      status=self.res['status'])
            return self.res
        elif host:
            self.res = add_host('', host, str(project_name[0]['name']))
            if self.res['status']:
                try:
                    is_exist = HostWithProject.objects.filter(is_del=False, hostname=host)
                    if is_exist:
                        data = HostWithProject.objects.get(is_del=False, hostname=host)
                        data.project.add(ids)
                    else:
                        hosts = HostWithProject()
                        hosts.hostname = host
                        hosts.save()
                        hosts.project.add(ids)
                    self.res['msg'] = 'Add Host Success...'
                except Exception as data:
                    self.res['msg'] = data
                    self.res['status'] = False
                ProjectLog.objects.create(project=ids, code='', oper_type='_modify_project_info', oper_user='', \
                                          status=self.res['status'])

            return self.res
            # else:
            #     return self.res

    def _modify_project_del(self, ids, user_id, hostname):
        print '------------'

        print ids, user_id, hostname
        project_name = ProjectInfo.objects.filter(is_del=False, id=ids).values('name')
        print project_name[0]['name'], type(project_name[0]['name'])

        # 正向del，反向用_set
        if user_id:
            # print 'del user', user_id
            try:
                data = ProjectInfo.objects.get(is_del=False, id=ids)
                data.user.remove(user_id)
            except Exception as data:
                self.res['msg'] = data
                self.res['status'] = False
            ProjectLog.objects.create(project=ids, code=data, oper_type='_modify_project_del', oper_user='', \
                                      status=self.res['status'])
            return self.res
        elif hostname:
            self.res = del_host('', hostname, str(project_name[0]['name']))
            if self.res['status']:
                print hostname
                # data = ProjectInfo.objects.get(is_del=False, id=ids)
                try:
                    data = HostWithProject.objects.get(is_del=False, hostname=hostname)
                    data.project.remove(ids)
                    HostWithProject.objects.filter(is_del=False, hostname=hostname).update(is_del=True)
                    self.res['msg'] = 'Del Host Success...'
                except Exception as data:
                    self.res['msg'] = data
                    self.res['status'] = False
                ProjectLog.objects.create(project=ids, code=data, oper_type='_modify_project_del', oper_user='', \
                                          status=self.res['status'])
            return self.res
            # else:
            #     return self.res

    def _delete_project(self, ids):
        try:
            data = ProjectInfo.objects.filter(is_del=False, id=ids).update(is_del=True)
            self.res['msg'] = 'Delete Project Success...'
        except Exception as data:
            self.res['msg'] = data
            self.res['status'] = False
        ProjectLog.objects.create(project=ids, code=data, oper_type='_delete_project', oper_user='', \
                                  status=self.res['status'])
        return self.res


def test(request):
    res = []
    tests = Oper_ProjectInfo('')
    res1 = tests._list_project()
    for i in res1:
        tmp = {}
        print 'res1', i.id, i.name, i.type, i.branches
        tmp['name'] = i.name
        tmp['type'] = i.type
        tmp['id'] = i.id
        tmp['branches'] = i.branches
        res.append(tmp)
    return HttpResponse(res)


if __name__ == '__main__':
    pass
    # test = Oper_ProjectInfo()
    # print '11'
    # print test._list_project()
