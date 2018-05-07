#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

from django.conf.urls import url
from views import login, reset_password, signup
from apps import add_group, get_users
from api import *

urlpatterns = [
    url(r'^login/$', login, name='passport_login'),
    url(r'^reset_password/$', reset_password, name='reset_password'),
    url(r'^signup/$', signup, name='passport_signup'),

    url(r'^add_group/$', add_group, name='passport_add_group'),

    # url(r'^get_users/$', get_users, name='passport_get_users'),

    url(r'^list/$', list, name='passport_list'),
    url(r'^is_group/$', is_group, name='passport_is_group'),
    url(r'^user_group/$', user_group, name='passport_user_group'),
    url(r'^reset_pawd_api/$', reset_pawd_api, name='passport_reset_pawd_api'),
    url(r'^user_add_group/$', user_add_group, name='passport_user_add_group'),
    url(r'^user_del_group/$', user_del_group, name='passport_user_del_group'),
    url(r'^apply_permission/$', apply_permission, name='passport_apply_permission'),
    url(r'^apply_dbmain/$', apply_dbmain, name='passport_apply_dbmain')

]