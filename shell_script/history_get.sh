#!/bin/sh
# Script para listar o histórico de determinado item

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

history_get()
{
    JSON='
    {
        "jsonrpc": "2.0",
        "method": "history.get",
        "params": {
            "itemids": [23668],
            "history": 0,
            "output": "extend",
            "time_from": "1438387200",
            "time_till": "1439250959"
        },
        "auth": "'$TOKEN'",
        "id": 1        
    }
    '
    curl -s -X POST -H "$HEADER" -d "$JSON" "$URL" | python -m json.tool
}

history_get
