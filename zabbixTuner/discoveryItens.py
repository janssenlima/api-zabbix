# -*- coding: utf-8 -*-
# @author: Janssen dos Reis Lima
# Este codigo verifica a quantidade total de itens descobertos (LLD) no ambiente

from zabbix_api import ZabbixAPI

zapi = ZabbixAPI(server="http://localhost/zabbix",timeout=1000)
login = zapi.login("Admin","zabbix")
itemDisc = zapi.item.get({
    "output": "extend",
    "selectItemDiscovery": [
        "itemid"
    ],
    "selectTriggers": ["description"]
})

cont = 0
for i in itemDisc:
    if i["itemDiscovery"]:
        cont += 1
print "Quantidade de itens descobertos no ambiente: ", cont
