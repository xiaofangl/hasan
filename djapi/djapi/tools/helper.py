#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

import shlex
import datetime
import subprocess
import time

from django.conf import settings
from log.logging_conf import *

loger = logging.getLogger(__file__)


def execute_command(cmdstring, cwd=None, timeout=None, shell=False):
    """执行一个SHELL命令
        封装了subprocess的Popen方法, 支持超时判断，支持读取stdout和stderr
        参数:
      cwd: 运行命令时更改路径，如果被设定，子进程会直接先更改当前路径到cwd
      timeout: 超时时间，秒，支持小数，精度0.1秒
      shell: 是否通过shell运行
    Returns: return_code
    Raises: Exception: 执行超时
    """
    if shell:
        cmdstring_list = cmdstring
    else:
        cmdstring_list = shlex.split(cmdstring)
    if timeout:
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)

    # 没有指定标准输出和错误输出的管道，因此会打印到屏幕上；
    sub = subprocess.Popen(cmdstring_list, cwd=cwd, stdin=subprocess.PIPE, shell=shell, bufsize=4096)

    # subprocess.poll()方法：检查子进程是否结束了，如果结束了，设定并返回码，放在subprocess.returncode变量中
    while sub.poll() is None:
        time.sleep(0.1)
        if timeout:
            if end_time <= datetime.datetime.now():
                raise Exception("Timeout：%s" % cmdstring)

    return str(sub.returncode)


def execute_command_2(cmdstring, timeout=None, shell=False):
    """执行一个SHELL命令
        封装了subprocess的Popen方法, 支持超时判断，支持读取stdout和stderr
        参数:
      cwd: 运行命令时更改路径，如果被设定，子进程会直接先更改当前路径到cwd
      timeout: 超时时间，秒，支持小数，精度0.1秒
      shell: 是否通过shell运行
    Returns: return_code
    Raises: Exception: 执行超时
    """
    res = {}
    if shell:
        cmdstring_list = cmdstring
    else:
        cmdstring_list = shlex.split(cmdstring)
    if timeout:
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)

    # ；
    sub = subprocess.Popen(cmdstring_list, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    # subprocess.poll()方法：检查子进程是否结束了，如果结束了，设定并返回码，放在subprocess.returncode变量中
    while sub.poll() is None:
        print '+++++++++++='
        # print sub.stdout
        line = sub.stdout.read()
        line = line.strip()
        tmp = line.split("\n")
        time.sleep(0.1)
        # print 'line', line
        if timeout:
            if end_time <= datetime.datetime.now():
                raise Exception("Timeout：%s" % cmdstring)
    res['status'] = str(sub.returncode)
    res['data'] = tmp
    return res


def create_file_hasan(host_ip, name, *args, **kwargs):
    print 'create_file_hasan', host_ip, name
    res = {
        'status': True,
        'message': ''
    }
    # 文件头
    files = name.split('.')[0] + '.' + name.split('.')[1] + '.'
    ns_var = 'ns' + '.' + files
    ns_var_ = 'ns2' + '.' + files
    root_var = 'root' + '.' + files
    two_line = settings.DNS_MODELFILE.get('2') % (ns_var, root_var)
    eight_line = settings.DNS_MODELFILE.get('8') % ns_var
    eight_line_ = settings.DNS_MODELFILE.get('9') % ns_var_
    # print files, ns_var, root_var
    # print "++++++++++++++++++++++++++++++++++"
    # print two_line
    # print eight_line
    head_list = []
    try:
        for i in host_ip:
            head_list.append(i.split('.')[0])
        head_list = set(head_list)
        print 'head', head_list
        for item in head_list:
            filename = item + '_' + name
            new_file = 'touch %s' % filename
            execute_command(new_file)

            if item == settings.DNS_SERVER.get('lan_dns').get('ip')[0].split('.')[0]:
                nine_line = 'ns' + '\t' + ' ' + 'IN' + '\t' + ' ' + 'A' + '\t' + ' ' + settings.DNS_SERVER.get('lan_dns').get('ip')[0]
                teen_line = 'ns2' + '\t' + ' ' + 'IN' + '\t' + ' ' + 'A' + '\t' + ' ' + \
                            settings.DNS_SERVER.get('lan_dns').get('ip')[1]
            elif item == settings.DNS_SERVER.get('wan_dns').get('ip')[0].split('.')[0]:
                nine_line = 'ns' + '\t' + ' ' + 'IN' + '\t' + ' ' + 'A' + '\t' + ' ' + settings.DNS_SERVER.get('wan_dns').get('ip')[0]
                teen_line = 'ns2' + '\t' + ' ' + 'IN' + '\t' + ' ' + 'A' + '\t' + ' ' + \
                            settings.DNS_SERVER.get('wan_dns').get('ip')[1]
            print 'nine_line', nine_line
            # 写文件
            try:
                with open(filename, 'a+') as f:
                    f.write(settings.DNS_MODELFILE.get('1') + '\n')
                    f.write(two_line + '\n')
                    f.write(settings.DNS_MODELFILE.get('3') + '\n')
                    f.write(settings.DNS_MODELFILE.get('4') + '\n')
                    f.write(settings.DNS_MODELFILE.get('5') + '\n')
                    f.write(settings.DNS_MODELFILE.get('6') + '\n')
                    f.write(settings.DNS_MODELFILE.get('7') + '\n')
                    f.write(eight_line + '\n')
                    f.write(eight_line_ + '\n')
                    f.write(nine_line + '\n')
                    f.write(teen_line + '\n')

                res['message'] = '%s create_file_hasan success..' % filename
            except:
                res['status'] = False
                res['message'] = '%s create_file_hasan failed..' % filename
    except:
        res['status'] = False
        res['message'] = '%s create_file_hasan failed..' % filename
    loger.warning(res)
    return res


def delete_file_hasan(host_ip, name, *args, **kwargs):
    print 'params', host_ip, name
    res = {
        'status': True,
        'message': ''
    }
    try:
        for i in host_ip:
            filename = i + '_' + name
            del_comm = 'rm -fr %s' % filename
            execute_command(del_comm)
            res['message'] = '%s delete_file_hasan success..' % filename
    except:
        res['status'] = False
        res['message'] = '%s delete_file_hasan failed..' % filename
    loger.warning(res)
    return res


def sync_file_hasan(host_ip, name, *args, **kwargs):
    print 'create_file_hasan', host_ip, name
    lan_dns_ip = settings.DNS_SERVER.get('lan_dns').get('ip')
    wan_dns_ip = settings.DNS_SERVER.get('wan_dns').get('ip')
    lan_ip = lan_dns_ip[0].split('.')[0]
    wan_ip = wan_dns_ip[0].split('.')[0]
    print '====', lan_dns_ip, wan_dns_ip, wan_ip, lan_ip
    res = {
        'status': True,
        'message': ''
    }
    try:
        for i in host_ip:
            if i == wan_ip:
                filename = i + '_' + name
                comm = 'find ./ -name *%s' % name
                reco = execute_command(comm)
                # print 'reco', reco, type(reco)
                # print '+++++++++++++++++++++++++++++++'
                if reco == '0':
                    descname = lan_ip + '_' + name
                    cp_comm = 'cp -fr %s %s' % (filename, descname)
                    execute_command(cp_comm)
                    res['message'] = '%s sync_file_hasan %s success..' % (filename, descname)
            elif i == lan_ip:
                filename = i + '_' + name
                comm = 'find ./ -name *%s' % name
                reco = execute_command(comm)
                print 'reco', reco,
                print '+++++++++++++++++++++++++++++++'
                if reco == '0':
                    descname = wan_ip + '_' + name
                    cp_comm = 'cp -fr %s %s' % (filename, descname)
                    execute_command(cp_comm)
                    res['message'] = '%s sync_file_hasan %s success..' % (filename, descname)
    except:
        res['status'] = False
        res['message'] = '%s sync_file_hasan failed..' % filename
    loger.warning(res)
    return res


if __name__ == '__main__':
    execute_command('uname')
    execute_command('pwd')
    execute_command('sed -i "_bak" "/test16       IN      A   1.1.1.25/d" ../192_huashenghaoche.net.zone')
