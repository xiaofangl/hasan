#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

from django.conf.urls import url
from api import *
from oper import get_file_list

urlpatterns = [
    url(r'^dns_test/', test, name='test'),
    url(r'^list/', list, name='list'),
    url(r'^add_item/', add_item, name='add_item'),
    url(r'^mod_item/', mod_item, name='mod_item'),

    url(r'^get_file_list', get_file_list, name='get_file_list'),

    url(r'^file_list', file_list, name='file_list'),
    url(r'^add_file/', add_file, name='add_file'),
    url(r'^del_file/', del_file, name='del_file'),
    url(r'^copy_file/', copy_file, name='copy_file'),
    url(r'^upload_file/', upload_file, name='upload_file')
]