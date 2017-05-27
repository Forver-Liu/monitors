#!/use/bin/env python
#coding:utf-8
# Description:for zabbix discovery disk partition on linux machine

import os
import re,json

cmd = """cat /proc/diskstats |grep -E '\ssd[a-z]\s|\sxvd[a-z]\s|\svd[a-z]\s'|awk '{print $3}'|sort|uniq"""
disks = []

def get_disks():
	f = os.popen(cmd)
	for disk in f.readlines():
		disks.append({'{#DISK_NAME}':disk.strip()})
	return disks

if __name__ == "__main__":
	datas = get_disks()
	print json.dumps({'data':datas},sort_keys=True,indent=4,separators=(',',':'))
