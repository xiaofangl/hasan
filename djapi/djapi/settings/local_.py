#!/usr/bin/env python
# coding=utf-8

from base import *

DEBUG = True

# DATABASE_ROUTERS = ['tools.db_router.YerpRouter']

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'yweb',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

JENKINS_INFO = {
    'test': {
        'host': 'http://test.jenkins.huashenghaoche.com',
        'username': 'admin',
        'password': 'admin',
        'api': {
            'python_api': '/api/python?pretty=true'
        }
    }
}


