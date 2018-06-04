#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

from django.conf.urls import url
from api import *

urlpatterns = [
    url(r'^list/', test, name='test'),
    url(r'^get_all_job/', list_jobs, name='list_jobs')
]