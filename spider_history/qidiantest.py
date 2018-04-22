#coding=utf-8

import urllib2
from bs4 import BeautifulSoup
import re
import time
import sys  
reload(sys)
sys.setdefaultencoding('utf-8')



user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64)'
headers={'User-Agent':user_agent}

root_url='http://all.qidian.com/Book/BookStore.aspx?ChannelId=-1&SubCategoryId=-1&PageIndex='
# root_url='http://www.qidian.com/Book/1004235150.aspx'
with open('/urls_data.txt','a') as DataUrls:
    for PageIndex in xrange(2,2):
        url = root_url + str(PageIndex)           
        try:
            request = urllib2.Request(url,headers=headers)
            response = urllib2.urlopen(request)
            html_doc =  response.read().decode('utf-8')
            time.sleep(1)
            soup = BeautifulSoup(html_doc,'html.parser',from_encoding='utf-8')
            links = soup.find('div',class_ = "bookstoretwo clearfix").find_all('a',href = re.compile('http.*?\/Book\/\d+\.aspx'))
#             for link in links:
#                print  link['href'],link.get_text().encode('utf-8')
            print "正在写入第%d页数" %PageIndex
            for link in links:
                
                DataUrls.write(link['href']+','+link.get_text())
                print link['href']+','+link.get_text()
                DataUrls.write('\n')
            
        except Exception,e:
            print Exception,':',e
            print "craw %d filed" %PageIndex
        
DataUrls.close()
print "抓取over"
 
            
    
          




