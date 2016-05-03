# -*- coding: utf-8 -*-
# Desenvolvido por Janssen dos Reis Lima - janssenreislima@gmail.com
# Relatório de eventos
# Não está finalizado. Caso queira utilizar, alterar o código do grupo de host e o timestamp inicial e final

from zabbix_api import ZabbixAPI

import time

zapi = ZabbixAPI(server="http://localhost/zabbix")

zapi.login("user", "password")

 
eventos = zapi.event.get ({
        "output": "extend",
        "selectHosts": ["hostid", "host"],    
        "groupids": "21",        
        "selectRelatedObject": ["description", "lastchange"],
        "time_from": "1459468800",
        "time_till": "1462060800",
        "sortfield": "eventid",
        "sortorder": "DESC"
})

 
print '{0:20} | {1:15} | {2:72} | {3:10} | {4}'.format("Data", "Nome do host", "Descrição do evento", "Status", "Duração")
print ""
for i in eventos:
 
        nomeHost = i["hosts"][0]["host"]

        dataEvento = time.strftime("%d-%m-%Y %H:%M:%S",time.localtime(float(i["clock"])))

        if i["value"] == "0":
            duracao = time.time() - float(i["relatedObject"]["lastchange"])
            statusEvento = "OK"
        else:
            duracao = float(i["relatedObject"]["lastchange"]) - float(i["clock"])
            statusEvento = "INCIDENTE"

        triggers = zapi.trigger.get ({            
                                    "triggerids": i["relatedObject"]["triggerid"],
                                    "output": ["description"],
                                    "expandDescription": True
                                    })

        pegadia = "{0.tm_yday}".format(time.gmtime(duracao))
        dia = int(pegadia) - 1
        horaMinuto = "d {0.tm_hour}h {0.tm_min}m {0.tm_sec}s".format(time.gmtime(duracao))
        duracaoEvento = str(dia)+str(horaMinuto)
        
        print '{0:20} | {1:15} | {2:70} | {3:10} | {4}'.format(dataEvento, nomeHost, triggers[0]["description"], statusEvento, duracaoEvento)