#!/bin/bash
#Description:backup zabbix(webcode,configfile,nginxconfig,database,scripts)

cur_date=`date +%F`
[ -d /data/backup/ ] && mkdir -p /data/backup/
cd /data/backup/

#/usr/bin/mysqldump --login-path=zabbix --databases zabbix > zabbix_${cur_date}.sql
/usr/bin/mysqldump -u zabbix -pxxxxxxx --databases zabbix > zabbix_${cur_date}.sql
if [ $? -ne 0 ];then
	echo "backup zabbix dabases failed"
	exit 1
fi

tar zcf zabbix_${cur_date}.tgz zabbix_${cur_date}.sql /etc/nginx /data/wwwRoot/zabbix /usr/local/php/etc /usr/local/zabbix/etc /usr/local/zabbix/scripts /usr/local/zabbix/share/zabbix/alertscripts /home/lyb/scripts --exclude=/usr/local/zabbix/share/zabbix/alertscripts/*.log
if [ $? -ne 0 ];then
	echo "tar files failed"
	exit 2
fi

[ -f zabbix_${cur_date}.sql ] && rm -f zabbix_${cur_date}.sql
find ./ -name "zabbix*.tgz" -mtime +7 -delete
