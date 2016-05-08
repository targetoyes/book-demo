#!/usr/bin/env  python
# -*- coding: utf-8 -*-

import json
import ConfigParser

class KconfigParser(ConfigParser.RawConfigParser):
    def write(self, fp):
        """Write an .ini-format representation of the configuration state."""
        if self._defaults:
            fp.write("[%s]\n" % DEFAULTSECT)
            for (key, value) in self._defaults.items():
                fp.write("%s : %s\n" % (key, str(value).replace('\n', '\n\t')))
            fp.write("\n")
        for section in self._sections:
            fp.write("[%s]\n" % section)
            for (key, value) in self._sections[section].items():
                if key != "__name__":
                    fp.write("%s : %s\n" %
                             (key, str(value).replace('\n', '\n\t')))
            fp.write("\n")

class Generate_ansible_hosts(object):
    def __init__(self, host_file):
        self.new_config = KconfigParser(allow_no_value=True)
        self.old_config = KconfigParser(allow_no_value=True)
        self.host_file = host_file

    def create_all_servers(self, items):
        for i in items:
            group = i['group']
            self.new_config.add_section(group)
            for j in i['items']:
                name = j['name']
                ssh_port = j['ssh_port']
                ssh_host = j['ssh_host']
                ssh_user = j['ssh_user']
                build = "ansible_ssh_port={0} ansible_ssh_host={1} ansible_ssh_user={2}".format(
                        ssh_port, ssh_host, ssh_user)
                self.new_config.set(group, name, build)
        with open(self.host_file, 'wb') as configfile:
            self.new_config.write(configfile)
        return True

    def add_one_server(self, item):
        self.old_config.read(self.host_file)
        group_list = [i for i in self.old_config.sections()]
        if item['group'] not in group_list:
            self.old_config.add_section(item['group'])
        build = "ansible_ssh_port={0} ansible_ssh_host={1} ansible_ssh_user={2}".format(
                 item['ssh_port'], item['ssh_host'], item['ssh_user'])
        self.old_config.set(item['group'], item['name'], build)
        with open(self.host_file, 'wb') as configfile:
            self.old_config.write(configfile)
        return True

    def delete_one_server(self, item):
        self.old_config.read(self.host_file)
        group_list = [i for i in self.old_config.sections()]
        if item['group'] not in group_list:
            return False
        else:
            self.old_config.remove_option(item['group'], item['name'])
            if not self.old_config.items(item['group']):
                self.old_config.remove_section(item['group'])
            with open(self.host_file, 'wb') as configfile:
                self.old_config.write(configfile)
        return True

    def update_one_server(self, old_item, new_item):
        self.delete_one_server(old_item)
        self.add_one_server(new_item)


if __name__ == '__main__':
    host_file = 'hosts.cfg'
    all_servers = [
        {"group": "test1",
        "items": [{"name": "test_test1",
                   "ssh_port": "22",
                   "ssh_host": "10.8.17.27",
                   "ssh_user": "deploy",
                   "type": "server"
                  },
                  {"name": "test_test2",
                   "ssh_port": "22",
                   "ssh_host": "10.8.17.27",
                   "ssh_user": "deploy",
                   "type": "server"
                  }]
        },
        {"group": "test2",
        "items": [{"name": "test_test3",
                   "ssh_port": "22",
                   "ssh_host": "10.8.17.27",
                   "ssh_user": "deploy",
                   "type": "server"
                  },
                  {"name": "test_test4",
                   "ssh_port": "22",
                   "ssh_host": "10.8.17.27",
                   "ssh_user": "deploy",
                   "type": "server"
                  }]
        },
        {"group": "test3",
        "items": [{"name": "test_test5",
                   "ssh_port": "22",
                   "ssh_host": "10.8.17.27",
                   "ssh_user": "deploy",
                   "type": "server"
                  }]
        }
    ]

    add_one = {"group": "test3",
               "name": "test_test5",
               "ssh_port": "22",
                "ssh_host": "10.8.17.27",
                "ssh_user": "deploy"
              }

    update_one = {"group": "test3",
               "name": "test_test5",
               "ssh_port": "2223",
                "ssh_host": "10.8.17.27",
                "ssh_user": "deploy"
              }

    x = Generate_ansible_hosts(host_file)
    x.create_all_servers(all_servers)
    x.add_one_server(add_one)
    x.update_one_server(add_one, update_one)
    x.delete_one_server(add_one)
