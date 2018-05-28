#!/usr/bin/env python
# encoding: utf-8
# author: xiaofangliu

from helper import _playbook


# host_list
def _start_deploy(json_data, play_file):
    client_path = json_data.get('client_path', '/tmp')
    hosts = json_data.get('project_name', 'test')
    # hosts = 'test'
    print hosts
    package_url = json_data.get('package_url', '')
    package_name = json_data.get('package_name', '')

    params = '{"host": "%s", "package_url": "%s", "client_path": "%s", "package_name": "%s"}' % (hosts, package_url, client_path, package_name)
    play_file = './deploy/playbook/playbook.yml' if not play_file else play_file
    res = _playbook(params, play_file)
    print res