#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

import os
import json
import ansible.runner
from ansible.playbook import PlayBook
from ansible.inventory import Inventory
from ansible import callbacks
from ansible import utils


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

    def on_ok(self, host, host_result):
        super(PlaybookRunnerCallbacks, self).on_ok(host, host_result)
        print '===on_ok====host=%s===result=%s' % (host, host_result)

    def on_unreachable(self, host, results):
        super(PlaybookRunnerCallbacks, self).on_unreachable(host, results)
        print '===on_unreachable====host=%s===result=%s' % (host, results)

    def on_failed(self, host, results, ignore_errors=False):
        super(PlaybookRunnerCallbacks, self).on_failed(host, results, ignore_errors)
        print '===on_unreachable====host=%s===result=%s' % (host, results)

    def on_skipped(self, host, item=None):
        super(PlaybookRunnerCallbacks, self).on_skipped(host, item)
        print "this task does not execute,please check parameter or condition."


class PlaybookCallbacks(callbacks.PlaybookCallbacks):
    def __init__(self, verbose=False):
        super(PlaybookCallbacks, self).__init__(verbose)

    def on_stats(self, stats):
        super(PlaybookCallbacks, self).on_stats(stats)
        print"palybook executes completed===="


hosts = ['192.168.99.252', '127.0.0.1']
inventory = Inventory(hosts)

stats = callbacks.AggregateStats()
runner_cb = PlaybookRunnerCallbacks(stats, verbose=utils.VERBOSITY)
playbook_cb = PlaybookCallbacks()
print 'this', os.getcwd()
res = PlayBook(
    playbook='./playbook/playbook.yml',
    stats=stats,
    callbacks=playbook_cb,
    runner_callbacks=runner_cb,
    inventory=inventory,
    forks=200
)
result = res.run()
playbook_cb.on_stats(res.stats)
