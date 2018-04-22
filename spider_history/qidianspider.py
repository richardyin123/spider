#coding=utf-8

import urllib2
import re
from bs4 import BeautifulSoup
import xlwt
import time


class QDWX:
    def __init__(self,maxdex=1):
        self.root_url = 'http://a.qidian.com/?orderId=0&page='       
        self.urls = set()
        self.old_urls=set() 
        self.book_datas = []
        self.mindex = 1
        self.maxdex = maxdex
                
    #访问起点中文网
    def getPage(self,url):
        user_agent='Mozilla/5.0 (Windows NT 6.1; WOW64)'
        headers={'User-Agent':user_agent}    
        try:
            request = urllib2.Request(url,headers = headers)
            response = urllib2.urlopen(request)
            return response.read().decode('utf-8')
        except urllib2.URLError,e:
            print u"连接起点文学失败，错误原因",e.reason
            print u"%s没抓到"  %url      
    #获取最大页数       
    def getNumDex(self):
        url = self.root_url  + str(1)
        page = self.getPage(url)
        result = re.search(r'data-pageMax=["](\d+)["]', page,re.S)
        if result :
            print result.group(1)
    
    def getUrls(self,page):
        soup = BeautifulSoup(page,'html.parser',from_encoding='utf-8')
        links = soup.find_all('h4')
        for link in links:
            m = re.search(r'\/\/.*?\d+', str(link),re.S)
            if m and m.group() not in self.urls:              
                self.urls.add(m.group())
        print u"urls已整理完毕"

    #从下载的url列表中获取新一个新的url

    def getUrl(self):
        if len(self.urls)==0:
            return None
        new_url = self.urls.pop()
        if new_url not in self.old_urls:
            self.old_urls.add(new_url)
            return new_url
    
    def htmlParser(self,crawUrl,soup):
        try:
            crawUrl_Id = re.search(r'(\d+)', crawUrl)
            book_id = crawUrl_Id.group(1)
            book_name = soup.find('h1').find('em').get_text() #作品名
            writer = soup.find('a',class_="writer",href=re.compile(r'\/\/.*?id=\d+'))
            book_writer = writer.get_text()    #作者名
            book_writerId = 'http:'+writer['href']      #作者连接
            #状态
            book_staus = soup.find('p',class_='tag').find_all('span',class_='blue')
            book_progress = book_staus[0].get_text() #写作进度
            if len(book_staus)==2:
                book_quter = ''        #授权状态
                book_vip = book_staus[1].get_text()   #小说性质
            else :
                book_quter = book_staus[1].get_text()
                book_vip = book_staus[2].get_text()
            #分类
            book_lb = soup.find('p',class_='tag').find_all('a',class_='red')
            book_lb1 = book_lb[0].get_text()    #分类1
            book_lb2 = book_lb[1].get_text()    #分类2
            #点击等数据
            book_data = soup.find_all('p')[2]
            book_wordCount = book_data.get_text().split('|')[0]  #总字数
            book_clikCount = book_data.get_text().split('|')[1].split(u'·')[0]  #总点击
            book_allCount = book_data.get_text().split('|')[2].split(u'·')[0]  #总推荐
            #简介
            book_intro = soup.find('div',class_="book-intro").get_text().strip().replace('\t','').replace(' ','')
            #章数                   
            catalogCount_url = 'http://book.qidian.com/ajax/book/category?_csrfToken=jQvGxG6g2RFdSBT8vTFmpTND0O6Yzu9aOv5415Lp&bookId=' + str(book_id)
            catalogCountPage = self.getPage(catalogCount_url)

            #"chapterTotalCnt":1346
            book_catalogCount = re.search(r'chapterTotalCnt[":]+(\d+)',catalogCountPage,re.S)
            if book_catalogCount : book_catalogCount = book_catalogCount.group(1)
            #讨论人数
            discusCount_url = 'http://book.qidian.com/ajax/book/GetBookForum?_csrfToken=jQvGxG6g2RFdSBT8vTFmpTND0O6Yzu9aOv5415Lp&chanId=22&pageSize=15&bookId=' + str(book_id)
            discusCountPage = self.getPage(discusCount_url)
            #"threadCnt":522120,
            book_discusCount = re.search(r'threadCnt[":]+(\d+)', discusCountPage, re.S)
            if book_discusCount : book_discusCount = book_discusCount.group(1)          
            
            #作者的作品信息
            book_counts = soup.find('ul',class_='work-state').find_all('li')
            auther_count =  book_counts[0].find('em').get_text()  #作品数
            auther_wordCount =  book_counts[1].find('em').get_text()  #累计字数
            auther_days =  book_counts[2].find('em').get_text()     #创作天数
                        
            #评分
            bookScore_url = 'http://book.qidian.com/ajax/comment/index?_csrfToken=jQvGxG6g2RFdSBT8vTFmpTND0O6Yzu9aOv5415Lp&chanId=22&pageSize=15&bookId=' + str(book_id)
            bookScorePage = self.getPage(bookScore_url)
            #分数
            book_score = re.search(r'rate[":]+(.*?)[,"]+',bookScorePage,re.S)
            if book_score : book_score = book_score.group(1)
            #评分人数
            book_count = re.search(r'userCount[":]+(\d+)',bookScorePage,re.S)
            if book_count : book_count = book_count.group(1)
            

        except Exception,e:
            print Exception,":",e
            print u'解析出现问题！'
#          print book_score,book_count,book_catalogCount,book_discusCount
#          print book_name,book_writer,book_writerId,book_progress,book_quter,book_vip,book_lb1,book_lb2,book_wordCount,book_clikCount,book_allCount,book_score,book_count,book_intro,book_catalogCount,book_discusCount,auther_count,auther_wordCount,auther_days,book_id
        self.book_datas.append([book_name,book_writer,book_writerId,book_progress,book_quter,book_vip,book_lb1,book_lb2,book_wordCount,book_clikCount,book_allCount,book_score,book_count,book_intro,book_catalogCount,book_discusCount,auther_count,auther_wordCount,auther_days,book_id])
       
    def writeTitle(self,sheet):
        try:
            sheet.write(0,0,u"名称")
            sheet.write(0,1,u"作者")
            sheet.write(0,2,u"作者连接")
            sheet.write(0,3,u"写作进度")
            sheet.write(0,4,u"授权状态")
            sheet.write(0,5,u"小说性质")
            sheet.write(0,6,u"分类1")
            sheet.write(0,7,u"分类2")
            sheet.write(0,8,u"总字数")
            sheet.write(0,9,u"总点击")
            sheet.write(0,10,u"总推荐")
            sheet.write(0,11,u"得分")
            sheet.write(0,12,u"评分人数")
            sheet.write(0,13,u"简介")
            sheet.write(0,14,u"章数")
            sheet.write(0,15,u"讨论人数")
            sheet.write(0,16,u"作品个数")
            sheet.write(0,17,u"累计完成字数")
            sheet.write(0,18,u"累计完成天数")
            sheet.write(0,19,u"书号")
        except:
            print u"初始化失败！"
        print u'初始化excel完成！'     
        
    def spiderStarte(self):
        start = time.clock()
        count =1
        if self.maxdex < 1 :
            self.maxdex = self.getNumDex()
        if not isinstance(self.maxdex, int):
            self.maxdex = 1
        print u"初始化Urls列表，请稍等！"
        print u"计划抓取%d页数据" %self.maxdex
        for index in range(self.mindex,self.maxdex+1):
            craw_url = self.root_url + str(index)
            print craw_url
            page = self.getPage(craw_url)
            self.getUrls(page)
            if count%3==0:
                time.sleep(2)
            count+=1  
    
        print u'逐个解析url'             
        numCount=1 #计数
        while len(self.urls) :
            try :
#                  if numCount%3==0:
#                      time.sleep(2)
                new_craw_url = 'http:'+self.getUrl()
                html_doc = self.getPage(new_craw_url)
                soup = BeautifulSoup(html_doc,'lxml',from_encoding='utf-8').find('div',class_='wrap')
                self.htmlParser(new_craw_url,soup)
    #                  numCount+=1
                print u"正在抓取:%s,剩余:%d页！" %(new_craw_url,len(self.urls))
                
            except Exception,e:
                print Exception,":",e
                print u"抓取失误:%s" %new_craw_url
                self.old_urls.add(new_craw_url)
                    
        workbook = xlwt.Workbook(encoding='utf-8',style_compression=0)
        sheet = workbook.add_sheet('data',cell_overwrite_ok=True)
        self.writeTitle(sheet)   #对excel初始化写入标题
        if len(self.book_datas):
            for index,data in enumerate(self.book_datas):
                sheet.write(index+1,0,data[0].encode('utf-8'))
                sheet.write(index+1,1,data[1].encode('utf-8'))
                sheet.write(index+1,2,data[2])
                sheet.write(index+1,3,data[3].encode('utf-8'))
                sheet.write(index+1,4,data[4].encode('utf-8'))
                sheet.write(index+1,5,data[5].encode('utf-8'))
                sheet.write(index+1,6,data[6].encode('utf-8'))
                sheet.write(index+1,7,data[7].encode('utf-8'))
                sheet.write(index+1,8,data[8].encode('utf-8'))
                sheet.write(index+1,9,data[9].encode('utf-8'))
                sheet.write(index+1,10,data[10].encode('utf-8'))
                sheet.write(index+1,11,data[11])
                sheet.write(index+1,12,data[12])
                sheet.write(index+1,13,data[13].encode('utf-8'))
                sheet.write(index+1,14,data[14])
                sheet.write(index+1,15,data[15])
                sheet.write(index+1,16,data[16])
                sheet.write(index+1,17,data[17].encode('utf-8'))
                sheet.write(index+1,18,data[18])   
                sheet.write(index+1,19,data[19])
        workbook.save("D:\\qidian.xls")
        end = time.clock()
        print u"已经抓取完成，请核查！共耗时间%s S" %(end-start)
                        
       
if __name__ == "__main__":
    maxdex = raw_input("请输入计划抓取页数,全网抓输入0,具体页数请输入数字\n")
    zq = QDWX(maxdex)
    page = zq.spiderStarte()    
                 
            
            
            
    
        
    
            
    
            
        
            
        