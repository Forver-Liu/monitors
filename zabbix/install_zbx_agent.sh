#!/bin/bash
#description:autoinstall zabbix agent on linux 
#author:forverliu2015@gmail.com

#set -x
soft_path=/usr/local/src
zabbix_version="3.2.4"
my_system="unknow system"
[ $(id -u) -ne 0 ] &&echo "Please run as root" &&exit 1

function system_judge {
	sys_version="`cat /proc/version`"
	if [[ $sys_version =~ "Red Hat" ]];then
		echo "Red Hat system"
		my_system="Red Hat system"
	elif [[ $sys_version =~ "Ubuntu" ]];then
		echo "Ubuntu system"
		my_system="Ubuntu system"
	elif [[ $sys_version =~ "Debian" ]];then
		echo "Debian system"
		my_system="Debian system"
	fi
	}

function pre_install {
	id zabbix
	[ $? -ne 0 ] && useradd -r -M -s /sbin/nologin zabbix
	[ ! -d "$soft_path" ] && mkdir -p "$soft_path"

	[ ! -f $soft_path/zabbix-${zabbix_version}.tar.gz ] && 	wget http://jaist.dl.sourceforge.net/project/zabbix/ZABBIX%20Latest%20Stable/${zabbix_version}/zabbix-${zabbix_version}.tar.gz -P $soft_path
	tar zxvf $soft_path/zabbix-${zabbix_version}.tar.gz -C $soft_path
	cd $soft_path
	touch pre_installed.txt
	echo -e "data path\nsource download\nuser add\nFINISHED!!!" >>zbx_preinstall.txt
	}

function install_agent {
	user=`id zabbix`
	if [[ $user =~ "no such user" ]];then
		agent_judge=`netstat -anlp|grep zabbix_agent`
	fi
	if [ -z "$agent_judge" ];then

		echo "install agentd on this system:$my_system!!!!"
		test ! -e $soft_path/pre_installed.txt && pre_install
		if [ "$my_system"x = "Red Hat system"x ];then
			yum install -y net-snmp-devel net-snmp
			yum install -y gcc\*

			agentd_inst_conf

			cp $soft_path/zabbix*/misc/init.d/tru64/zabbix_agentd /etc/init.d/zabbix_agentd
			sed -i '/#!\/bin\/sh/a\#chkconfig: 35 80 90\n#description:zabbix_agentd' /etc/init.d/zabbix_agentd
			sed -i 's/local/local\/zabbix/g' /etc/init.d/zabbix_agentd
			chmod +x /etc/init.d/zabbix_agentd
			chkconfig --add zabbix_agentd
			chkconfig zabbix_agentd on
		elif [[ "$my_system"x = "Ubuntu system"x ]] || [[ "$my_system"x = "Debian system"x ]];then
			apt-get install -y build-essential
			apt-get install -y snmp snmpd libsnmp-dev

			agentd_inst_conf

			cp $soft_path/zabbix*/misc/init.d/debian/zabbix-agent /etc/init.d/zabbix-agent
			sed -i 's/local/local\/zabbix/g' /etc/init.d/zabbix-agent
			chmod +x /etc/init.d/zabbix-agent
			update-rc.d	zabbix-agent defaults 96
			mv /etc/init.d/zabbix-agent /etc/init.d/zabbix_agentd
		fi
		clean_file

	else
		echo "zabbix_agent is already installed on this host"
		exit 3
	fi
	}


function agentd_inst_conf {
	cd $soft_path/zabbix*
	./configure --prefix=/usr/local/zabbix --enable-agent
	sleep 20
	make 
	sleep 20
	make install
	###################config zabbix agentd###############
	mkdir /usr/local/zabbix/scripts
	cp /usr/local/zabbix/etc/zabbix_agentd.conf /usr/local/zabbix/etc/zabbix_agentd.conf.bak
	Agtconfig_file="/usr/local/zabbix/etc/zabbix_agentd.conf"
	Agtlog_file="/var/log/zabbix_agentd.log"
	sed -i '30s/^/#/' $Agtconfig_file
	echo "LogFile=$Agtlog_file" >>$Agtconfig_file
	sed -i "/Server=127.0.0.1/ s/127.0.0.1/${server}/" $Agtconfig_file
	sed -i "/ServerActive=127.0.0.1/ s/127.0.0.1/${server}/" $Agtconfig_file

	if [ -n "$myhostname" ];then
		sed -i "s/Hostname=Zabbix server/Hostname=${myhostname}/" $Agtconfig_file
	else
		sed -i '143s/^/#/' $Agtconfig_file
		sed -i '151s/#//' $Agtconfig_file
	fi

	sed -i 's/# UnsafeUserParameters=0/UnsafeUserParameters=1/g' $Agtconfig_file
	sed -i 's/# HostMetadata=/HostMetadata=zabbix-10-10/' $Agtconfig_file
	touch $Agtlog_file
	chown zabbix:zabbix  $Agtlog_file
	sed -i '/^#/d' $Agtconfig_file
	sed -i '/^$/d' $Agtconfig_file
	echo "Include=/usr/local/zabbix/etc/zabbix_agentd.conf.d/*.conf" >>$Agtconfig_file
	echo -e "\n\n#memory\nUserParameter=memory.size[*],cat /proc/meminfo|grep ^\$1\":\"|awk -F[:\ ]+ '{print \$\$2}'" >>$Agtconfig_file
	echo -e "\n\n#tcp/udp\nUserParameter=tcp.con.num[*],ss -ant|grep \$1|wc -l" >>$Agtconfig_file
	}

function clean_file {
	rm -rf /usr/local/src/zabbix*
	}

system_judge

server="10.10.3.215"

if [ $# != 0 ];then
	while [ $# -gt 0 ]
		do
			if [ $1 == "-s" ];then
				server=$2
			elif [ $1 == "-n" ];then
				myhostname=$2
			fi
			shift 2
		done
	#install_agent
else
	echo "Usage:$0 -n HostName [-s Server]"
	exit 5
fi
