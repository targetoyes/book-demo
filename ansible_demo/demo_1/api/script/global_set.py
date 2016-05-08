#!/usr/bin/env  python
# -*- coding: utf-8 -*-
# use for git api

import ConfigParser
import base64
import sys
import os
from random import choice
from string import ascii_uppercase

reload(sys)
sys.setdefaultencoding('utf-8')

home_auto_dir = os.path.abspath('.') + '/'

class Global_Set(object):

    def __init__(self):
        self.common_set = ConfigParser.RawConfigParser(allow_no_value=True)
        self.new_common_set = ConfigParser.RawConfigParser(allow_no_value=True)
        self.local_ini = home_auto_dir + 'local_settings.ini'
        self.common_set.read(self.local_ini)

    def get_all_data(self):
        a_d = {}
        for option in self.common_set.sections():
            a_d[option] = {}
            for k,v in self.common_set.items(option):
                if k == 'svn_password':
                    v = base64.decodestring(v)[:-2]
                a_d[option][k] = v
        return a_d

    def save_all_data(self, data):
        for k,v in data.items():
            self.new_common_set.add_section(k)
            for i,j in v.items():
                if i == 'svn_password':
                    random2 = ''.join(choice(ascii_uppercase) for x in range(2))
                    j = base64.encodestring(j + random2)
                self.new_common_set.set(k, i, j)
        with open(self.local_ini, 'wb') as configfile:
            self.new_common_set.write(configfile)



if __name__ == '__main__':
    home_auto_dir = '/data/Automation_test/ansible_release/'
    a = Global_Set()
    b = a.get_all_data()
    print b
    c = a.save_all_data(b)
