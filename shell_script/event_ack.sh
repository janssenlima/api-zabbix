#!/bin/sh
# Script para adicionar dependencia de trigger

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

event_ack()
{
    JSON='
    {
        "jsonrpc": "2.0",
        "method": "event.acknowledge",
        "params": {
            "eventids": "4248",
            "message": "Evento do curso reconhecido."
        },
        "auth": "'$TOKEN'",
        "id": 1        
    }
    '
    curl -s -X POST -H "$HEADER" -d "$JSON" "$URL" > /dev/null
    echo "Evento reconhecido com sucesso."
}

event_ack