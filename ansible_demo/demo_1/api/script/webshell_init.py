#!/usr/bin/env  python
# -*- coding: utf-8 -*-

import ConfigParser

class Ssh_Info(object):
    def __init__(self, span_file='/etc/ansible/hosts'):
        self.common_set = ConfigParser.RawConfigParser(allow_no_value=True)
        self.common_set.read(span_file)
        self.headers = self.common_set.sections()
        self.infos = []

    def get_all_info(self):
        for i in self.headers:
            info = {}
            info['ip'] = ''
            info['name'] = ''
            info['port'] = ''
            info['user'] = ''
            items = self.common_set.options(i)
            info['name'] = i
            for attr in items:
                nx = self.common_set.get(i, attr)
                if nx == None:
                    info['ip'] = attr
                else:
                    nx = attr + '=' + self.common_set.get(i, attr)
                    for j in nx.split(' '):
                        if nx.find('ansible_ssh_host') != -1 and j.find('ansible_ssh_host') != -1:
                            info['ip'] = j.replace('ansible_ssh_host=','')
                        if nx.find('ansible_ssh_host') == -1:
                            info['ip'] = nx.split()[0]
                        if j.find('ansible_ssh_port') != -1:
                            info['port'] = j.replace('ansible_ssh_port=','')
                        if j.find('ansible_ssh_user') != -1:
                            info['user'] = j.replace('ansible_ssh_user=','')
            self.infos.append(info)
        for i in self.infos:
            initcommand = 'ssh '
            if i['port']:
                initcommand += '-p ' + i['port'] + ' '
            if i['user']:
                initcommand += i['user'] + '@'
            initcommand += i['ip']
            i['initcommand'] = initcommand
        return self.infos

    def define_info(self, item):
        infos_c.get_all_info()
        for i in self.infos:
            if i['name'] == item:
                return i
            else:
                pass
        return item + 'not found'

if __name__ == '__main__':
    infos_c = Ssh_Info()
    infos_c.get_all_info()
    print infos_c.define_info('nebulaplus-app-02')
