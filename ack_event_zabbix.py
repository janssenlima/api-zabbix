# -*- coding: utf-8 -*-
"""
Created on Thu Apr 09 18:37:18 2015

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

zapi.event.acknowledge({"eventids": sys.argv[1], "message": "Checking the problem."})
