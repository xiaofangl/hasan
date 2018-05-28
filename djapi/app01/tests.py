#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

import os
from tools.helper import execute_command


def update_branch(file_name):
    # file_name = '' if not file_name else file_name
    branch_p = "sed -n '3p' %s" % file_name
    _branch = int(branch_p.split(';')[0].strip()).__add__(1)
    branch = '                        ' + str(_branch) + ';' + branch_p.split(';')[1]
    _cmd = "sed -i -e '3s/^.*$/%s/' %s" % (branch, file_name)
    res = execute_command(_cmd)
    print res
    # loger.info(_branch)
    # loger.info('update branch success...')
    return res

if __name__ == '__main__':
    print '_______', os.getcwd()
    update_branch('../../upload_tmp/tmp.zone')
