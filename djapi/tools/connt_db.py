#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

import redis
import Queue

from django.conf import settings


def retry(times=1, exceptions=None):
    exceptions = exceptions if exceptions is not None else Exception

    def wrapper(func):
        def wrapper(*args, **kwargs):
            last_exception = None
            for _ in range(times):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    last_exception = e
            raise last_exception

        return wrapper

    return wrapper


class OperationRedis(object):
    def __init__(self):
        self.host = settings.REDIS_INFO.get('host')
        self.port = settings.REDIS_INFO.get('port')
        self.db = settings.REDIS_INFO.get('db')
        self.res = {}

    @retry(times=2, exceptions=None)
    def _conn_nosql(self):
        try:
            r = redis.Redis(host=self.host, port=self.port,
                            db=self.db)
        except Exception as e:
            r = e
        return r

    def _append_data(self, key, data):
        try:
            _conn = self._conn_nosql()
            _conn.append(key, data)
            self.res['status'] = True
        except Exception as e:

            self.res['status'] = False
            self.res['msg'] = e
        return self.res

    def _get_data(self, key):
        try:
            _conn = self._conn_nosql()
            tmp = _conn.get(key)
            _tmp = tmp.split(',')
            self.res['data'] = _tmp
            self.res['status'] = True
        except Exception as e:

            self.res['status'] = False
            self.res['msg'] = e
        return self.res

    def _delete_data(self, key):
        try:
            _conn = self._conn_nosql()
            _conn.delete(key)
            self.res['status'] = True
        except Exception as e:
            self.res['status'] = False
            self.res['msg'] = e
        return self.res
