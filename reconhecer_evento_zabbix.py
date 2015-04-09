Created on Thu Apr 09 18:37:18 2015

@author: Janssen dos Reis Lima
"""

from zabbix_api import ZabbixAPI
import sys

zabbix_server = "http://myserverzabbix/zabbix"
username = "user"
password = "********"

conexao = ZabbixAPI(server = zabbix_server)
conexao.login(username, password)

conexao.event.acknowledge({"eventids": sys.argv[1], "message": "Problema resolvido"})
