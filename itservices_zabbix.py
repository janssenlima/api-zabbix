#!/usr/bin/python
# -*- coding: utf-8 -*-

# """
# Created on Tue Aug 11 22:36:58 2015

# @author: Janssen dos reis lima
# @email : janssenreislima@gmail.com 

# @contributor: Sansao Simonton
# @telegram: @sansaoipb
# """
import sys
from zabbix_api import ZabbixAPI
import click


@click.group()
def itservices():
    pass

SLA = "99.99"
zbx_server = "http://127.0.0.1:8080"
user = "Admin"
password = "zabbix"

# add the IP of your Zabbix Server
zapi = ZabbixAPI(server=zbx_server)

# add your access credentials
zapi.login(user, password)


def get_hostgroups(hostGroups='*'):
    hostgroups = zapi.hostgroup.get(
        {"output": "extend", "search": {"name": hostGroups}, "searchByAny": True, "searchWildcardsEnabled": True})
    listaGrupos = []
    for x in hostgroups:
        if 'template' not in str(x['name']).lower():
            listaGrupos += [x['name']]
    return listaGrupos

def get_hostgroups_id(grupo):
    try:
        groupId = zapi.hostgroup.get({"output": "extend", "filter": {"name": grupo}})[0]['groupid']
        return groupId
    except:
        print "Host group not found!!!"
        exit(0)


def get_hosts(grupo):
    hosts_grupo = zapi.host.get(
        {"groupids": get_hostgroups_id(grupo), "output": ["host", "name"], "filter": {"status": 0}})
    listaHosts = []
    for x in hosts_grupo:
        listaHosts += [x['name']]
    return listaHosts


def get_hostid(host):
    hostId = zapi.host.get({"output": "hostid", "filter": [{"name": host}]})[0]['hostid']
    return hostId


def get_triggers_hosts(host):
    triggers = zapi.trigger.get(
        {"hostids": get_hostid(host), "expandDescription": "true", "expandComment": "true", "expandExpression": "true"})
    for x in triggers:
        print (x['description'])


def get_items_hosts(host):
    items = zapi.item.get({"hostids": get_hostid(host), "with_triggers": True, "selectTriggers": "extend"})
    listaItems = []
    for x in items:
        print (x['name'])
        listaItems += [x['name']]
    return listaItems


def get_item_triggerid(host, item):
    triggerId = zapi.item.get(
        {"output": "triggers", "hostids": get_hostid(host), "with_triggers": True,
         "selectTriggers": "triggers", "filter": {"name": item}})[0]['triggers'][0]['triggerid']
    return triggerId


def mk_father_itservices(grupo):
    teste = get_itservices_raiz(grupo)
    if teste != []:
        pass
    else:
        if get_hosts(grupo) != []:
            zapi.service.create({"name": grupo, "algorithm": "1", "showsla": "1", "goodsla": SLA, "sortorder": "1"})


def get_itservice_pid(grupo):
    parentId = zapi.service.get(
        {"selectParent": "extend", "selectTrigger": "extend", "expandExpression": "true",
         "filter": {"name": grupo}})[0]['serviceid']
    return parentId


def mk_child_itservices(host, grupo):
    zapi.service.create({"name": host, "algorithm": "1", "showsla": "1", "goodsla": SLA, "sortorder": "1",
                         "parentid": get_itservice_pid(grupo)})


def get_itservice_pid_child(host):
    parentIdChild = zapi.service.get(
        {"selectParent": "extend", "selectTrigger": "extend", "expandExpression": "true",
         "filter": {"name": host}})[0]['serviceid']
    return parentIdChild


def mk_child_itservices_trigger(host, item):
    zapi.service.create({"name": item, "algorithm": "1", "showsla": "1", "goodsla": SLA, "sortorder": "1",
                         "parentid": get_itservice_pid_child(host), "triggerid": get_item_triggerid(host, item)})


def get_itservices(hostGroups):
    hostgroups = ["{0}".format(hostsW).rstrip().strip() for hostsW in hostGroups.split(",")]
    itServices = zapi.service.get({"selectParent": ["serviceid", "name"],
                                   "selectDependencies": ["serviceid", "servicedownid", "serviceupid", "linkid"],
                                   "output": ["serviceid", "name"]})
    
    listaServicos = []
    hosts = []
    text = ""
    try:
        for host in hostgroups:
            if "*" != host:
                hosts += [host.upper()]
                for x in itServices:
                    if host.lower() in str(x['name']).lower():
                        listaServicos += [x['serviceid']]
                    
                    for i in x['dependencies']:
                        if i['serviceupid'] in listaServicos:
                            listaServicos += [i['serviceid']]
            else:
                text += "\nTodos os grupos excluidos pelo uso do \"*\""
                for x in itServices:
                    listaServicos += [x['serviceid']]
        
        if [] != hosts:
            if len(hosts) == 2:
                text += "\nGrupos excluidos: {0}".format(' e '.join(hosts))
            
            elif len(hosts) > 2:
                ultimoNome = hosts[-1:]
                todosAntes = hosts[:-1]
                text += "\nGrupos excluidos: {0} e {1}".format(', '.join(todosAntes), ultimoNome[0])
            else:
                text += "\nGrupo excluido: {0}".format(hosts[0])
    
    except Exception as msg:
        print (msg)
    return listaServicos, text


def get_itservices_raiz(hostGroups):
    hostgroups = ["{0}".format(hostsW).rstrip().strip() for hostsW in hostGroups.split(",")]
    itServices = zapi.service.get({"output": ["serviceid", "name"]})
    
    listaRaiz = []
    try:
        for host in hostgroups:
            if "*" != host:
                for x in itServices:
                    if host in str(x['name']) and host not in listaRaiz:
                        listaRaiz += [host]
    
    except Exception as msg:
        print (msg)
    return listaRaiz


@itservices.command()
@click.option('--hostgroup', help='Exclui toda a arvore de servicos caso nao seja passado nenhum hostgroup como argumento.', default='*', type=str)
def delete_itservices(hostgroup):
    try:
        ids, result = get_itservices(hostgroup)
        print (result)
        zapi.service.deletedependencies(ids)
        zapi.service.delete(ids)
    except Exception as msg:
        print (msg)


@itservices.command()
@click.option('--hostgroup', help='Cria toda a arvore de servicos por default. Aceita passar hostgroups separados por virgula..', default='*', type=str)
def make_itservices(hostgroup):
    hostgroups = ["{0}".format(hostsW).rstrip().strip() for hostsW in hostgroup.split(",")]
    for nomeGrupo in get_hostgroups(hostgroups):
        mk_father_itservices(nomeGrupo)
        for nomeHost in get_hosts(nomeGrupo):
            print ("\n{0} ({1})\n".format(nomeGrupo, nomeHost))
            mk_child_itservices(nomeHost, nomeGrupo)
            for nomeItem in get_items_hosts(nomeHost):
                mk_child_itservices_trigger(nomeHost, nomeItem)


if __name__ == '__main__':
    itservices()
