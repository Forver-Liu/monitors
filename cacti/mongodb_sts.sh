#!/bin/bash
host="10.10.10.1"
passwd="********"
rst=''

case "$1" in
    conn)
        rst=`mongostat -n 1 -u dbbak -p $passwd --authenticationDatabase=admin|awk 'NR==2 {print $(NF-1)}'`
        ;;
    dirty)
        rst=`mongostat -n 1 -u dbbak -p $passwd --authenticationDatabase=admin|awk -F[\ ]+ 'NR==2 {print $8}'`
        ;;
    used)
        rst=`mongostat -n 1 -u dbbak -p $passwd --authenticationDatabase=admin|awk -F[\ ]+ 'NR==2 {print $9}'`
        ;;
    qr)
        rst=`mongostat -n 1 -u dbbak -p $passwd --authenticationDatabase=admin|awk -F[\ \|]+ 'NR==2 {print $(NF-7)}'`
        ;;
    qw)
        rst=`mongostat -n 1 -u dbbak -p $passwd --authenticationDatabase=admin|awk -F[\ \|]+ 'NR==2 {print $(NF-6)}'`
        ;;
    res)
        res=$(echo "db.serverStatus().mem" | mongo -u dbbak -p $passwd admin|awk -F[,\ ] '/"resident"/{print $3}')
        rst=$[res*1024*1024]
        ;;
	vsize)
		resize=$(echo "db.serverStatus().mem" | mongo -u dbbak -p $passwd admin|awk -F[,\ ] '/"virtual"/{print $3}')
		rst=$[resize*1024*1024]
		;;
	*)
	    echo "aaaaaaaaaaaa"
		#exit 5
esac

if [ -z $rst ];then
   echo 0
else
   echo $rst
fi
