#!/usr/bin/python
#coding:utf-8
#Author:forverLiu2015@gmail.com

import sys,time,re,os,glob

import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

import urllib,urllib2,cookielib
import zlib

mail_host = 'smtp.qiye.163.com'
mail_user = 'xxxxx@xxx.com'
mail_pass = '******'
mail_postfix = 'xxx.com'

login_url = "http://zabbix.xxxx.com/index.php"
chart_url = "http://zabbix.xxxx.com/chart.php"
zabbix_user = "Admin"
zabbix_pass = "******"
line = "ItemID"

me = "Airdroid"+'<'+mail_user+'>'

def get_itemid(src_mail):
	for line in src_mail:
		if "ItemID" in line:
			item_id = int(re.match(r'[^\d]+(\d+)[^\d]+',line,re.I|re.M).group(1))
			print "ItemID:",item_id
			return item_id

#########爬虫获取图片，保证cookie的可用性
def get_graph(itemID):
	post_value = {"request":"",
			"name":zabbix_user,
			"password":zabbix_pass,
			"autologin":"1",                #注意这个是否记住密码的选项，将造成生成的cookie长度不一样，短的能查看到图但没有数据
			"enter":"Sign+in"
		}
	post_data = urllib.urlencode(post_value)
	headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0",
		   "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
		   "Accept-Encoding":"gzip, deflate",
		   "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
		   "Connection":"Keep-Alive",
		   "Content-Length":"70",
		   "Content-Type":"application/x-www-form-urlencoded",
		   ###########这个cookie很重要，要求当前cookie正在浏览器上正常使用，才能顺利取图
		   "Cookie":"Hm_lvt_57f88cc10f8dc7874ad3b586c9cc389c=1451618794; PHPSESSID=fupvponfpl9b2v496unohpqj61; tab=0; zbx_sessionid=95303bc5bba8ee97fe04d92713414ca6"
		}
	
	request = urllib2.Request(login_url,post_data,headers)
	cj = cookielib.CookieJar()
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
	urllib2.install_opener(opener)
	
	result = opener.open(request)
#	print result.info()			  			 #查看下内容信息，如果是gzip要解压写入文件
#	result_html = zlib.decompress(result.read(), 16+zlib.MAX_WBITS)
	
	global graph_url
	graph_url = chart_url +"?itemids="+str(itemID)
	graph_data = urllib2.urlopen(graph_url)
	print graph_data.info()#.get('Content-Encoding')
	#graph_html = zlib.decompress(graph_data.read(), 16+zlib.MAX_WBITS)
	
	print graph_data.info().get('Content-Type')
	image_data = graph_data.read()
	if graph_data.info().get('Content-Type') == "image/png":
		image_file = open('last_%s.pnj'%itemID,'wb')
		image_file.write(image_data)
		image_file.close()
	else:
		trigged = open('trigged.pnj','rb')
		image_data = trigged.read()
		trigged.close()
	print "Graph_URL:",graph_url
	return image_data


def mail_con(txtData,imageData):
	msg = MIMEMultipart('related')
	msg['Subject'] = subject
	msg['From'] = me
	msg['to'] = to_list

	con_txt = MIMEText(txtData,_subtype='html',_charset='utf-8')
	msg.attach(con_txt)

	con_img = MIMEImage(imageData)
	con_img.add_header('Content-ID','digglife')
	msg.attach(con_img)

	return msg.as_string()

def send_mail(to_list,subject,contents):
	logfile = open('alarm_mail.log','a')
	
	try:
		s = smtplib.SMTP()
		s.connect(mail_host)
		s.ehlo()
		s.esmtp_features["auth"] = "LOGIN PLAIN"
		s.login(mail_user,mail_pass)
		s.sendmail(me,to_list,contents)
		s.close()
		log = time.ctime() + "\tOK\t" + subject +"\t"+ to_list + "\n"
	except Exception,e:
		log = time.ctime() + "\tFail\t" + subject +"\t"+ to_list + "\n"
	logfile.write("\n"+"\t"+graph_url+"\n")
	logfile.write(log)
	logfile.close()


if __name__ == "__main__":
	cur_pwd = os.getcwd()
	print cur_pwd
	os.chdir(cur_pwd)
	old_pnjs = glob.glob('last_*.pnj')
	for old_file in old_pnjs:
		os.remove(old_file)

	file_con = open('body2.txt','r')
	subject = sys.argv[2]
	to_list = sys.argv[1]

	try:
		src_mail_con = file_con.read()
		try:
			ItemID = re.match(r'.*ItemID:(\d+)[^\d]+.*',src_mail_con.replace('\n',''),re.S).group(1)
		except:
			ItemID = 0
		print "ItemID:",ItemID
		ImageData = get_graph(ItemID)
		MailCon = mail_con(src_mail_con,ImageData)
	
		send_mail(to_list,subject,MailCon)
	finally:
		file_con.close()
