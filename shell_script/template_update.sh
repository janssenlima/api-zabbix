#!/bin/sh
# Script para atualizar tempaltes.

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

atualizar_template()
{
    JSON='
    {
        "jsonrpc": "2.0",
        "method": "template.update",
        "params": {
            "templateid": "10111",
            "name": "Template a remover 2"
        },
        "auth": "'$TOKEN'",
        "id": 1        
    }
    '
    curl -s -X POST -H "$HEADER" -d "$JSON" "$URL" > /dev/null
    echo "Template atualizado com sucesso."
}

atualizar_template