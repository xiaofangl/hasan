#!/usr/bin/env python
# coding=utf-8
from settings import *
from os.path import join, abspath, dirname

# make root path
here = lambda *x: join(abspath(dirname(__file__)), *x)
PROJECT_ROOT = here("..", "..")
root = lambda *x: join(abspath(PROJECT_ROOT), *x)

DEBUG = False

TIME_ZONE = 'Asia/Shanghai'
LANGUAGE_CODE = 'zh-hans'
LOGIN_URL = "/passport/login/"
LOGOUT_URL = "/passport/logout/"
LOGIN_REDIRECT_URL = "/passport/"
ALLOWED_HOSTS = [
]
INTERNAL_IPS = ['127.0.0.1']
INSTALLED_APPS += [
    'app01',
    'usejks',
    'dns_api',
    'deploy',
    'passport',
    'cmdb'
]

SMS = {
}

WEIXIN = {
}

WEIXIN_ADM = {

}

WX_CONF = {

}

API_SRV = {
    'erp': {
        'host': "http://.com",
        'authorization': '',
        'api': {
            "pdnames": "/api/v1/intapi/products/",
        },
    },
}

IMG_UPLOAD_URL = "http://img..com"

LOGGING_MIXIN_CONFIG = {
    "logging_methods": ['POST', 'PUT', 'PATCH', 'DELETE'],
}

AUTH = {
    "app_name": "deal",
    "app_key": "",
    "auth_login": "",
    "auth_info": "",
    "auth_mobile": "",
    "api_grouprole": "",
    "api_member": "",
    "api_groups": "",
}

CAPTCHA_BACKGROUND_COLOR = "#eee"
CAPTCHA_CHALLENGE_FUNCT = 'tools.helper.random_digit_challenge'

# REST_FRAMEWORK = {
#     'DEFAULT_AUTHENTICATION_CLASSES': ('tools.rest_helper.YMAuthentication',),
#     'DEFAULT_PAGINATION_CLASS': 'tools.rest_helper.YMPagination',
#     'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
# }
#
# PRODUCT_CATEGORY = (
#     (u'锯材', (('11', u'阔叶锯材'), ('12', u'针叶锯材'), ('13', u'名贵锯材'),)),
#     (u'原木', (('21', u'阔叶原木'), ('22', u'针叶原木'), ('23', u'名贵原木'),)),
#     (u'木皮', (('31', u'天然木皮'), ('32', u'染色木皮'), ('33', u'科技木皮'),)),
#     (u'人造板', (
#         ('41', u'密度板'), ('42', u'多层板/胶合板'), ('43', u'建筑混凝土模板'),
#         ('44', u'OSB'), ('45', u'刨花板'), ('46', u'细木工板'), ('47', u'指接拼板')
#     )),
# )

