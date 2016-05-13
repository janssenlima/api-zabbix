#!/bin/sh
# Script que imprime na saída a listagem dos hosts com seu ID e nome.

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

hosts()
{
    JSON='
    {
        "jsonrpc": "2.0",
        "method": "host.get",
        "params": {
            "output": [
                "hostid ",
                "host"
                ],
            "sortfield": "host"
        },
        "auth": "'$TOKEN'",
        "id": 1
    }
    '
    awk 'BEGIN { print "ID    - Host" }'
    curl -s -X POST -H "$HEADER" -d "$JSON" "$URL" | awk -v RS='{"' -F\" '/^hostid/ {printf $3 " - " $7 "\n"}'
}

hosts
