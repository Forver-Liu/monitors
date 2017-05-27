#!/usr/bin/env python
#coding:utf-8

import json
import urllib2
import time,datetime
import sys
import xlrd

user="Admin"
password="zabbix"

url="http://zabbix.forver.com/api_jsonrpc.php"
header={"Content-Type":"application/json"}

user_login_data=json.dumps(
	{"jsonrpc":"2.0",
	"method":"user.login",
	"params":{"user":user,"password":password,"userData":"true"},
	"id":1}
)

def curl_exe(Data):
	request=urllib2.Request(url,Data,header)
	try:
		result=urllib2.urlopen(request)
		response=json.loads(result.read())
		result.close()
		return response
	except urllib2.URLError,e:
		print "Auth Failed,Please check your name and password,%s"%(e)
		sys.exit(3)

def item_get_data(ItemID,Session):
	return json.dumps(
	{
		"jsonrpc":"2.0",
		"method":"item.get",
		"params":{
			"itemids":ItemID,
			"output":"extend"
			},
		"auth":Session,
		"id":1
	})

def get_httptest(Session,httptestid):
	return json.dumps(
	{
		"jsonrpc": "2.0",
		"method": "httptest.get",
		"params": {
			"output": "extend",
			"selectSteps": "extend",
			"httptestids": httptestid
		},
		"auth":Session,
		"id": 1
		}
	)

def add_httpstest(Session,infos):
	step_num = len(infos)
	step_line = [{"no":int(infos[0][1]),"name":infos[0][2].encode('utf-8'),"url":infos[0][3].encode('utf-8'),"timeout":int(infos[0][4]),"required":infos[0][5].encode('utf-8'),"status_codes":int(infos[0][6]),"headers":infos[0][7].encode('utf-8')}]
	if step_num > 1:
		for num in range(1,step_num):
			step_line.append({"no":int(infos[num][1]),"name":infos[num][2].encode('utf-8'),"url":infos[num][3].encode('utf-8'),"timeout":int(infos[num][4]),"required":infos[num][5].encode('utf-8'),"status_codes":int(infos[num][6]),"headers":infos[num][7].encode('utf-8')})
	
	#print step_line

	datas = json.dumps(
	{
		"jsonrpc": "2.0",
		"method":"httptest.create",
		"params":{
			"name":infos[0][0].encode('utf-8'),
			"hostid":10084,
			"applicationid":459,
			"steps":step_line
		},
		"auth":Session,
		"id":1
		})
	print datas
	return datas

if __name__=='__main__':
	my_session=curl_exe(user_login_data)['result']['sessionid']
#	my_session="hhhhhhhh"
	print "Session:",my_session

#	items = curl_exe(item_get_data(25656,my_session))
#	print items

#	httptests = curl_exe(get_httptest(my_session,3))
#	print httptests

#	add_web = curl_exe(add_httpstest(my_session))
#	print add_web

	workbook = xlrd.open_workbook(sys.argv[1])
	sheet = workbook.sheet_by_index(0)
	s1 = sheet.cell(1,0).value

	web_info = []

	for line in range(1,sheet.nrows):
		row = sheet.row_values(line)
		if row[0] == u'':
			row[0] = s1
			web_info.append(row)
		else:
			if len(web_info) > 0:
			#	add_httpstest(my_session,web_info)
				curl_exe(add_httpstest(my_session,web_info))
			web_info = [row]
			s1 = row[0]

	#add_httpstest(my_session,web_info)
	curl_exe(add_httpstest(my_session,web_info))
