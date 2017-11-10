import hashlib
import json
import collections
import xml.etree.ElementTree as ElementTree
import requests
import random


class Bot:
    def __init__(self):
        self.config = {}

        self.load_config()

        self.unique_id = hashlib.md5(self.config['unique_id']).hexdigest().upper()
        self.campaign = self.config['campaign']
        self.computer_id = '{0}_W{1}.{2}'.format(self.config['pc_name'], 617600, self.unique_id)
        self.reg_str = '{0}/{1}/{2}/{3}/'.format('Windows 7 x86', self.config['build_id'],
                                                 self.config['ip_address'], self.unique_id)

    def load_config(self):
        try:
            config_file = open('config.json', 'r')
            config_json = json.load(config_file, object_pairs_hook=collections.OrderedDict)
            config_file.close()

        except (IOError, ValueError):
            config_json = dict()

        if 'config_id' not in config_json or type(config_json['config_id']) is not int:
            config_json['config_id'] = 0

        if 'campaign' not in config_json or type(config_json['campaign']) is not unicode:
            config_json['campaign'] = 'kas78'

        if 'unique_id' not in config_json or type(config_json['unique_id']) is not unicode:
            config_json['unique_id'] = self.random_str()

        if 'pc_name' not in config_json or type(config_json['pc_name']) is not unicode:
            config_json['pc_name'] = 'Admin-PC'

        if 'build_id' not in config_json or type(config_json['build_id']) is not int:
            config_json['build_id'] = 1031

        if 'ip_address' not in config_json or type(config_json['ip_address']) is not unicode:
            config_json['ip_address'] = self.get_ip_address()

        if 'registered' not in config_json or type(config_json['registered']) is not bool:
            config_json['registered'] = False

        if 'server_list' not in config_json or type(config_json['server_list']) is not dict:
            config_json['server_list'] = self.import_servers()

        self.config = config_json
        self.save_config()

        return True

    def save_config(self):
        config_file = open('config.json', 'w')
        json.dump(self.config, config_file, indent=5)
        config_file.close()

    def get_servers(self):
        if 'server_list' not in self.config.keys():
            return None

        return self.config['server_list']

    def merge_server_list(self, new_config):
        old_server_list = self.import_servers()
        new_server_list = []

        config_xml = ElementTree.fromstring(new_config)

        for server in config_xml.iter('srv'):
            new_server_list.append(server.text)
        count = 1
        for server in old_server_list:
            if server not in new_server_list:
                count += 1
                new_server_list.append(server)

        self.config['server_list'] = new_server_list

    @staticmethod
    def import_servers():
        help_msg = "servers.txt must contain a list of TrickBot C2 servers in format:\n" \
                   "<servs>\n" \
                   "<srv>ip:port</srv>\n" \
                   "<srv>ip:port</srv>\n" \
                   "</servs>\n"

        try:
            server_file = open('servers.txt', 'r')
            servers_xml = server_file.read()
            server_file.close()

            servers_xml = ElementTree.fromstring(servers_xml)

            server_list = []
            for server in servers_xml.iter('srv'):
                server_list.append(server.text)

            if len(server_list) == 0:
                raise RuntimeError(help_msg)

            return server_list

        except (IOError, ElementTree.ParseError, ValueError):
            raise RuntimeError(help_msg)

    @staticmethod
    def get_ip_address():
        ip = requests.get('https://api.ipify.org', verify=False, timeout=4)
        return ip.content

    @staticmethod
    def random_str():
        str_len = random.randrange(0, 17) + 16
        rand_str = ''

        for i in range(0, str_len):
            char = random.randrange(0, 62)

            if char >= 52:
                char -= 4
            elif char >= 26:
                char += 71
            else:
                char += 65

            rand_str += chr(char)

        return rand_str
