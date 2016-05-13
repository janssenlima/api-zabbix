#!/bin/sh
# Script para cadastrar hosts associando grupos e templates 

URL='http://localhost/zabbix/api_jsonrpc.php'
HEADER='Content-Type:application/json'

USER='"Admin"'
PASS='"zabbix"'

autenticacao()
{
    JSON='
    {
        "jsonrpc": "2.0",
        "method": "user.login",
        "params": {
            "user": '$USER',
            "password": '$PASS'
        },
        "id": 0
    }
    '
    curl -s -X POST -H "$HEADER" -d "$JSON" "$URL" | cut -d '"' -f8
}
TOKEN=$(autenticacao)

criar_hosts()
{
    JSON='
    {
        "jsonrpc": "2.0",
        "method": "host.create",
        "params": [
            {
                "host": "Curso API para remover de novo 2",
                "status": 1,
                "interfaces": [
                    {
                        "type": 1,
                        "main": 1,
                        "useip": 1,
                        "ip": "192.168.0.5",
                        "dns": "",
                        "port": 10050
                    }
                ],
                "groups": [
                    {
                        "groupid": 2
                    },
                    {
                        "groupid": 7
                    }
                ],
                "templates": [
                    {
                        "templateid": 10001
                    },
                    {
                        "templateid": 10047
                    }
                ]
            },
            {
                "host": "Curso API para remover de novo 3",
                "status": 1,
                "interfaces": [
                    {
                        "type": 1,
                        "main": 1,
                        "useip": 1,
                        "ip": "192.168.0.5",
                        "dns": "",
                        "port": 10050
                    }
                ],
                "groups": [
                    {
                        "groupid": 2
                    },
                    {
                        "groupid": 7
                    }
                ],
                "templates": [
                    {
                        "templateid": 10001
                    },
                    {
                        "templateid": 10047
                    }
                ]
            }
        ],
       "auth": "'$TOKEN'",
        "id": 1
    }
    '
    curl -s -X POST -H "$HEADER" -d "$JSON" "$URL" > /dev/null
    echo "Hosts  criados"
}

criar_hosts