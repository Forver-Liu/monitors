#!/usr/bin/env python
#encoding:utf-8
# Description:monitor mongodb status for cacti or zabbix

import sys
import pymongo
from optparse import OptionParser

parser = OptionParser(usage="Usage:%prog [-h] [-p PORT] [-a PASSWD] HOSTNAME")
#parser.add_option("-h","--host",action="store_true",type="string",dest="hostM",default="127.0.0.1",help="default host is localhost")
parser.add_option("-p","--port",type="int",dest="portM",default=27017,help="mongodb default port is 27017")
parser.add_option("-u","--user",type="string",dest="userM",default="root",help="mongodb default user is root")
parser.add_option("-a","--auth",type="string",dest="authM",default=None,help="mongodb default password is None")
(options, args) = parser.parse_args()

if len(args) <> 1:
	parser.error("HOSTNAME is required.")
	sys.exit(1)
else:
	hostM = args[0]
#	print options

try:
	con = pymongo.Connection(host=hostM,port=int(options.portM),network_timeout=20)
	db = con.admin
	if options.authM:
		db.authenticate(options.userM,options.authM)
	serverStatus = db.command('serverStatus')

except Exception,e:
	print e.message
	sys.exit(1)
finally:
	con.close()

connections = serverStatus['connections']
cur_con = connections['current']
avail_con = connections['available']

queue = serverStatus['globalLock']
rqueue = queue['currentQueue']['readers']
wqueue = queue['currentQueue']['writers']

aclients = queue['activeClients']
areaders = aclients['readers']
awriters = aclients['writers']

mem = serverStatus['mem']
vsize = mem['virtual'] * 1024 * 1024
resident = mem['resident'] * 1024 * 1024
mapped = mem['mapped'] * 1024 * 1024

index = serverStatus['indexCounters']
misses = index['misses']

print "con_current:%s con_available:%s que_read:%s que_write:%s act_read:%s act_write:%s tol_insert:%s tol_query:%s tol_update:%s tol_delete:%s tol_command:%s mem_vsize:%s mem_resident:%s mem_mapped:%s idx_misses:%s"%(cur_con,avail_con,rqueue,wqueue,areaders,awriters,insert,query,update,delete,command,vsize,resident,mapped,misses)
