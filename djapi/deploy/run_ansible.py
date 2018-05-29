#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu
import redis
import Queue
from multiprocessing import Pool

from helper import _playbook
from tools.connt_db import OperationRedis
from models import ProjectInfo
from models import DeployProject
from passport.models import userInfo


def _start_multprocess(f):
    # q = Queue.Queue()
    pool = Pool(processes=4)
    rl = pool.map(f)
    pool.close()
    pool.join()
    print 'rl--', rl
    return rl


# host_list
def _start_deploy(json_data, play_file):
    client_path = json_data.get('client_path', '/tmp')
    hosts = json_data.get('project_name', 'test')
    # hosts = 'test'
    print hosts
    name = json_data.get('project_name', '')
    package_url = json_data.get('package_url', '')
    package_name = json_data.get('package_name', '')

    params = '{"host": "%s", "package_url": "%s", "client_path": "%s", "package_name": "%s"}' % (
        hosts, package_url, client_path, package_name)
    play_file = './deploy/playbook/playbook.yml' if not play_file else play_file
    _playbook(params, play_file)
    r = OperationRedis()
    res = r._get_data(str(name))

    for i in res['data']:
        if len(i) != 0:
            if i.split('::')[1]:
                _host = i.split('::')[0]
                _status = i.split('::')[1]
                DeployProject.objects.create(project=ProjectInfo.objects.get(is_del=False, name=name), host=_host, package=package_name,
                                             status=_status)
            else:
                hosts = []
                hosts.append(str(i.split('::')[0]))
                params = '{"host": "%s", "package_url": "%s", "client_path": "%s", "package_name": "%s"}' % (
                    hosts, package_url, client_path, package_name)
                _playbook(params, play_file)
                r = OperationRedis()
                res = r._get_data(str(name))
                for i in res['data']:
                    if len(i) != 0:
                        _host = i.split('::')[0]
                        _status = i.split('::')[1]
                        DeployProject.objects.create(project=ProjectInfo.objects.get(is_del=False, name=name),
                                                     host=_host, package=package_name,
                                                     status=_status)
    r._delete_data(str(name))
    print '___________________________'
    print 'redis::', res, type(res['data'])
    return res
