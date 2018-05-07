#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

import jenkins

from django.conf import settings
from log.logging_conf import *


loger = logging.getLogger(__file__)


class jenkins_tools(object):
    def __init__(self, jks_env='test', *args, **kwargs):
        self.jks_env = settings.JENKINS_INFO.get(jks_env)
        self.jks_host = settings.JENKINS_INFO.get(jks_env).get('host')
        self.jks_user = settings.JENKINS_INFO.get(jks_env).get('username')
        self.jks_pawd = settings.JENKINS_INFO.get(jks_env).get('password')
        self.jks_api = settings.JENKINS_INFO.get(jks_env).get('api').get('python_api')

    def _conn_jks(self):
        try:
            server = jenkins.Jenkins(self.jks_host, username=self.jks_user, password=self.jks_pawd)
            return server
        except Exception:
            loger.warning('conn jenkins faild!')
            return None

    def _jobs_list(self):
        server = self._conn_jks()
        if server:
            all_jobs = server.get_all_jobs()
            # for item in all_jobs:
            #     print('name: %s' % item['name'], 'URL: ', item['url'])
        else:
            loger.warning('conn jenkins faild!')
            all_jobs = {}

        return all_jobs
