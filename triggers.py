# -*- coding: utf-8 -*-
# Desenvolvido por Janssen dos Reis Lima

from zabbix_api import ZabbixAPI
import time
from conf.vars import *

zapi = ZabbixAPI(server=ZBX_SERVER)
zapi.login(ZBX_USER, ZBX_PASS)

triggers = zapi.trigger.get ({
            "output": ["description", "lastchange"], 
            "selectHosts": ["hostid", "host"], 
            "selectLastEvent": ["eventid", "acknowledged", "objectid", "clock", "ns"], 
            "sortfield" : "lastchange", 
            "monitored": "true", 
            "only_true": "true", 
            "maintenance":  "false", 
            "expandDescription": True,
            "filter":{"value":1}
            })
print "Host - Descricao - Última alteração - Idade"
print "==========================================="
for y in triggers:
    nome_host = y["hosts"][0]["host"]
    
    idade = time.time() - float(y["lastchange"])
    pegadia = "{0.tm_yday}".format(time.gmtime(idade))
    dia = int(pegadia) - 1
    duracao = "dias {0.tm_hour} horas {0.tm_min} minutos".format(time.gmtime(idade))
    ultima_alteracao = time.strftime("%d/%m/%Y %H:%M:%S", time.localtime(float(y["lastchange"])))
    print nome_host, "- ", y["description"], "- ", ultima_alteracao, "- ", dia, duracao
    print ""
    #print "---------------------------------------"
