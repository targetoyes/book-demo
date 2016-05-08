#!/usr/bin/env  python
# -*- coding: utf-8 -*-
# use for git api

import re
import commands
import sys
import ConfigParser
from multiprocessing.dummy import Pool as ThreadPool
import os

reload(sys)
sys.setdefaultencoding('utf-8')

home_auto_dir = os.path.abspath('.') + '/'

class Maven_Extra(object):

    def __init__(self, root_dir):
        self.common_set = ConfigParser.RawConfigParser(allow_no_value=True)
        self.common_set.read(home_auto_dir + 'local_settings.ini')
        self.maven_dir = self.common_set.get('build', 'maven_dir')
        self.ant_dir = self.common_set.get('build', 'ant_dir')
        self.root_dir = root_dir

    def start_exec(self, args, jdk_mode='java-6-openjdk-amd64', pom_file='', logfile='', plat_form='maven'):
        os.chdir(self.root_dir)
        if plat_form == 'maven':
            bits = 'JAVA_HOME=/usr/lib/jvm/' + jdk_mode + ' ' + self.maven_dir + 'mvn ' + args
            bits += ' -f ' + pom_file  + ' '
        elif plat_form == 'ant':
            bits = 'JAVA_HOME=/usr/lib/jvm/' + jdk_mode + ' ' + self.ant_dir + ' ' + args
            bits += ' -file ' + pom_file  + ' '
        print bits
        if logfile:
            bits += '|tee -a ' + logfile
        (status, output) = commands.getstatusoutput(bits)
        if output:
            flag = find_error(output)
            return flag
        else:
            analyze_clu = maven_log(logfile)
        os.chdir(home_auto_dir)
        return {'status': status, 'analyze_clu': analyze_clu}

def find_error(log_text):
    flag = 'success'
    for i in ['BUILD FAILURE', 'Finished: FAILURE']:
        build_fail = log_text.find(i)
        if build_fail != -1:
            flag = 'fail'
            break
    error_time = log_text.count('ERROR')
    fake_error = log_text.count('does not exist')
    if error_time - fake_error >= 6:
        flag = 'fail'
    print flag
    return flag

def maven_log(logfile):
    with open(logfile, 'r') as f:
        all_log = f.read()
    return maven_analyze(all_log)

def simple_maven_log(logfile):
    error_log = []
    with open(logfile, 'r') as f:
        all_log = f.read()
        try:
            error_log = '\n'.join([i for i in all_log.split('\n')
                        if re.search('\[ERROR\]', i)])
        except:
            error_log = ''
    return {'all_log': all_log, 'error_log': error_log}

def maven_analyze(log_text):
    simple_log = []
    log_conclusion = {}
    log_conclusion['item'] = []
    error_log = []
    flag = False
    item = ''
    build_result = 'failed'
    cost_time = 'N/A'
    item_status = re.compile('\[INFO\]\s+(\w+-\w+)\s+\.+\s+(\w+)\s+\[(.*)\]')
    build_pat = re.compile('\[INFO\] BUILD (.*)')
    cost_pat = re.compile('\[INFO\] Total time: (.*)')
    for i in log_text.split('\n'):
        if re.search('\[ERROR\]', i):
            error_log.append(i)
        if re.search('Reactor Summary', i):
            flag = True
        if re.search(build_pat, i):
            flag = True
        if flag:
            simple_log.append(i)
            item = re.search(item_status, i)
            build_flag = re.search(build_pat, i)
            cost_flag = re.search(cost_pat, i)
            if item:
                item_name = item.group(1)
                item_result = item.group(2)
                item_time = item.group(3).strip()
                log_conclusion['item'].append({'name': item_name,
                                               'flag': item_result,
                                               'cost_time': item_time
                                               })
            if build_flag:
                build_result = build_flag.group(1)
                log_conclusion['total_flag'] = build_result
            if cost_flag:
                cost_time = cost_flag.group(1)
                log_conclusion['total_time'] = cost_time
    simple_text = '\n'.join(simple_log)
    error_text = '\n'.join(error_log)
    #print simple_text
    #print log_conclusion
    if not item:
        log_conclusion['item'].append({'name': '',
                                       'flag': build_result,
                                       'cost_time': cost_time
                                        })
        simple_text = 'some errors happens'
    if not simple_text:
        raise Exception('maven日志匹配时发生错误')
    if error_text:
        print 'error_text'
        return {'simple_log': simple_text, 'json_log': log_conclusion, 'error_log': error_text}
    #return {'complex_log': log_text, 'simple_log': simple_text, 'json_log': log_conclusion}
    return {'simple_log': simple_text, 'json_log': log_conclusion}



        #return ansi_escape.sub('', text)

if __name__ == '__main__':
    a = Maven_Extra('/hudson_workspace/test1/')
    #a.start_exec('clean')
    #a.start_exec('install','/temp/aa.log')
    #a.start_exec(['clean', 'install'])
    print maven_log('/temp/aa.log')
