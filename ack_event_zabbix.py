# -*- coding: utf-8 -*-
"""
Updated on Thu Jul 16 10:31:20 2020

@author: Janssen dos Reis Lima

how to use: python ack_event_zabbix.py <event.id>
"""

from zabbix_api import ZabbixAPI
import sys

zabbix_server = "http://<your_server>/zabbix"
username = "user"
password = "pass"

zapi = ZabbixAPI(server = zabbix_server)
zapi.login(username, password)

zapi.event.acknowledge({"eventids": sys.argv[1], "action": 6 , "message": "Checking the problem."})
