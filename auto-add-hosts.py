#!/usr/bin/env python
# -*- coding: utf-8 -*-

#author: Janssen dos Reis Lima - http://blog.conectsys.com.br

from zabbix_api import ZabbixAPI
import csv

zapi = ZabbixAPI(server="http://localhost/zabbix")
zapi.login("Admin", "zabbix")

f = csv.reader(open('/tmp/hosts.csv'), delimiter=';')
for [hostname,ip] in f:
    print "Cadastrando host da linha ", f.line_num
    hostcriado = zapi.host.create({
        "host": hostname,
        "status": 1,
        "interfaces": [
            {
                "type": 1,
                "main": 1,
                "useip": 1,
                "ip": ip,
                "dns": "",
                "port": 10050
            }
        ],
        "groups": [
            {
                "groupid": 2
            }
        ],
        "templates": [
            {
                "templateid": 10001
            }
        ]
    })
