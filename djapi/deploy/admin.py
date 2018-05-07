#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu
from django.contrib import admin

# Register your models here.

import requests
import re

"""
def _project_file_list():
    r = requests.get('http://192.168.100.42:55555/download/')
    c = requests.get('http://192.168.100.42:55555/download/huasheng_jave_test/')
    # print '----', c.text
    # pattern = '<a.*?href="([^"]*)".*?>([\S\s]*?)</a>'
    p = re.compile(r'<a.*?href="([^"]*)".*?>([\S\s]*?)</a>+')
    ret = p.findall(c.text)
    tmp = []
    for item in ret[5:]:
        _item = set(item)
        tmp.append(_item)
    print 'i', tmp, c.url
    res = p.findall(r.text)
    # print 'i', res[5:], r.url
    # s = p.finditer(c.text)
    # for i in s:
    #     print 's', i.group()
"""


# 接收一个url 获取url 下的 jar包list
def get_package_list(url):
    res = {
        'status': True,
        'msg': ''
    }
    p = re.compile(r'<a.*?href="([^"]*)".*?>([\S\s]*?)</a>+')

    reco = requests.get(url)
    if reco:
        ret = p.findall(reco.text)
        _tmp = []
        for item in ret[5:]:
            # print item[0]
            _item = item[0]
            _tmp.append(_item)
        res['data'] = _tmp
        res['url'] = reco.url
    else:
        res['status'] = False
        res['msg'] = 'Not Open Url...'
    return res


def format_url(start, url, end):
    _start = url.startswith(start)
    _end = url.endswith(end)
    if _start and _end:
        pass
    elif _start:
        url = url + end
    elif _end:
        url = url + start
    else:
        url = start + url + end
    print url
    return url

if __name__ == '__main__':
    r = '192.168.100.42:55555/download'
    # p = re.compile(r'^http.+?\/$')
    # _url = p.match(r)
    # print _url.group()
    format_url('', r, '/')