#!/usr/bin/env python
#coding:utf-8

import base64
import hashlib
import urllib
import json

publicKey  = 'ucloudxxxx@xxxx.com1430731698000139967079'
privateKey = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'


ULB_info_params = {"Action":"DescribeULB",
		"Region":"cn-bj2",
		"ProjectId":"org-26862",
		"PublicKey":publicKey,
		}

def get_signature(privateKey,params):
	items = params.items()
	items.sort()

	params_data = ""
	for key,value in items:
		params_data = params_data + str(key) + str(value)
	params_data = params_data + privateKey

	sign = hashlib.sha1()
	sign.update(params_data)
	signatuer = sign.hexdigest()
	
	return signatuer

def get_url(params,signature):
	url = "https://api.ucloud.cn/?Action=" + params['Action']
	for key,value in params.items():
		if key != "Action":
			url = url + '&' + str(key) + '=' + str(value)
	url = url + '&Signature=' + signature
	return url

if __name__ == "__main__":
	enabled = 0
	total_node = 0
	ULB_info_signature = get_signature(privateKey,ULB_info_params)
	ULB_info_url = get_url(ULB_info_params,ULB_info_signature)
	ULB_info_data = urllib.urlopen(ULB_info_url).read()
	vServerSet = json.loads(ULB_info_data)['DataSet'][0]['VServerSet']

	for item in vServerSet:
		if item['VServerId'] == 'vserver-bcozps':
			total_node = item['PolicySet'][0]['TotalCount']
			hosts = item['BackendSet']
			for host in hosts:
				#print "PrivateIP:%s\tstatus:%s"%(host['PrivateIP'],host['Enabled'])
				if int(host['Enabled']) == 1:
					enabled = enabled + 1
	if enabled == total_node:
		print 0
	else:
		print 1
