# -*- coding:utf-8 -*-

import requests
from lxml import etree

loginurl='https://passport.csdn.net/account/login?ref=toolbar'

headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
		   'Referer':loginurl}

loginSession = requests.Session()

req = loginSession.get(loginurl,headers=headers)
sellector = etree.HTML(req.content)
lt = sellector.xpath('//input[@name="lt"]/@value')[0]
execution = sellector.xpath('//input[@name="execution"]/@value')[0]
#eventId = sellector.xpath('//input[@name="_eventId"]/@value')[0]

print u'参数数据已抓取完成！'
print lt,execution
postData = {'username':'ruochengyin@163.com','password':'Glxrcyin201314',
			'lt':lt,'execution':execution,'_eventId':'submit'}
html = loginSession.post(loginurl,data=postData,headers=headers)
print html.cookies
print "*"*100
html1 = loginSession.get("http://my.csdn.net",cookies=html.cookies,headers=headers)
print html1.status_code

# if 'mycsdn'in html.url