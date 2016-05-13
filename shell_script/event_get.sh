#!/bin/sh
# Script para listar eventos por orden decrescente

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

event_get()
{
    JSON='
    {
        "jsonrpc": "2.0",
        "method": "event.get",
        "params": {
                    "output": "extend",
                    "time_from": "1438387200",
                    "time_till": "1439250959",
                    "sortfield": ["clock", "eventid"],
                    "sortorder": "desc"
        },
        "auth": "'$TOKEN'",
        "id": 1        
    }
    '
    curl -s -X POST -H "$HEADER" -d "$JSON" "$URL" | python -m json.tool
}

event_get
