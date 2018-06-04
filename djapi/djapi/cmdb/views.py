#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

from models import Resource
from models import ResourceLog


class OperateResource(object):
    def __init__(self, user, res, *wargs, **kwargs):
        self.user = user
        self.res = res

    def _list(self):
        _total_data = Resource.objects.filter(is_del=False).values('id', 'address', 'owner', 'be_app', 'os', 'hostname',
                                                                   'host_type', \
                                                                   'pyh_host', 'host_env', 'status', 'created')
        print '_total_data+++++++', _total_data
        _total_list = []
        for item in _total_data:
            _total_list.append(item)
        self.res['data'] = _total_list
        return self.res

    def _add(self, ip_address, admin, apps, os, hostname, run_env, host_type, pyh_machine, is_del, status):
        print '_add', self.user
        self.user = '' if not self.user else self.user
        try:
            Resource.objects.create(address=ip_address, owner=admin, be_app=apps, os=os, hostname=hostname, \
                                    host_type=host_type, pyh_host=pyh_machine, host_env=run_env, status=status)
            self.res = {'status': True, 'user': self.user, 'desc': 'add resource success..'}
        except IOError, e:
            self.res = {'status': False, 'user': self.user, 'desc': e}
        ResourceLog.objects.create(user=self.user, type='', status=self.res['status'], desc=self.res['desc'])
        return self.res

    def _del(self, id):
        try:
            data = Resource.objects.filter(id=id).update(is_del=True)
            # print '_del', data
            # data.is_del.add(True)
            self.res = {'status': True, 'user': self.user, 'desc': data}
        except IOError, e:
            self.res = {'status': False, 'user': self.user, 'desc': e}
        ResourceLog.objects.create(user=self.user, type='', status=self.res['status'], desc=self.res['desc'])
        return self.res

    def _mod(self, id, ip_address, admin, apps, os, hostname, run_env, host_type, pyh_machine):
        try:
            print id, ip_address
            data = Resource.objects.filter(id=id).update(address=ip_address, owner=admin, be_app=apps, os=os,
                                                         hostname=hostname, \
                                                         host_type=host_type, pyh_host=pyh_machine, host_env=run_env)
            # data['adress'] = ip_address
            # data['owner'] = admin
            # data['be_app'] = apps
            # data['os'] = os
            # data['hostname'] = hostname
            # data['host_type'] = host_type
            # data['pyh_host'] = pyh_machine
            # data['host_env'] = run_env
            self.res = {'status': True, 'user': self.user, 'desc': data}
        except IOError, e:
            self.res = {'status': False, 'user': self.user, 'desc': e}
        ResourceLog.objects.create(user=self.user, type='', status=self.res['status'], desc=self.res['desc'])
        return self.res

    def _search(self, admin, apps, run_env):
        self.res['status'] = True
        _total_list = []
        if len(admin) != 0:
            try:
                _total_data = Resource.objects.filter(is_del=False, owner=admin).values('id', 'address', 'owner',
                                                                                        'be_app', 'os', 'hostname',
                                                                                        'host_type', \
                                                                                        'pyh_host', 'host_env',
                                                                                        'status', 'created')

                for item in _total_data:
                    _total_list.append(item)
                self.res['data'] = _total_list
            except IOError, e:
                self.res['data'] = e
                self.res['status'] = False
            return self.res
        elif len(apps) != 0:
            try:
                _total_data = Resource.objects.filter(is_del=False, be_app=apps).values('id', 'address', 'owner',
                                                                                        'be_app', 'os', 'hostname',
                                                                                        'host_type', \
                                                                                        'pyh_host', 'host_env',
                                                                                        'status', 'created')

                for item in _total_data:
                    _total_list.append(item)
                self.res['data'] = _total_list
            except IOError, e:
                self.res['data'] = e
                self.res['status'] = False
            return self.res
        elif len(run_env) != 0:

            try:
                _total_data = Resource.objects.filter(is_del=False, host_env=run_env).values('id', 'address', 'owner',
                                                                                             'be_app', 'os', 'hostname',
                                                                                             'host_type', \
                                                                                             'pyh_host', 'host_env',
                                                                                             'status', 'created')

                for item in _total_data:
                    _total_list.append(item)
                self.res['data'] = _total_list
            except IOError, e:
                self.res['data'] = e
                self.res['status'] = False
            return self.res
