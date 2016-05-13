#!/bin/sh
# Script que imprime na saída a versão da API do Zabbix

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

versao()
{
    JSON='
    {
        "jsonrpc": "2.0",
        "method": "apiinfo.version",
        "id": 0
    }
    '
    version=$(curl -s -X POST -H "$HEADER" -d "$JSON" "$URL" | cut -d '"' -f8)
    echo "Versao da API:" $version
}

versao