#!/usr/bin/env python
#coding:utf-8

import os
import httplib
import json
import MySQLdb
import datetime

cur_data = datetime.datetime.now().strftime("%Y-%m-%d")
post_url = "https://api-test.xxxxx.com/v1/ucenter/login/"
web_login = "https://www-test.xxxxx.com/signIn"

test_appID = 496
test_host = 'api-test.xxxxx.com'
dev_appID = 497
dev_host = 'api-dev.xxxxx.com'
pd_appID = 624
pd_host = 'api.xxxxx.com'

def get_token(host):
	infos = {
		"login_name":"xxxx@xxxxx.com",
		"password":"************",
		"auto_login":"ture"}

	headers = {"Content-Type":"application/json"}
	params = json.dumps(infos)
	conn = httplib.HTTPSConnection(host,port=443,timeout=5)
	http_req = conn.request('POST',"/v1/ucenter/login/",params,headers)
	http_res = conn.getresponse()

	#print http_res.getheaders()
	if http_res.status == 200:
		#print http_res.reason
		result =  http_res.read()
		res_js = json.loads(result)
		token = res_js['data'][0]['accesstoken']

		with open('/var/log/zabbix/token.log','a+') as token_log:
			line = "[" + cur_data + "]\t" + host + "\ttoken:\"%s\""%(token) + '\n'
			token_log.write(line)
		token_log.close()

		return token
	else:
		print "get token failed"
		os.exit(3)

def update_token(token,appID):
	db_host = 'localhost'
	db_user = 'zabbix'
	db_pwd = '*************'

	sql_1 = """update httptest set headers="accesstoken:%s" where applicationid = %d and headers != ''"""%(token,appID)
	sql_2 = """update httpstep set headers="accesstoken:%s" where headers != '' and httptestid in (select httptestid from httptest where applicationid=%d)"""%(token,appID)

	sdb = MySQLdb.connect(db_host,port=3306,user=db_user,passwd=db_pwd,db='zabbix',charset="utf8",connect_timeout=30,unix_socket="/tmp/mysql.sock")
	cursor = sdb.cursor()

	cursor.execute(sql_1)
	cursor.execute(sql_2)
	sdb.commit()

	cursor.close()
	sdb.close()

if __name__ == "__main__":
	test_token = get_token(test_host)
	update_token(test_token,test_appID)

	dev_token = get_token(dev_host)
	update_token(dev_token,dev_appID)

	pd_token = get_token(pd_host)
	update_token(pd_token,pd_appID)
