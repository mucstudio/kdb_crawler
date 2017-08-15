# encoding=utf-8

import os
from util import config_parser


class ConfigHelper:
    @staticmethod
    def get_server_port():
        return config_parser.ConfigHandler('config.cfg',
                                           'info').fread('dip_svc_port')

    @staticmethod
    def get_dip_ip_port():
        c = config_parser.ConfigHandler('config.cfg', 'dip')
        ip = c.fread('dip_ip')
        port = c.fread('dip_port')
        return '{}:{}'.format(ip, port)

    @staticmethod
    def get_mysql_conn_info():
        conn = {'ip': '127.0.0.1',
                'port': '3306',
                'user': 'kdb',
                'passwd': 'kdb',
                'db': 'kdb',
                'sock': 'kdb'
                }
        key_list = ['ip', 'port', 'user', 'passwd', 'db', 'sock']
        for key in key_list:
            v = config_parser.ConfigHandler('config.cfg', 'mysql').fread(key)
            conn[key] = v if v else conn[key]

        return conn

    @staticmethod
    def get_dip_home():
        return os.environ.get('DIP_HOME')
