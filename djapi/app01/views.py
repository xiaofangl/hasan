#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu


from django.shortcuts import render, render_to_response
from django.http import HttpResponse, JsonResponse
import json


def test(request):
    print '11', request.method, request
    name = '222'
    res = {
        'status': True,
        'msg': 'good job',
        'code': '200'
    }
    print res
    return JsonResponse(res)


class test2(object):
    def __init__(self, name):
        self.name = name

    @classmethod
    def get(self, request):
        res = {
            'status': True,
            'msg': 'good job'
        }
        print res
        return JsonResponse(res)
