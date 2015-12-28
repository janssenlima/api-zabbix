# Zabbix API

## Codes for use Zabbix API
  - ack_event_zabbix.py
  - itervices_zabbix.py
   
## Installation

You need lib zabbix-api and pip

```sh
# apt-get install pip git
# pip install zabbix-api

$ git clone https://github.com/janssenlima/api-zabbix
```

## How to use - examples

#### auto-add-hosts.py
>Change the file path in the code

>Structure hosts.csv file

```sh
hostautomatico1;192.168.0.1
hostautomatico2;192.168.0.2
hostautomatico3;192.168.0.3
hostautomatico4;192.168.0.4
hostautomatico5;192.168.0.5
.
.
.
hostautomatico100;192.168.0.100
```

>Just run

```sh
$ python auto-add-hosts.py
```

#### ack_event_zabbix.py
>Inform the Event ID generated in Zabbix as a parameter

```sh
$ python ack_event_zabbix.py <event.id>
```
#### itservices_zabbix.py
>Inform the function to be used

##### list groups
Syntaxy: get_hostgroups()

No parameter is required
```sh
$ python -c "execfile('itservices_zabbix.py'); get_hostgroups()"
```
##### list hosts of specific group
Syntax:  get_hosts('<name_of_group>')"
```sh
$ python -c "execfile('itservices_zabbix.py');  get_hosts('Linux servers')"
```
##### list items of a specific host that has associated trigger
Syntax:  get_items_hosts('<name_of_host>')"
```sh
$ python -c "execfile('itservices_zabbix.py');  get_hosts('Apache Web Server')"
```
##### delete full service tree
Syntax:  delete_tree_itservices()

No parameter is required
```sh
$ python -c "execfile('itservices_zabbix.py');  delete_tree_itservices()"
```
##### automatically create service tree
Syntax:  mk_populate()

No parameter is required
```sh
$ python -c "execfile('itservices_zabbix.py');  mk_populate()"
```

### Development

Want to contribute? Great!

Send suggestions, problems, errors etc for janssenreislima@gmail.com

Visit http://blog.conectsys.com.br

### Todos

 - Do not list groups without hosts
 - Create menu for selecting options and call the internal modules
 - And others

