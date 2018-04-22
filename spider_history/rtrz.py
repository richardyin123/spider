#coding=utf-8
import urllib2
from bs4 import BeautifulSoup
import re
import MySQLdb


class rtrz():
    def __init__(self):
        self.data_num = []
        self.data_tb = []
    
    def readUrl(self):
        try:
            with open('F:\dataurls.txt','r') as file_to_read:
                urls = file_to_read.readlines()
                return urls
        except Exception,e:
            print e.reason()
        finally:
            file_to_read.close()
        
    def getPage(self,url):

        user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64)'
        headers={'User-Agent':user_agent}    
        try:
            request = urllib2.Request(url,headers = headers)
            response = urllib2.urlopen(request)
            return response.read().decode('utf-8')
        except urllib2.URLError,e:
            print u"连接网页失败，错误原因",e.reason
            print u"%s没抓到"  %url  
        
    def pageParser(self,soup,url):
        
        #项目名称
        tit_name = soup.find('img',align="absmiddle").get_text()
        #预期年化收益
        nmb = soup.find_all('dt')
        nmb_year = nmb[0].get_text()
        #投资期限
        invesdate = nmb[1].get_text()
        #融资金额
        invesr = nmb[2].get_text()
        #开始时间
        start_time = 'na'
        time = re.search(r'<ul>.*?</span><em>(?P<time>.*?)</em></li>',str(soup),re.S)
        if time :
            start_time = time
        self.data_num.append(tit_name,nmb_year,invesdate,invesr,start_time.group(1),url)
        
        
               
    
    def insertdb(self):
        conn = MySQLdb.connect(host='localhost', user='root', passwd='', db='python_test', port = 3306, charset = 'utf8')
        cur = conn.cursor()
        if self.data_num :
            for data in self.data_num:
                cur.execute('insert into currentM(name,nmb_year, invesdate, invesr, start_time, url) values(%s%s%s%s%s%s)', (data[0],data[1],data[2],data[3],data[4],data[5]))
        conn.commit()
        cur.close()
        conn.close()      
        
    def main(self):
        get_urls = self.readUrl()
#          for new_url in get_urls:
#              page = self.getPage(new_url)             
        new_url = get_urls.pop()
        page = self.getPage(new_url)
        soup = BeautifulSoup(page,'html.parser',from_encoding='utf-8').find('div',class_='investCont')
        self.pageParser(soup, new_url)
        
        


if __name__=='__main__':
     yun = rtrz()
     yun.main()
