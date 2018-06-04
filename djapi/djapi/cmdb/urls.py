#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

from django.conf.urls import url
from api import *

urlpatterns = [
    url(r'^list/', list, name='list'),
    url(r'^add_item/', add_item, name='add_item'),
    url(r'^mod_item/', mod_item, name='mod_item'),
    url(r'^del_item/', del_item, name='del_item'),
    url(r'^search_one/', search_one, name='search_one')
]