#!/usr/bin/env  python
# -*- coding: utf-8 -*-
import ansible.runner
import ansible.playbook
import ansible.inventory
from ansible import callbacks
from ansible import utils
import re

class Ansi_Play(object):

    def __init__(self, playbook, extra_vars={}):
        self.stats = callbacks.AggregateStats()
        self.playbook_cb = callbacks.PlaybookCallbacks(verbose=utils.VERBOSITY)
        self.extra_vars = extra_vars
        self.playbook = playbook
        self.setbook = self.book_set()

    def book_set(self):
        runner_cb = callbacks.PlaybookRunnerCallbacks(self.stats, verbose=utils.VERBOSITY)
        self.pb = ansible.playbook.PlayBook(
            playbook = self.playbook,
            stats = self.stats,
            extra_vars = self.extra_vars,
            callbacks = self.playbook_cb,
            runner_callbacks = runner_cb
        )

    def ansi_escape(self, text):
        ansi_escape = re.compile(r'\x1b[^m]*m')
        return ansi_escape.sub('', text)

    def run(self):
        simple_std = self.pb.run()
        # complex_std = callbacks.log_add
        complex_std = self.ansi_escape('\n'.join(callbacks.log_add))
        error_std = self.ansi_escape('\n'.join(callbacks.error_add))
        callbacks.log_add = []
        callbacks.error_add = []
        # complex_std = complex_std.replace('\n','\\n')
        return [simple_std, complex_std, error_std]
        # return simple_std

if __name__ == "__main__":
    excute = Ansi_Play('test.yml',{'test': '/tmp/test.book'})
    excute.run()
