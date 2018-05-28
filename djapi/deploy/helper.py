#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

import os
import redis
import ansible.runner
from ansible.playbook import PlayBook
from ansible import callbacks
from ansible import utils

from models import DeployInfo
from passport.models import userInfo

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


def get_userinfo(request):
    username = request.META.get('HTTP_AUTHORIZATION', '')
    user_id = userInfo.objects.filter(hashKey=username).values('user_id')
    return user_id


class PlaybookRunnerCallbacks(callbacks.PlaybookRunnerCallbacks):
    def __init__(self, stats, verbose=None):
        super(PlaybookRunnerCallbacks, self).__init__(stats, verbose)
        print 'os:', os.getcwd()

    def _inster_nosql(self, host, res):
        r = redis.Redis(host='192.168.99.61', port=6379, db=0)
        r.set(host, res)

    def _inster_db(self, host, res):
        host = '' if not host else host
        print type(res)
        std = res.get('stderr', 'stdout')
        if res.get('changed'):
            status = True
        elif '100%' or '0K' in std:
            status = True
        else:
            status = False
        packges = res.get('cmd', '')
        start = res.get('start', '')
        end = res.get('end', '')
        delta = res.get('delta', '')
        user_id = ''
        DeployInfo.objects.get_or_create(user=user_id, host=host, status=status, packges=packges,\
                                         start_time=start, end_time=end, delta=delta, deploy_env='pro',\
                                         desc=std)

    def on_ok(self, host, host_result):
        super(PlaybookRunnerCallbacks, self).on_ok(host, host_result)
        self._inster_nosql(host, host_result)
        self._inster_db(host, host_result)
        print '===on_ok====host=%s===result=%s' % (host, host_result)

    def on_unreachable(self, host, results):
        super(PlaybookRunnerCallbacks, self).on_unreachable(host, results)
        self._inster_nosql(host, results)
        self._inster_db(host, results)
        print '===on_unreachable====host=%s===result=%s' % (host, results)

    def on_failed(self, host, results, ignore_errors=False):
        super(PlaybookRunnerCallbacks, self).on_failed(host, results, ignore_errors)
        self._inster_nosql(host, results)
        self._inster_db(host, results)
        print '===on_unreachable====host=%s===result=%s' % (host, results)

    def on_skipped(self, host, item=None):
        super(PlaybookRunnerCallbacks, self).on_skipped(host, item)
        self._inster_nosql(host, item)
        self._inster_db(host, item)
        print "this task does not execute,please check parameter or condition."


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
