#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu


from django.conf.urls import url
from views import *


urlpatterns = [
    url(r'^show_test/', test, name='show_test'),
    url(r'^show_test2/', test2, name='show_test2'),

]