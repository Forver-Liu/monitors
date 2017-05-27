#!/bin/bash

to="$1"
subject="$2"

if [[ "$subject" =~ "OK" ]]; then
	emoji=':smile:'
elif [[ "$subject" =~ 'PROBLEM' ]]; then
	emoji=':frowning:'
else
	emoji=':ghost:'
fi

if [[ "$subject" =~ "正式环境" ]];then
	env='xxxxxxxxxxxxenv1'
elif [[ "$subject" =~ "测试环境" || "$subject" =~ "开发环境" ]];then
	env='xxxxxxxxxxxxenv2'
fi

url="https://hook.bearychat.com/=bw6lt/zabbix/${env}"
message="${subject}: $3"

payload="payload={\"channel\": \"${to//\"/\\\"}\", \"text\": \"${emoji} ${subject//\"/\\\"}\"}"
curl -m 5 --data-urlencode "${payload}" $url -A 'zabbix-bearychat-alertscript / https://github.com/ericoc/zabbix-bearychat-alertscript'
