#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu
import os
import re

"""
    re.search(r"(([01]?\d?\d|2[0-4]\d|25[0-5])\.){3}([01]?\d?\d|2[0-4]\d|25[0-5]\.)"
"""


# 打开文件找到 地方， 替换
# with open(file_name, 'r+') as f:
#     line = f.readline()
#     while line:
#         if group in line:
#             f.seek(f.tell(), 0)
#             host = host + "\n"
#             f.write(host)
#             break
#         line = f.readline()
#      i += 1


# find group add host
def add_host(file_name, host, group):
    print file_name, host, group
    res = {
        'status': True,
        'message': ''
    }
    file_name = './deploy/hosts' if not file_name else file_name
    try:
        i = 1
        with open(file_name, 'r') as f:
            with open(file_name, 'r+') as f_w:
                line = f.readline()
                while line:
                    if group in line:
                        f_w.seek(f.tell(), 0)
                        host = host + "\n"
                        f_w.write(host)
                        next_line = f.readline()
                        while next_line:
                            f_w.write(next_line)
                            next_line = f.readline()
                        f_w.truncate()
                        break
                    line = f.readline()
                    i += 1
    except IOError:
        res['status'] = False
        res['message'] = 'file wirte false！'
    return res


# sed
def del_host(file_name, host, group):
    res = {
        'status': True,
        'message': ''
    }
    print 'host, group', host, group,
    file_name = './deploy/hosts' if not file_name else file_name
    try:
        i = 1
        with open(file_name, 'r') as f:
            line = f.readline()
            # print f.tell()
            while line:
                if group in line:
                    _this = f.tell()
                    break
                line = f.readline()
                i += 1
            else:
                _this = False

        i = i + 1
        with open(file_name, 'r') as f_r:
            lines = f_r.readlines()
            f_r.seek(_this, 0)
            line = f_r.readline()
            while line:
                if "[" in line:
                    _end = f_r.tell()
                    break
                if i == len(lines):
                    print i, lines
                    _end = f_r.tell()
                    print 'last line', _end
                    break
                line = f_r.readline()
                i += 1
            else:
                _end = False
        print 'start, end', _this, _end
        if _this == False:
            res['status'] = False
            res['message'] = 'start  false！'
        elif _end == False:
            res['status'] = False
            res['message'] = 'end  false！'
        elif _this == _end:
            res['status'] = False
            res['message'] = '_this == _end！'
        else:
            print 'start, end', _this, _end
            try:
                with open(file_name, 'r') as f_r:
                    with open(file_name, 'r+') as f_w:
                        f_r.seek(_this, 0)
                        line = f_r.readline()
                        host_list = []
                        while line and f_r.tell() <= _end:
                            host = "192.168.100.44" if not host else host
                            print(line, f_r.tell())
                            host_list.append(f_r.tell())
                            if line.strip().replace('/n', '') == host:
                                _host = f_r.tell()
                                print f_r.tell()
                                if len(host_list) > 1:
                                    for i in host_list:
                                        if i == _host:
                                            now_location = host_list[host_list.index(i) - 1]
                                else:
                                    now_location = _this
                                print 'now_location', now_location
                                print 'host it..', line, i
                                f_w.seek(now_location, 0)
                                # f_r.readline()
                                print 'i', i, line
                                next_line = f_r.readline()
                                print 'i--', i, next_line
                                # next_line = line
                                while next_line:
                                    # print 'next line', next_line
                                    f_w.write(next_line)
                                    next_line = f_r.readline()
                                # break
                                f_w.truncate()
                            line = f_r.readline()
            except Exception as e:
                res['status'] = False
                res['msg'] = e

    except Exception as e:
        res['status'] = False
        res['msg'] = e
    return res


if __name__ == '__main__':
    print os.getcwd()
    # fr = open('./hosts', 'r')
    # c = fr.readline()
    # print 'c:: ', c
    del_host('./hosts', '192.168.99.25x', 'vue_test')
