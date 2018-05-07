#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

from django.http import JsonResponse

from log.logging_conf import *
from django.conf import settings
from tools.helper import execute_command
from tools.helper import create_file_hasan
from tools.helper import delete_file_hasan
from tools.helper import sync_file_hasan
from app01.models import DnsHost
from app01.models import DnsFiles
from tools.format_script import test_file
from tools.format_script import write_in_db


loger = logging.getLogger(__file__)


def get_file_list():
    res = {
        'status': True,
        'message': ''
    }
    tmp = []
    lan_dns_ip = settings.DNS_SERVER.get('lan_dns').get('ip')
    wan_dns_ip = settings.DNS_SERVER.get('wan_dns').get('ip')
    lan_ip = lan_dns_ip[0].split('.')[0]
    wan_ip = wan_dns_ip[0].split('.')[0]
    files = DnsFiles.objects.all().values('id', 'filename', 'file_to_host__desc')
    # print 'files', files
    print '====', lan_dns_ip, wan_dns_ip, lan_ip, type(lan_ip), wan_ip
    for item in files:
        if 'lan_dns' in item['file_to_host__desc']:
            filename = lan_dns_ip[0].split('.')[0] + '_' + item['filename']
        elif 'wan_dns' in item['file_to_host__desc']:
            filename = wan_dns_ip[0].split('.')[0] + '_' + item['filename']

        tmp.append(filename)
    res['data'] = set(tmp)
    print res['data']
    return res


def read_files(file_name):
    c = 0
    i = 1
    all_list = []
    #print 'file_name', file_name, type(file_name)
    with open(file_name, 'r') as f:
        line = f.readline()
        while line:
            line = f.readline()
            i += 1
            if i >= 10:
                # print '------------------------------'
                one_line = line.strip()
                # print 'i:', i, one_line.split(' ')
                one_line2 = one_line.replace('\t', ' ')
                #print 'i:', i, one_line2.split(' ')
                one_line3 = ' '.join(filter(lambda x: x, one_line2.split(' ')))
                # print 'i:', i, one_line3
                one_read = {
                    'id': '',
                    'type': '',
                    'host': '',
                    'ns_path': '-',
                    'value': '',
                    'mx': '-',
                    'ttl': '-',
                    'status': '-'
                }
                if len(one_line3) > 0:
                    c += 1
                    one_read['id'] = c
                    one_read['type'] = one_line3.split(' ')[2]
                    one_read['host'] = one_line3.split(' ')[3]
                    one_read['value'] = one_line3.split(' ')[0]
                    one_read['file_name'] = file_name

                    all_list.append(one_read)
    #print 'all_list:', len(all_list)
    return all_list


def write_files(file_name, host, type, value, *args, **kwargs):
    res = {
        'status': True,
        'message': ''
    }

    one_line = host + '\t' + ' ' + 'IN' + '\t' + ' ' + type + '\t' + ' ' + value
    print 'one_line', one_line

    try:
        with open(file_name, 'a+') as f:
            f.write(one_line+'\n')
        loger.info('write one item...')
        loger.info(one_line)
    except:
        res['status'] = False
        res['message'] = 'file wirte false！'
        loger.warning('file wirte false！')
        loger.warning(one_line)
    return res


def mod_files(file_name, host, type, value, *args, **kwargs):
    res = {
        'status': True,
        'message': ''
    }

    rece_line = value + '\t' + ' ' + 'IN' + '\t' + ' ' + type + '\t' + ' ' + host
    run_os = settings.SYSTEM_OS.get('os')
    #cmd_linux = 'sed -i "0,/%s/{/%s/d}" %s' % (rece_line, rece_line, file_name)
    #cmd_mac = 'sed -i "_bak" "0,/%s/{/%s/d}" %s' % (rece_line, rece_line, file_name)
    cmd_linux = 'sed -i "/%s/d" %s' % (rece_line, file_name)
    cmd_mac = 'sed -i "_bak" "/%s/d" %s' % (rece_line, file_name)

    #print cmd_mac
    try:
        # mac = execute_command('sed -i "_bak" "/test16       IN      A   1.1.1.25/d" 192_huashenghaoche.net.zone')
        if run_os == 'linux':
            execute_command(cmd_linux)
        else:
            execute_command(cmd_mac)
        loger.info('delect item success!')
        loger.info(rece_line)
    except Exception as e:
        res['status'] = False
        res['message'] = 'delect item success!!'
        loger.warning('delect item false!')
        loger.warning(rece_line)
    return res

"""
返回 vue_table 数据类型
    {
  "status": true,
  "message": "",
  "data": {
    "huashenghaoche.net.zone": [
      [
        {
          "ip": "192.168.99.251",
          "env": "lan_dns"
        },
        {
          "ip": "192.168.99.252",
          "env": "lan_dns"
        }
      ]
    ],
    "huashenghaoche.work.zone": [
      [
        {
          "ip": "192.168.99.251",
          "env": "lan_dns"
        },
        {
          "ip": "192.168.99.252",
          "env": "lan_dns"
        }
      ]
    ],
    "huashenghaoche.com.zone": [
      [
        {
          "ip": "172.30.5.135",
          "env": "wan_dns"
        },
        {
          "ip": "172.30.5.145",
          "env": "wan_dns"
        },
        {
          "ip": "192.168.99.251",
          "env": "lan_dns"
        },
        {
          "ip": "192.168.99.252",
          "env": "lan_dns"
        }
      ]
    ]
  }
}

"""


def query_list():
    res = {
        'status': True,
        'message': ''
    }
    tmp = {}
    files = DnsFiles.objects.all()
    for item in files:
        list2 = []
        list3 = []
        item_host = item.file_to_host.all()
        for i in item_host:
            tmp2 = {}
            tmp2['ip'] = i.host
            tmp2['env'] = i.desc
            list2.append(tmp2)
        list3.append(item.filename)
        list3.append(list2)
        list3.append(item.id)
        tmp[item.filename] = list3
    res['data'] = tmp
    return res


def create_files(host, name, *args, **kwargs):
    print os.getcwd()
    print 'params', host, name
    res = {
        'status': True,
        'message': ''
    }
    files = DnsFiles()
    files.filename = name
    files.save()
    host_ip = []
    if len(host) > 1:
        try:
            reco = DnsHost.objects.filter(desc=host[0])
            reco2 = DnsHost.objects.filter(desc=host[1])
            for i in reco:
                host_ip.append(i.host)
                # print i.host, i.desc
                files.file_to_host.add(i.id)
            for c in reco2:
                host_ip.append(c.host)
                # print c.host, c.desc
                files.file_to_host.add(c.id)
            # host_ip = set(host_ip)
            print 'host_ip', host_ip
            res = create_file_hasan(host_ip, name)

        except:
            res['status'] = False
            res['message'] = ' create file failed 0 ..'
    else:
        try:
            reco = DnsHost.objects.filter(desc=host[0])
            for i in reco:
                host_ip.append(i.host)
                # print i.host, i.desc
                files.file_to_host.add(i.id)
            # host_ip = set(host_ip)
            print 'host_ip', host_ip
            res = create_file_hasan(host_ip, name)

        except:
            res['status'] = False
            res['message'] = ' create file failed 1..'
    loger.info(res)

    return res


def run_del(res, b, info):
    try:
        reco = DnsHost.objects.filter(desc=info)
        for item in reco:
            item.dnsfiles_set.all()
            item.dnsfiles_set.remove(b)
        res['message'] = ' run_del success ..'
    except:
        res['status'] = False
        res['message'] = ' run_del failed ..'
    loger.warning(res)
    return res


def delete_files(host, name, file_id,  *args, **kwargs):
    # print 'params', host, name, host[0]
    res = {
        'status': True,
        'message': ''
    }
    host_ip = []
    res_file = DnsFiles.objects.filter(id=file_id).values('file_to_host__host', 'file_to_host__desc')
    # print 'res_file', res_file

    b = DnsFiles.objects.get(id=file_id)
    # b.file_to_host.all()

    if len(res_file) == 2:
        # 只有一组主机，删除多对多记录 删除zone文件.传过来的host 必然是1
        # print reco.values('host', 'desc', 'id')
        # b.file_to_host.remove(reco)
        str_host = host[0]
        for n in res_file:
            # print n
            if host[0] == n['file_to_host__desc']:
                host_ip.append(n['file_to_host__host'].split('.')[0])
        host_ip = set(host_ip)
        # print 'host_ip', host_ip
        res = delete_file_hasan(host_ip, name)

        res = run_del(res, b, str_host)
        b.delete()

    elif len(res_file) == 4:
        # 两组主机
        if len(host) > 1:
            # 两组主机都删， 删除多对多，删除zone文件
            str_host = host[0]
            str2_host = host[1]
            for n in res_file:
                # print n
                if str_host == n['file_to_host__desc']:
                    host_ip.append(n['file_to_host__host'].split('.')[0])
                elif str2_host == n['file_to_host__desc']:
                    host_ip.append(n['file_to_host__host'].split('.')[0])
            host_ip = set(host_ip)
            # print 'host_ip', host_ip
            res = delete_file_hasan(host_ip, name)

            res = run_del(res, b, str_host)
            res = run_del(res, b, str2_host)
            b.delete()

        else:
            # 只删一组， 删除多对多对应的记录。不删除zone文件
            str_host = host[0]
            for n in res_file:
                # #print n
                if host[0] == n['file_to_host__desc']:
                    host_ip.append(n['file_to_host__host'].split('.')[0])
            host_ip = set(host_ip)
            #print 'host_ip', host_ip
            res = delete_file_hasan(host_ip, name)

            res = run_del(res, b, str_host)

    loger.info(res)

    return res


def rsync_files(host, name, is_exist, *args, **kwargs):
    #print 'rsync_files', host, name, is_exist
    res = {
        'status': True,
        'message': "%s rsync_files %s host success.." % (name, host)
    }
    host_ip = []
    files = DnsFiles.objects.filter(filename=name).values('id', 'file_to_host__host', 'filename', 'file_to_host__desc')
    # #print 'files', files
    for item in files:
        host_ip.append(item['file_to_host__host'].split('.')[0])
    host_ip = set(host_ip)
    #print host_ip
    if len(host_ip) == 1:
        res = sync_file_hasan(host_ip, name)

    f = DnsFiles.objects.get(filename=name)

    if len(host) > 1:

        reco = DnsHost.objects.filter(desc=host[0])
        for i in reco:
            # #print i.host, i.desc
            f.file_to_host.add(i.id)

        reco = DnsHost.objects.filter(desc=host[0])
        for i in reco:
            # #print i.host, i.desc
            f.file_to_host.add(i.id)
    else:

        try:
            reco = DnsHost.objects.filter(desc=host[0])
            for i in reco:
                # print i.host, i.desc
                f.file_to_host.add(i.id)
        except:
            res['status'] = False
            res['message'] = ' rsync_files file failed 1..'

    loger.info(res)

    return res


def format_files(host, names, *args, **kwargs):
    print 'format_files', host, names
    name = "tools/tmp.zone"
    res = {}
    # 格式化 ip_file 到本地，上传新文件
    for item in host:
        if "lan_dns" in item:
            print "lan_dns"
            host_ip = settings.DNS_SERVER.get('lan_dns').get('ip')[0].split('.')[0]
            dis_filename = host_ip + '_' + names
            _format = test_file(name, dis_filename)
            if _format['status']:
                res = write_in_db(host[0], names)
            else:
                logging.info(res)
        elif "wan_dns" in item:
            print "wan_dns"
            host_ip = settings.DNS_SERVER.get('wan_dns').get('ip')[0].split('.')[0]
            dis_filename = host_ip + '_' + names
            _format = test_file(name, dis_filename)
            if _format['status']:
                res = write_in_db(host[1], names)
            else:
                logging.info(res)
        logging.info(res)
    execute_command('rm -fr %s' % name)
    print res
    return res

if __name__ == '__main__':
    # read_files('172_huashenghaoche.com.zone')
    # read_files('192_huashenghaoche.com.zone')
    print os.getcwd()
    loger.info('statrt print log')