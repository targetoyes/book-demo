#!/usr/bin/env  python
# -*- coding: utf-8 -*-
# use for git api

import sh
import re
import commands
import os
import sys

reload(sys)
sys.setdefaultencoding('utf-8')

home_auto_dir = os.path.abspath('.') + '/'

class Git_Extra(object):

    def __init__(self, git_dir):
        self.common_set = ConfigParser.RawConfigParser(allow_no_value=True)
        self.common_set.read(home_auto_dir + 'local_settings.ini')
        self.git_com_dir = self.common_set.get('svn', 'git_dir')
        self.git_dir = git_dir
        self.git = sh.git.bake(_cwd=git_dir)

    def _exec(self, args):
        bits = "cd {0};git clean -fd;{1} ".format(self.git_dir, self.git_com_dir)
        bits += " " + args
        print bits
        (status, output) = commands.getstatusoutput(bits)
        return {'status': status, 'output': output}

    def ansi_escape(self, text):
        ansi_escape = re.compile(r'\x1b[^m]*m')
        return ansi_escape.sub('', text)

    def now_branch(self):
        branch = self.ansi_escape(str(self.git.branch()))
        now = [i for i in branch.split('\n') if i.startswith('*')][0].split()[1]
        return now

    def search_branch(self, flag='-a', tidy='t'):
        if flag in ['-a', '-v', '-av']:
            text = str(self.git.branch(flag))
            branch = self.ansi_escape(text)
            branchlist = [i.strip() for i in branch.split('\n') if i != '']
            if flag == '-a' and tidy == 't':
                branchlist = [i.strip().split()[0] for i in branch.split('\n') if i != '' and not i.startswith('*')]
            return branchlist
        else:
            return 'flag mush be -a -av -v'

    def check_out(self, branch, log_file):
        if branch not in [i.split('/')[-1] for i in self.search_branch()]:
            x = 'branch not exists, must be in   ' + ' '.join(self.search_branch())
            commands.getstatusoutput('echo %s |tee -a %s'% (x, log_file))
        else:
            self.git.checkout(branch)
            x = 'now switch to ' + branch
            commands.getstatusoutput('echo %s |tee -a %s'% (x, log_file))
        return x

    def get_last_version(self, branch):
        return self._exec("rev-parse {0}".format(branch))

    def pull(self, log_file):
        return self._exec("pull|tee -a {0}".format(log_file))

    def status(self, log_file):
        return self._exec("status|tee -a {0}".format(log_file))

    def clone(self, git_url, log_file):
        return self._exec("clone {0} {1}|tee -a {2}".format(git_url, self.git_dir, log_file))

    def reset(self, version, log_file):
        return self._exec("reset --hard {0}|tee -a {1}".format(version, log_file))

if __name__ == '__main__':
    a = Git_Extra('/temp/bb') #, "git@git.baozun.cn:jie.gan/ansible_release.git")
    b = a.pull('/temp/aa.log')
    print b
