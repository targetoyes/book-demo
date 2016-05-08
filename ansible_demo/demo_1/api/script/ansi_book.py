#!/usr/bin/env  python
# -*- coding: utf-8 -*-
import commands
import json

class Ansi_Play(object):

    def __init__(self, playbook):
        self.playbook = playbook

    def _exec(self, args):
        bits = "ansible-playbook %s " %(self.playbook)
        bits += args
        print bits
        (status, output) = commands.getstatusoutput(bits)
        return {'status': status, 'output': output}

    def run(self, log_file):
        res = self._exec('|tee -a %s' %(log_file))
        flag = self.analyze_log(res['output'])
        res['all_flag'] = flag
        return res

    def run_vars(self, extra_vars, log_file=''):
        var = json.dumps(extra_vars)
        flag = True
        if log_file:
            res = self._exec("--extra-vars '%s'|tee -a %s" %(var, log_file))
            if res['output'].find('no hosts matched') != -1:
                flag = True
            else:
                clu_line = [i for i in res['output'].split('\n') if "unreachable" in i]
                for i in clu_line:
                    flag = self.analyze_log(i)
                    if flag == False:
                        break
        else:
            res = self._exec("--extra-vars '%s'" %(var))
            if res['output'].find('no hosts matched') != -1 or res['status'] == 1:
                flag = False
            else:
                clu_line = [i for i in res['output'].split('\n') if "unreachable" in i]
                for i in clu_line:
                    flag = self.analyze_log(i)
                    if flag == False:
                        break
        res['flag'] = flag
        return res

    def analyze_log(self, output):
        if output.find('ERROR: Invalid control') != -1:
            return False
        str1 = ' '.join(output.split(':')[1].strip().replace('=','":').split()).replace(' ',',"')
        str_dict = '{"' + str1 + '}'
        clu_dict = json.loads(str_dict)
        if clu_dict['unreachable'] == 0 and clu_dict['failed'] == 0:
            return True
        else:
            return False

if __name__ == "__main__":
    excute = Ansi_Play('/data/Automation/ansible_file/test_go.yml')
    excute.run_vars({"test": "test",'fsds':''}, '/temp/ansible_play.log')
