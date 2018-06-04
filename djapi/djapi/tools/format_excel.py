#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

import xlrd
import json
import os
from django.shortcuts import HttpResponse

# from app01.models import UpdateFiles
from passport.apps import login_required_hasan
from django.views.decorators.csrf import csrf_exempt
import django.http.request


def test():
    read_data = xlrd.open_workbook("test.xlsx")

    read_data.nsheets
    read_data.sheet_names()
    sh = read_data.sheet_by_index(0)
    print sh.name, sh.nrows, sh.ncols

    sh.cell_value(rowx=26, colx=3)

    for rx in range(sh.nrows):
        print sh.row(rx)


@csrf_exempt
# @login_required_hasan
def api_upload(request):
    print 'api_upload', request
    data = request.body
    # print 'data', data
    # data1 = json.loads(request.body('data', ''))
    # data1 = json.loads(request.body)
    # data2 = data1.get('name', '')
    # print data
    file_name = "tools/tmp.zone"
    f = open(file_name, 'w')
    f.write(data)
    f.close()

    ret = {'status': True, 'path': 'test_file'}
    return HttpResponse(ret)