#!/bin/bash
datetime=`date`
log_file="/var/log/zabbix/alarm_mail.log"

echo -e "$datetime \nmailaddress:$1 \nsub:$2 \ncon:$3 \n">> $log_file

echo $3 | /usr/bin/mutt -s "$2" -e "my_hdr content-type:text/html" $1 >/dev/null  2>&1

if [ $? -eq 0 ];then
	echo $(date "+%Y-%m-%d %H:%M:%S")"  Successed">> $log_file
else
	echo $(date "+%Y-%m-%d %H:%M:%S")"   Failed">> $log_file
fi
