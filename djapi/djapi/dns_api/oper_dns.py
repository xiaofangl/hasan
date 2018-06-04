#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

from log.logging_conf import *
from fabfile import go
from fabfile import go_del
from fabfile import do_register
from fabfile import do_del_register
from django.conf import settings

loger = logging.getLogger(__file__)


def sync_file(filename, *args, **kwargs):
    host = filename.split("_")[0]
    files = filename.split('_')[1]
    print 'this sync test run fab', host, type(host), files
    result = go(host, files, filename)
    loger.warning(result)
    return result


def go_sync(host, files, *args, **kwargs):
    res = {
        'status': True,
        'message': 'go_syncing..'
    }
    print 'go_sync', host, files
    for item in host:
        if 'lan_dns' in item:
            host0 = settings.DNS_SERVER.get('lan_dns').get('ip')[0].split('.')[0]
            filename = host0 + '_' + files
            res['register'] = do_register(files, 'lan_dns')
            res = go(host0, files, filename)

        elif 'wan_dns' in item:
            host1 = settings.DNS_SERVER.get('wan_dns').get('ip')[0].split('.')[0]
            filename = host1 + '_' + files
            res['register'] = do_register(files, 'wan_dns')
            res = go(host1, files, filename)
    loger.info(res)
    return res


def del_sync(host, files, *args, **kwargs):
    res = {
        'status': True,
        'message': 'del_syncing..'
    }
    print 'go_sync', host, files
    for item in host:
        if 'lan_dns' in item:
            res = go_del(files, 'lan_dns')
        elif 'wan_dns' in item:
            res = go_del(files, 'wan_dns')
    loger.info(res)
    return res


def go_register(host, files, *args, **kwargs):
    res = {
        'status': True,
        'message': 'go_register..'
    }
    print 'go_register', host, files
    for item in host:
        if 'lan_dns' in item:
            res = do_register(files, 'lan_dns')
        elif 'wan_dns' in item:
            res = do_register(files, 'wan_dns')
    loger.info(res)
    return res


def go_del_register(host, files, *args, **kwargs):
    res = {
        'status': True,
        'message': 'go_del_register..'
    }
    print 'go_del_register', host, files
    for item in host:
        if 'lan_dns' in item:
            res = do_del_register(files, 'lan_dns')
        elif 'wan_dns' in item:
            res = do_del_register(files, 'wan_dns')
    loger.info(res)
    return res

if __name__ == '__main__':
    sync_file('192_test.com.zone')
    # go_sync([''])