#!/bin/sh
# Script para remover grupos hosts.

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

remover_grupo()
{
    JSON='
    {
        "jsonrpc": "2.0",
        "method": "hostgroup.create",
        "params": [
            23
        ],
        "auth": "'$TOKEN'",
        "id": 1        
    }
    '
     curl -s -X POST -H "$HEADER" -d "$JSON" "$URL" > /dev/null
}

remover_grupo