# -*- coding: utf-8 -*-
#"""
#Created on Tue Aug 11 22:36:58 2015

#@author: Janssen dos reis lima 
#@email : janssenreislima@gmail.com / janssen@conectsys.com.br
#@web   : conectsys.com.br / blog.conectsys.com.br

#Credits:  Luis Sales, who had the original idea and started the project using Shell Script.
#http://redhate.me
#luiz@lsales.biz

#"""

from zabbix_api import ZabbixAPI

# add the IP of your Zabbix Server
zapi = ZabbixAPI(server="http://<ip_of_server>/zabbix")
# add your access credentials
zapi.login("<user>", "<password>")

def get_hostgroups():
    hostgroups = zapi.hostgroup.get({"output": "extend"})
    listaGrupos = []
    for x in hostgroups:
        print x['name']
        listaGrupos += [x['name']]
    return listaGrupos

def get_hostgroups_id(grupo):
    groupId = zapi.hostgroup.get({"output": "extend","filter":{"name":grupo}})[0]['groupid']
    return groupId

def get_hosts(grupo):
    hosts_grupo = zapi.host.get({"groupids":get_hostgroups_id(grupo),"output":["host"]})
    listaHosts = []
    for x in hosts_grupo:
        print x['host']
        listaHosts += [x['host']]
    return listaHosts

def get_hostid(host):
    hostId = zapi.host.get({"output":"hostid","filter":{"host":host}})[0]['hostid']
    return hostId

def get_triggers_hosts(host):
    triggers = zapi.trigger.get({"hostids":get_hostid(host),"expandDescription":"true","expandComment":"true","expandExpression":"true"})
    for x in triggers:
        print x['description']

def get_items_hosts(host):
    items = zapi.item.get({"hostids":get_hostid(host),"with_triggers":True,"selectTriggers":"extend"})
    listaItems = []
    for x in items:
        print x['name']
        listaItems += [x['name']]
    return listaItems

def get_item_triggerid(host,item):
    triggerId = zapi.item.get({"output":"triggers","hostids":get_hostid(host),"with_triggers":True,"selectTriggers":"triggers","filter":{"name":item}})[0]['triggers'][0]['triggerid']
    return triggerId

def mk_father_itservices(grupo):
    zapi.service.create({"name":grupo,"algorithm":"1","showsla":"1","goodsla":"99.99","sortorder":"1"})

def get_itservice_pid(grupo):
    parentId = zapi.service.get({"selectParent":"extend","selectTrigger":"extend","expandExpression":"true","filter":{"name":grupo}})[0]['serviceid']
    return parentId

def mk_child_itservices(host,grupo):
    zapi.service.create({"name":host,"algorithm":"1","showsla":"1","goodsla":"99.99","sortorder":"1","parentid":get_itservice_pid(grupo)})

def get_itservice_pid_child(host):
    parentIdChild = zapi.service.get({"selectParent":"extend","selectTrigger":"extend","expandExpression":"true","filter":{"name":host}})[0]['serviceid']
    return parentIdChild

def mk_child_itservices_trigger(host,item):
    zapi.service.create({"name":item,"algorithm":"1","showsla":"1","goodsla":"99.99","sortorder":"1","parentid":get_itservice_pid_child(host),"triggerid":get_item_triggerid(host,item)})

def get_itservices():
    itServices = zapi.service.get({"selectParent":"extend","selectTrigger":"extend"})
    listaServicos = []
    for x in itServices:
        listaServicos += [x['serviceid']]
    return listaServicos

def delete_tree_itservies():
    for x in get_itservices():
        zapi.service.deletedependencies([x])
        zapi.service.delete([x])

def mk_populate():
    delete_tree_itservies()
    for nomeGrupo in get_hostgroups():
        mk_father_itservices(nomeGrupo)
        for nomeHost in get_hosts(nomeGrupo):
            mk_child_itservices(nomeHost, nomeGrupo)
            for nomeItem in get_items_hosts(nomeHost):
                mk_child_itservices_trigger(nomeHost, nomeItem)
