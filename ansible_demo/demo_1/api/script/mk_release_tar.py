#!/usr/bin/env  python
# -*- coding: utf-8 -*-
# use for git api

import sh
import re

class Git_Extra(object):

    def __init__(self, git_dir):
        self.git = sh.git.bake(_cwd=git_dir)

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
                mainbranch = self.now_branch()
                branchlist.insert(0, mainbranch)
            return branchlist
        else:
            return 'flag mush be -a -av -v'

    def check_out(self, branch):
        if branch not in self.searh_branch():
            return 'branch not exists, must be in   ' + ' '.join(self.searh_branch())
        else:
            self.git.checkout(branch)
            return 'now switch to branch ' + branch

    def pull(self):
        return self.git.pull()

    def status(self):
        return self.git.status()

if __name__ == '__main__':
    a = Git_Extra('/home/deploy/zhaoyong/')
    b = a.now_branch()
    print b
