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

add_trigger_dependencia()
{
    JSON='
    {
        "jsonrpc": "2.0",
        "method": "trigger.adddependencies",
        "params": {
            "triggerid": "14410",
            "dependsOnTriggerid": "14411"
        },
        "auth": "'$TOKEN'",
        "id": 1        
    }
    '
    curl -s -X POST -H "$HEADER" -d "$JSON" "$URL" > /dev/null
    echo "Dependencia de trigger adicionada com sucesso."
}

add_trigger_dependencia