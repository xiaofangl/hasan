#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

from django.conf.urls import url
from views import test
from api import *

urlpatterns = [
    url(r'^test/', test, name='test'),
    url(r'^list/?', list, name='list'),
    url(r'^package_list/?', package_list, name='package_list'),
    url(r'^run_deploy/?', run_deploy, name='run_deploy'),

    url(r'^add_item/', add_item, name='add_item'),
    url(r'^mod_item/?', mod_item, name='mod_item'),
    url(r'^del_item/?', del_item, name='del_item')

]