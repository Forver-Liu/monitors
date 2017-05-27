#!/bin/bash

host="127.0.0.1"
passwd1="********"
passwd2="********"
passwd3="********"


if [ $# -lt 4 ];then
	echo "Usage: bash $0 -p [6379] -s section -k keys [-d] db [-o] opt"
	exit 1
else
	port=6379
	db=''
	opt=''
	while [ $# -gt 0 ]
	do
		if [ $1 == "-p" ];then
			port=$2
		fi
		if [ $1 == "-s" ];then
			section=$2
		fi
		if [ $1 == "-k" ];then
			key=$2
		fi
		if [ $1 == "-d" ];then
			db=$2
		fi
		if [ $1 == "-o" ];then
			opt=$2
		fi
		shift 2
	done
fi

case $port in
	6379)
		passwd=""
		;;
	6380)
		passwd=$passwd2
		;;
	6381)
		passwd=$passwd3
		;;
	*)
		passwd=$passwd1
		;;
esac
	

if [[ $section == "Keyspace" && $key == "dbs" ]];then
	cmd="/usr/local/redis/bin/redis-cli -p $port -a $passwd info Keyspace |grep '^db[0-9]\{1,2\}:*'|wc -l"
elif [[ ! -z $db && ! -z $opt ]];then
	echo $opt
	cmd="/usr/local/redis/bin/redis-cli -p $port info Keyspace |grep $db |tr -s ',' '\n' |awk -F [=] -v akey=$opt '/$akey/{print """$2"""}'"
	#cmd="/usr/local/redis/bin/redis-cli -p $port info Keyspace |grep $db |tr -s ',' '\n' |grep $opt |cut -d '=' -f 2"
else
	cmd="/usr/local/redis/bin/redis-cli -p $port -a $passwd info $section|grep ${key}: |cut -d ':' -f 2"
fi

#echo $cmd
eval $cmd
