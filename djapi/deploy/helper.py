#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

import os
import redis
import ansible.runner
import Queue
from ansible.playbook import PlayBook
from ansible import callbacks
from ansible import utils

from models import DeployInfo
from tools.connt_db import OperationRedis

"""
    this file provides python-ansible API support;
    provides ansible-runner API;
    provides ansible-playbook API;
    the ansible version 1.9;
    python version 2.7;
    
"""


def _ansible_shells(host, mod_type, mod):
    runner = ansible.runner.Runner(
        host_list=host,
        module_name=mod_type,
        module_args=mod,
        remote_user="root",
        forks=10
    )
    return runner.run()


def ansible_copy(host_list, mod='copy', param=''):
    res = {
        'status': True,
        'message': ''
    }

    if param:
        results = _ansible_shells(host_list, mod, param)
        for (hostname, result) in results['contacted'].items():
            if not 'failed' in result:
                print "%s >>> %s" % (hostname, result['checksum'])
            else:
                print "%s >>> %s" % (hostname, result['msg'])
                res['status'] = False
                res[hostname] = result['msg']
        for (hostname, result) in results['dark'].items():
            print "%s >>> %s" % (hostname, result['msg'])
            res[hostname] = result['msg']

    else:
        res['status'] = False
        res['message'] = 'param not definition..'

    return res


def ansible_shell(host_list, mod='shell', param=''):
    res = {
        'status': True,
        'message': ''
    }

    if param:
        results = _ansible_shells(host_list, mod, param)
        for (hostname, result) in results['contacted'].items():
            an_rc = result["rc"]
            if an_rc == 0:
                print "%s >>> %s" % (hostname, result['stdout'])
            else:
                print "%s >>> %s" % (hostname, result['stderr'])
                res[hostname] = result['stderr']

        for (hostname, result) in results['dark'].items():
            print "%s >>> %s" % (hostname, result['msg'])
            res[hostname] = result['msg']
    else:
        res['status'] = False
        res['message'] = 'param not definition..'
    return res


def ansible_command(host_list, mod='script', param=''):
    res = {
        'status': True,
        'message': ''
    }

    if param:
        results = _ansible_shells(host_list, mod, param)
        for (hostname, result) in results['contacted'].items():
            an_rc = result["rc"]
            if an_rc == 0:
                print "%s >>> %s" % (hostname, result['stdout'])
            else:
                print "%s >>> %s" % (hostname, result['stderr'])
                res[hostname] = result['stderr']

        for (hostname, result) in results['dark'].items():
            print "%s >>> %s" % (hostname, result['msg'])
            res[hostname] = result['msg']
    else:
        res['status'] = False
        res['message'] = 'param not definition..'

    return res


class PlaybookRunnerCallbacks(callbacks.PlaybookRunnerCallbacks):
    def __init__(self, stats, verbose=None):
        super(PlaybookRunnerCallbacks, self).__init__(stats, verbose)
        print 'os:', os.getcwd()

    def _inster_nosql(self, host, res):
        # print 'inster nosql---', type(res), host, type(host)
        # print res.get('changed')

        r = OperationRedis()
        if type(res) == dict:
            status = res.get('changed')
            # tmp[host] = status
            cmd = res.get('cmd', '0')
            if 'wget' == cmd[0]:
                _key = cmd[3].split('download')[1].split('/')[1]
                tmp = host + ' :: ' + str(status) + ','
                if len(tmp) != 0:
                    # print '_key', tmp
                    r._append_data(_key, tmp)

    def _inster_db(self, host, res):

        # print 'inster _inster_db---', type(res), host, type(host), res.get('changed'), \
        #     res.get('delta', '0'), res.get('start', '0'), res.get('end', '0'), res.get('cmd', '0')
        host = '' if not host else host
        tmp = {}
        project_id = 2
        if type(res) == dict:
            status = res.get('changed')
            # tmp[host] = status
            delta = res.get('delta', '0')
            cmd = res.get('cmd', '0')

            DeployInfo.objects.create(host=host, status=status, delta=delta, desc=cmd)

        else:
            DeployInfo.objects.create(host=host, status=False, delta='1', desc=res)

    def on_ok(self, host, host_result):
        super(PlaybookRunnerCallbacks, self).on_ok(host, host_result)
        self._inster_nosql(host, host_result)
        self._inster_db(host, host_result)
        # print '===on_ok====host=%s===result=%s' % (host, host_result)

    def on_unreachable(self, host, results):
        super(PlaybookRunnerCallbacks, self).on_unreachable(host, results)
        self._inster_nosql(host, results)
        self._inster_db(host, results)
        # print '===on_unreachable====host=%s===result=%s' % (host, results)

    def on_failed(self, host, results, ignore_errors=False):
        super(PlaybookRunnerCallbacks, self).on_failed(host, results, ignore_errors)
        self._inster_nosql(host, results)
        self._inster_db(host, results)
        # print '===on_unreachable====host=%s===result=%s' % (host, results)

    def on_skipped(self, host, item=None):
        super(PlaybookRunnerCallbacks, self).on_skipped(host, item)
        self._inster_nosql(host, item)
        self._inster_db(host, item)
        # print "this task does not execute,please check parameter or condition."


class PlaybookCallbacks(callbacks.PlaybookCallbacks):
    def __init__(self, verbose=False):
        super(PlaybookCallbacks, self).__init__(verbose)

    def _inster_db(self, host, res):
        r = redis.Redis(host='192.168.99.61', port=6379, db=0)
        r.set(host, str(res))

    def on_stats(self, stats):
        super(PlaybookCallbacks, self).on_stats(stats)
        print"palybook executes completed===="


def _playbook(params, play_file):
    stats = callbacks.AggregateStats()
    playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
    runner_cb = PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)

    res = PlayBook(
        playbook=play_file,
        stats=stats,
        callbacks=playbook_cb,
        check=False,
        runner_callbacks=runner_cb,
        extra_vars=eval(params),
        forks=200
    )

    result = res.run()
    # print '-----', result
    res = playbook_cb.on_stats(res.stats)
    return res


if __name__ == '__main__':
    _playbook(params='', play_file='')
