#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

from datetime import datetime

import time
import sys
import os


# 登录用户和主机名：
os.environ['DJANGO_SETTINGS_MODULE'] = 'djapi.settings.settings'  # 项目的settings

import django
django.setup()
print sys.path
sys.path.append(os.path.dirname(__file__))
from fabric.api import *
from log.logging_conf import *
loger = logging.getLogger(__file__)
from django.conf import settings

# env.password = settings.DNS_SERVER.get('lan_dns').get('pawd')
env.roledefs = {
    'wan_dns': settings.DNS_SERVER.get('wan_dns').get('host'),
    'lan_dns': settings.DNS_SERVER.get('lan_dns').get('host')
}
print env.user, env.roledefs, env.password
# loger.info(env.user, env.roledefs, env.password)


@roles('lan_dns')
def register_lanzone(files):
    res = {}
    files = '\\\\"' + files + '\\\\"'
    # files = '\\' + '"' + files + '\\' + '"'
    one_line = settings.REGISTER_ZONE.get('file_content').get('1') % files + '\n'
    two_line = settings.REGISTER_ZONE.get('file_content').get('2') + '\n'
    three_line = settings.REGISTER_ZONE.get('file_content').get('3') % files + '\n'
    four_lien = settings.REGISTER_ZONE.get('file_content').get('4') + '\n'
    five_line = settings.REGISTER_ZONE.get('file_content').get('5') + '\n'
    file_path = settings.REGISTER_ZONE.get('file_path')
    # file_path = settings.REGISTER_ZONE.get('test_path')
    all_lines = one_line + two_line + three_line + four_lien + five_line
    commond = 'echo """%s""" >> %s' % (all_lines, file_path)
    status = 'service named status'
    recod = run(status)
    # print 'recod', recod
    loger.info(recod)
    # test_file = 'touch /tmp/rest.zone'
    # res['run'] = run(test_file)
    res['run'] = run(commond)
    print commond
    # res['run'] = local(commond)
    return res


@roles('wan_dns')
def register_wanzone(files):
    res = {}
    files = '\\\\"' + files + '\\\\"'
    local_files = '\\"' + files + '\\"'
    one_line = settings.REGISTER_ZONE.get('file_content').get('1') % files + '\n'
    two_line = settings.REGISTER_ZONE.get('file_content').get('2') + '\n'
    three_line = settings.REGISTER_ZONE.get('file_content').get('3') % files + '\n'
    four_lien = settings.REGISTER_ZONE.get('file_content').get('4') + '\n'
    five_line = settings.REGISTER_ZONE.get('file_content').get('5') + '\n'
    file_path = settings.REGISTER_ZONE.get('file_path')
    # file_path = settings.REGISTER_ZONE.get('test_path')
    all_lines = one_line + two_line + three_line + four_lien + five_line
    commond = 'echo """%s""" >> %s' % (all_lines, file_path)
    # test_file = 'touch /tmp/rest.zone'
    # res['run'] = run(test_file)
    status = 'service named status'
    recod = run(status)
    # print 'recod', recod
    loger.info(recod)
    res['run'] = run(commond)
    # print commond
    # res['run'] = local(commond)
    return res


@roles('lan_dns')
def del_register_lanzone(files):
    res = {}
    files = '\\\\"' + files + '\\\\"'
    local_files = '\\"' + files + '\\"'
    one_line = settings.REGISTER_ZONE.get('file_content').get('1') % files

    file_path = settings.REGISTER_ZONE.get('file_path')
    local_test = '\\/tmp\\/test.zones'
    # commond = 'sed -i "/%s/d" %s' % (all_lines, file_path)
    commond = 'sed -i "/%s/,+4d" %s' % (one_line, file_path)
    status = 'service named status'
    recod = run(status)
    print 'recod', recod
    loger.info(recod)
    res['run'] = run(commond)
    print commond
    # res['run'] = local(commond)
    return res


@roles('wan_dns')
def del_register_wanzone(files):
    res = {}
    files = '\\\\"' + files + '\\\\"'
    local_files = '\\"' + files + '\\"'
    one_line = settings.REGISTER_ZONE.get('file_content').get('1') % files + '\n'

    file_path = settings.REGISTER_ZONE.get('file_path')
    commond = 'sed -i "/%s/,+4d" %s' % (one_line, file_path)
    status = 'service named status'
    recod = run(status)
    # print 'recod', recod
    loger.info(recod)
    res['run'] = run(commond)
    # print commond
    # res['run'] = local(commond)
    return res


@roles('wan_dns')
def put_wandns(files, filename):
    res = {}
    loger.info(filename)
    local_file = filename
    dns_path = '/var/named/' + files
    loger.info(dns_path)
    # dns_path = '/tmp/' + files
    # backup = 'mv %s /backup/' % dns_path
    reload_dns = 'service named reload'
    lss = 'ls -l /tmp'
    status = 'ps -ef|grep named'
    loger.info('ready run')
    res['run'] = run(lss)
    loger.info('backup')
    #loger.info(res)
    res['put'] = put(local_file, dns_path)
    loger.info('put')
    loger.info(res)
    res['run'] = run(reload_dns)
    res['dns_status'] = run(status)
    return res


@roles('lan_dns')
def put_landns(files, filename):
    res = {}
    local_file = filename
    dns_path = '/var/named/' + files
    # backup = 'mv %s /backup/' % dns_path
    reload_dns = 'service named reload'
    status = 'ps -ef|grep named'
    # dns_path = '/tmp/' + files
    # reload_dns = 'ls -l /tmp'
    # tag = datetime.now().strftime('%y.%m.%d_%H.%M.%S')
    # res['run'] = run(backup)
    res['put'] = put(local_file, dns_path)
    res['run'] = run(reload_dns)
    res['dns_status'] = run(status)
    return res


@roles('lan_dns')
def del_lanfile(files):
    res = {}
    source_file = '/var/named/' + files
    # source_file = '/tmp/' + files
    del_comm = 'mv %s /tmp/' % source_file
    # del_comm = 'rm -fr %s' % source_file
    status = 'ps -ef|grep named'
    reload_dns = 'service named reload'
    res['run'] = run(del_comm)
    res['run'] = run(reload_dns)
    res['dns_status'] = run(status)
    return res


@roles('wan_dns')
def del_wanfile(files):
    res = {}
    source_file = '/var/named/' + files
    # source_file = '/tmp/' + files
    del_comm = 'mv %s /tmp/' % source_file
    # del_comm = 'rm -fr %s' % source_file
    status = 'ps -ef|grep named'
    reload_dns = 'service named reload'
    res['run'] = run(del_comm)
    res['run'] = run(reload_dns)
    res['dns_status'] = run(status)
    return res


def test(files, filename):
    local("pwd")
    local("uname")
    print files, filename


def go(host, files, filename):
    loger.info('sync dns zone file...')
    loger.info(filename)
    wan = settings.DNS_SERVER.get('wan_dns').get('ip')[0].split('.')[0]
    lan = settings.DNS_SERVER.get('lan_dns').get('ip')[0].split('.')[0]
    if host == wan:
        results = execute(put_wandns, files, filename)
    elif host == lan:
        results = execute(put_landns, files, filename)
    elif host == '199':
        results = execute(test, files, filename)
    time.sleep(1)
    print results
    loger.info(results)
    return results


def go_del(files, host_group):
    if host_group == 'wan_dns':
        results = execute(del_wanfile, files)
    elif host_group == 'lan_dns':
        results = execute(del_lanfile, files)
    loger.info(results)
    time.sleep(1)
    return results


def do_register(files, host_group):
    res = {}
    if host_group == 'wan_dns':
        res = execute(register_wanzone, files)
    elif host_group == 'lan_dns':
        res = execute(register_lanzone, files)
    loger.info(res)
    return res


def do_del_register(files, host_group):
    res = {}
    if host_group == 'wan_dns':
        res = execute(del_register_wanzone, files)
    elif host_group == 'lan_dns':
        res = execute(del_register_lanzone, files)
    loger.info(res)
    return res


if __name__ == '__main__':
    register_lanzone('huasheng.work.zone')