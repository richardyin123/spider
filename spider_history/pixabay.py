# -*- coding:utf-8 -*-
import re

import MySQLdb

from lxml import etree

import requests

class pixabayspide():
	def __init__(self):
		self.data = []

	def geturls(self,url):
		#构造头部
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64)'}
		try:
			html = requests.get(url,headers=headers)
			html_doc = html.content
			return html_doc   #返回源代码
		except Exception ,e:
			print u"连接网页失败，错误原因", e
			print u"%s爬取异常，请核实"  %url

	def htmlparse(self,page):
		#正则获取网页数据
		patent = re.compile(r'srcset="(?P<url>\S+).*?<em.*?</i>(?P<zz>.*?)</em.*?<em.*?</i>(?P<sc>.*?)</em.*?<em.*?</i>(?P<pj>.*?)</em.*?<a.*?>(?P<author>.*?)</a',re.S)
		html_page = patent.findall(page)
		for html_doc in html_page:
			datadic = {}
			datadic['url'] = html_doc[0].replace('__340', '_960_720')  #转换下图片像素，参考知乎崔斯特[微笑]
			datadic['zcounts'] = int(html_doc[1].strip())
			datadic['scounts'] = int(html_doc[2].strip())
			datadic['pjcounts'] = int(html_doc[3].strip())
			datadic['auther'] = html_doc[4]
			self.data.append(datadic)
		print u'已经抓取%d个记录' %len(self.data)
		# for data in self.data:
		# 	print data['url'], data['zcounts'], data['scounts'], data['pjcounts']

	def datasave(self):
		print u'开始连接mysql数据库'
		try:
			conn = MySQLdb.connect(host='localhost',port=3306,user='root',passwd='',db='python_test',charset='utf8')
			#获取操作游标
			cur = conn.cursor()
			cur.execute('DROP TABLE IF EXISTS PIXABAY')
			sql='''CREATE TABLE PIXABAY(
			URL VARCHAR(200) NOT NULL,
			ZCOUNTS INT ,
			SCOUNTS INT,
			PJCOUNTS INT,
			AUTHER VARCHAR(200)) '''
			cur.execute(sql)

			print u'数据表已经创建，可以开始导入数据'

			if len(self.data)!=0:
				for data in self.data:
					# print data['url'], data['zcounts'], data['scounts'], data['pjcounts'],data['auther']
					cur.execute("INSERT INTO PIXABAY(URL,ZCOUNTS,SCOUNTS,PJCOUNTS,AUTHER) VALUES(%s,%s,%s,%s,%s)",(data['url'],data['zcounts'],data['scounts'],data['pjcounts'],data['auther']))
				conn.commit()
			cur.close()
			conn.close()
			print u'数据已经全部插入库'
		except Exception,e:
			print u"错误原因",e

if __name__=='__main__':
	spide = pixabayspide()
	for i in range(1,165):
		url = 'https://pixabay.com/zh/editors_choice/'+'?media_type=photo&pagi='+str(i)
		page = spide.geturls(url)
		spide.htmlparse(page)
		print '已经完成第%d页数据的抓取' % i
	spide.datasave()













