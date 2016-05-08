#!/usr/bin/env  python
# -*- coding: utf-8 -*-
import ansible.runner

runner = ansible.runner.Runner(
   module_name='ping',
   module_args='',
   pattern='web*',
   forks=10
)
datastructure = runner.run()

if __name__ == "__main__":
    excute = Ansi_Play('test.yml',{'test': '/tmp/test.book'})
    excute.run()
