#coding=utf-8
import urllib2
import re
import xlwt
import time
from pip._vendor.distlib.locators import Page


class SLWspider():
    def __init__(self,urls):
        #urls = set()
        self.root_urls = urls
        self.datas = []
    
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



    def getPageNum(self,url):
        num_url = url + str(1)
        
        html_doc = self.getPage(num_url)
        try:
            pagenum = re.search(r'totalpage=(\d+)',html_doc,re.S)
            return pagenum.group(1)
        except Exception,e:
            print  u"连接网页页码错误，错误原因",e.reason
            print u"%s没抓到"  %num_url
    
        
        
    def pageParser(self,url,page):
        
        try:      
            partten =re.compile( r'<h3><a.*?f="(?P<url>.*?)["].*?>(?P<lm>.*?)</a></h3>.*?<p>.*?>(?P<lx>.*?)</a>',re.S)
            
            data = re.findall(partten,page)
            
            for data1 in  data:
                self.datas.append([url,data1[0],data1[1],data1[2]])
        except Exception,e:
            print u'解析出现问题%s' %e.reason

        

    def writepage(self):
        
        if len(self.datas) ==0 :
            return
        if self.datas is None :
            return 
        if self.datas:
            print u'开始写入数据，请稍候！'
            with  open('D:\\fangchan\\365fangchan.txt','a') as files:
                for data in self.datas:
                    files.write(data[0]+',')
                    files.write(data[1].encode('utf-8')+',')
                    files.write(data[2].encode('utf-8')+',')
                    files.write(data[3].encode('utf-8'))
                    files.write('\n')
            files.close()
            print u'已经写入完成！'
        
#          workbook = xlwt.Workbook(encoding='utf-8',style_compression=0)
#          sheet = workbook.add_sheet('data',cell_overwrite_ok=True)
#          
#          try:
#              sheet.write(0,0,u"名称")
#              sheet.write(0,1,u"url")
#              sheet.write(0,2,u"楼盘名")
#          except:
#              print u"初始化失败！"
#          print u'初始化excel完成！'
#          
#          if self.datas:
#              for index,data in enumerate(self.datas):
#                  sheet.write(index+1,0,data[0])
#                  sheet.write(index+1,1,data[1])
#                  sheet.write(index+1,2,data[2].encode('utf-8'))
#          workbook.save("D:\\fangchan\\365fangchan.xls")
#          print u'已写入完成，请核查!'
#      

    
    def spidemain(self):
        if self.root_urls is None :
            return 

        while len(self.root_urls) :
                   
            new_url = self.root_urls.pop().strip('\n')
            
            numx = self.getPageNum(new_url)
            
            for i in range(1,int(numx)+1):
                
                time.sleep(1.5)
                             
                spide_url = new_url + str(i)
                print u'正在抓取 %s页，请等待！'      %spide_url                
                page = self.getPage(spide_url)
                
                self.pageParser(spide_url, page)

        
        self.writepage()

if __name__=='__main__':
    
    print u'即将开始读取365url文件'
    try:
        with  open('D:\\365url.txt','r') as files :
            root_url = files.readlines()
            
    except Exception,e:
        print  u"连接网页页码错误，错误原因",e.reason

    finally: files.close()    
    print u'读取url链表完成'    
    SLW = SLWspider(root_url)
    SLW.spidemain()







