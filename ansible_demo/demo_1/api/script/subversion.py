#!/usr/bin/python
# -*- coding: utf-8 -*-

# svn api

EXAMPLES = '''
# Checkout subversion repository to specified folder.
- subversion: repo=svn+ssh://an.example.org/path/to/repo dest=/src/checkout
'''

import re
import tempfile
import commands
import xmltodict
import json
import ConfigParser
import sys
import os

reload(sys)
sys.setdefaultencoding('utf-8')

home_auto_dir = os.path.abspath('.') + '/'

class Subversion(object):
    def __init__(
            self, dest, repo, revision='HEAD', username=None, password=None, svn_path='not'):
        self.common_set = ConfigParser.RawConfigParser(allow_no_value=True)
        self.common_set.read(home_auto_dir + 'local_settings.ini')
        self.svn_dir = self.common_set.get('svn', 'svn_dir')
        self.dest = dest
        self.repo = repo
        self.revision = revision
        self.username = username
        self.password = password
        # self.svn_path = svn_path

    def _exec(self, args):
        bits = 'svn revert -R %s;svn cleanup -R %s;svn --non-interactive --trust-server-cert --no-auth-cache --depth infinity '%(self.dest, self.dest)
        if self.username:
            bits += '--username %s' % self.username
        if self.password:
            bits += ' --password %s' % self.password
        bits += " " + args
        print bits
        (status, output) = commands.getstatusoutput(bits)
        return {'status': status, 'output': output}

    def checkout(self, log_file):
        '''Creates new svn working directory if it does not already exist.'''
        print 'checkout'
        return self._exec("checkout -r %s %s %s| tee -a %s" % (self.revision, self.repo, self.dest, log_file))

    def switch(self):
        '''Change working directory's repo.'''
        # switch to ensure we are pointing at correct repo.
        return self._exec("switch '%s' '%s'" % (self.repo, self.dest))

    def update(self, log_file):
        '''Update existing svn working directory.'''
        return self._exec("update -r %s '%s' | tee -a %s" % (self.revision, self.dest, log_file))

    def get_version_info(self, num=20):
        out = self._exec("log -v '%s' -q --limit %s --xml" % (self.dest, num))
        o = xmltodict.parse(out['output'])
        x = json.dumps(o)
        tags = json.loads(x)['log']['logentry']
        return tags

    def get_last_version(self):
        self._exec("info -r HEAD|grep Revision: |cut -c11-")

    def revert(self):
        '''Revert svn working directory.'''
        self._exec("revert -R '%s'" % self.dest)

    def get_revision(self, log_file=''):
        '''Revision and URL of subversion working directory.'''
        if not log_file:
            text = self._exec("info -r HEAD '%s'" % self.dest)['output']
        else:
            text = self._exec("info -r %s '%s'|tee -a %s" % (self.revision, self.dest, log_file))['output']
        all_kv = {}
        for i in text.split('\n'):
            kv = i.split(": ")
            try:
                key = kv[0].replace(' ','_')
                value = kv[1]
                all_kv[key] = value
            except:
                pass
        return all_kv

    def needs_update(self):
        rev1 = self.get_revision()['Revision']
        rev2 = self.get_revision(head=True)['Revision']
        if rev1 < rev2:
            change = True
        return {'now_rev': rev1, 'head_rev':rev2, 'need_update': change}

    def status(self):
        return self._exec("status -v %s" % (self.dest))

    def modify_info(self, now_version, commit_version):
        return self._exec("info -v -r %s:%s" % (now_version, commit_version))

    def status_total(self):
        output = self._exec("status %s" % (self.dest))['output']
        return output
        #if not output:
        #    return {'status': '正常'}
        #if output == 'M':
        #    return {'status': '内容被修改'}
        #if output == 'C':
        #    return {'status': '发生冲突'}
        #if output == 'A':
        #    return {'status': '预定加入到版本库'}
        #if output == '?':
        #    return {'status': '不在svn的控制中'}
        #if output == 'K':
        #    return {'status': '被锁定'}
        #else:
        #    return {'status': '未知错误'}

if __name__ == '__main__':
    a = Subversion(dest='/hudson_workspace/use-for-test/', repo='http://10.8.12.100/svn/jumbo/unicomplatform/trunk/', username='hudson', revision=193274, password='h7d8S3')
    print a.update()
    print a.get_revision()
    #print a.checkout(294823)
    #print a.needs_update()
    print a.status_total()


