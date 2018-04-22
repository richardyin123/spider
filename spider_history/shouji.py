#coding=utf-8
import requests
import re
from bs4 import BeautifulSoup
import xlwt
import time

class ChinaPhone():
    def __init__(self,num=1):
        self.urls = set()
        self.param_urls = set()
        self.old_urls = set()
        self.num = num
        self.datas = []
    
    def getpage(self,url):
        headers = {
            'User_Agent':'User-Agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.59 Safari/537.36'}
        try:
            html_page = requests.get(url,headers=headers)
            return html_page.text
        except Exception as e:
            print str(e)
            
       
    def getUrl(self):
        if len(self.urls)==0:
            return None
        new_url = self.urls.pop()
        if new_url not in self.old_urls:
            self.old_urls.add(new_url)
            return new_url


    def paramgetUrl(self):
        if len(self.param_urls)==0:
            return None
        new_url = self.param_urls.pop()
        if new_url not in self.old_urls:
            self.old_urls.add(new_url)
            return new_url
    
    
    def html_parser(self,html_page,soup):
        try:
            title =  re.search(r'<h1><a.*?">(?P<title>.*?)</a></h1',html_page,re.S).group(1) 
            brand = re.search(u'选机中心.*?sub_57.*?html">(?P<pp>.*?)</a',html_page,re.S).group(1)
            time_parm = re.compile(u'outline.*?上市时间.*?n>(?P<time>.*?)</li>',re.S)
            price_parm = re.compile(r'Bid-price">(?P<pice>.*?)</em>',re.S)
            price = price_parm.search(html_page).group(1)
            if 'yen' in price :
                price = re.sub('&yen;','',price)
            #网络模式
            G_parm = soup.find('em',id="paramValue_206")
            if G_parm : G_parm = G_parm.get_text()
            
            #<em class="licont" id="paramValue_19">单卡多模</em>
            mo_parm = soup.find('em',id='paramValue_19')
            if mo_parm : mo_parm = mo_parm.get_text()
            
            #<em class="licont" id="paramValue_177">Nano-SIM卡</em>
            sim_parm = soup.find('em',id="paramValue_177")
            if sim_parm : sim_parm = sim_parm.get_text()
            
            #<em class="licont" id="paramValue_7">138.3mm×67.1mm×7.1mm</em>
            cc_parm = soup.find('em',id = "paramValue_7" )
            if cc_parm : cc_parm = cc_parm.get_text()
            
            #<em class="licont" id="paramValue_8">138g</em>
            kg_parm = soup.find('em',id = "paramValue_8" )
            if kg_parm : kg_parm= kg_parm.get_text()
            
            #<em class="licont" id="paramValue_176">不支持</em>
            dcgh_parm = soup.find('em',id="paramValue_176")
            if dcgh_parm : dcgh_parm = dcgh_parm.get_text()      #电池是否支持拆卸
            
            #<em class="licont" id="paramValue_23">4.7英寸</em>
            pmcc_parm = soup.find('em',id="paramValue_23")
            if pmcc_parm : pmcc_parm = pmcc_parm.get_text()  #屏幕尺寸
            
            #<em class="licont" id="paramValue_29">IPS</em>
            pmcz_parm = soup.find('em',id="paramValue_29")
            if pmcz_parm : pmcz_parm = pmcz_parm.get_text()  #屏幕材质
            
            #<em class="licont" id="paramValue_21">1334×750像素</em>
            pmfbl_parm = soup.find('em',id="paramValue_21")
            if pmfbl_parm : pmfbl_parm = pmfbl_parm.get_text()  #屏幕像素
            
            #<em class="licont" id="paramValue_63">iOS 10</em>
            czxt_parm = soup.find('em',id="paramValue_63")
            if czxt_parm : czxt_parm = czxt_parm.get_text()  #操作系统
            
            #<em class="licont" id="paramValue_64">苹果A10</em>
            cpu_parm = soup.find('em',id="paramValue_64")
            if cpu_parm : cpu_parm = cpu_parm.get_text()  #cpu型号
            
            #<em class="licont" id="paramValue_173">八核</em>
            hx_parm = soup.find('em',id="paramValue_173")
            if hx_parm : hx_parm = hx_parm.get_text()  #核心数
            
            #<em class="licont" id="paramValue_91">1741MHz</em>
            zp_parm = soup.find('em',id="paramValue_91")
            if zp_parm : zp_parm = zp_parm.get_text()  #cpu主频率
            
            #<em class="licont" id="paramValue_65">2GB</em>
            yxnc_parm = soup.find('em',id="paramValue_65")
            if yxnc_parm : yxnc_parm = yxnc_parm.get_text()  #运行内存
            
            #<em class="licont" id="paramValue_62">8GB</em>
            jsnc_parm = soup.find('em',id="paramValue_62")
            if jsnc_parm : jsnc_parm = jsnc_parm.get_text()  #机身内存
            
            #<em class="licont" id="paramValue_31">1300万像素</em>
            xs_parm = soup.find('em',id="paramValue_31")
            if xs_parm : xs_parm = xs_parm.get_text()  #像数
            
            #<em class="licont" id="paramValue_81">重力感应器,光感应器,距离传感器,指纹识别</em>
            gyq_parm = soup.find('em',id="paramValue_81")
            if gyq_parm : gyq_parm = gyq_parm.get_text()  #感应器
            
        except Exception as e:
                print u'解析出现问题！'
                print Exception,":",e
                          
        self.datas.append([title,brand,time_parm.search(html_page).group(1),price,mo_parm,sim_parm,cc_parm,kg_parm,dcgh_parm,pmcc_parm,pmcz_parm,pmfbl_parm,czxt_parm,cpu_parm,hx_parm,zp_parm,yxnc_parm,jsnc_parm,xs_parm,gyq_parm,G_parm])

    def writeExcel(self,sheet):
        try:
            sheet.write(0,0,u"手机名称")
            sheet.write(0,1,u"品牌")
            sheet.write(0,2,u"上市时间")
            sheet.write(0,3,u"价格")
            sheet.write(0,4,u"模式")
            sheet.write(0,5,u"SIM卡")
            sheet.write(0,6,u"手机尺寸")
            sheet.write(0,7,u"手机重量")
            sheet.write(0,8,u"支持换电池")
            sheet.write(0,9,u"屏幕尺寸")
            sheet.write(0,10,u"屏幕材质")
            sheet.write(0,11,u"屏幕像素")
            sheet.write(0,12,u"操作系统")
            sheet.write(0,13,u"cpu型号")
            sheet.write(0,14,u"cpu核心数")
            sheet.write(0,15,u"cpu主频")
            sheet.write(0,16,u"手机运存")
            sheet.write(0,17,u"机身内存")
            sheet.write(0,18,u"后置摄像头")
            sheet.write(0,19,u"感应器")
            sheet.write(0,20,u"网络模式")
        except :
            print u"初始化失败！"
    
        print u'初始化excel完成！' 
       
    
    def spidermain(self):
        start = time.clock()
        if self.num < 1:
            return 
        print u"初始化url列表元素，请稍候！"
        for index in range(1,self.num+1):
            root_url = 'http://product.cnmo.com/all/product_t1_p{0}.html'.format(index)
            html = self.getpage(root_url)
            url_compile = re.compile(r'pul-img-box">.*?href="(?P<url>http.*?shtml)"', re.S)
            url_lists = url_compile.findall(html)
            if url_lists:
                for url in url_lists:
                    self.urls.add(url)              
        print u'完成第一轮url收集！'
        
        index = len(self.urls)
          
        while len(self.urls):
            if len(self.urls)%4==0:
                time.sleep(2)
            try:
                new_url = self.getUrl()
                html_page = self.getpage(new_url)
                url = re.search(r'class="online".*?a><a\shref=["](?P<url>.*?param.shtml)["]\starget', html_page,re.S)
                print url.group(1),time.strftime("%H:%M:%S")
                if  url :
                    parm_url = url.group(1)
                    self.param_urls.add(parm_url)
                    
            except Exception as e:
                print u'%s有问题！' %new_url
                print str(e)


            if len(self.param_urls)==30:
                while len(self.param_urls):
                    
                    if len(self.param_urls)%5==0:
                        time.sleep(1)
                    try:
                        new_get_url = self.paramgetUrl()
                        print u'即将抓取%s，请稍候！' %new_get_url
                          
                        if  re.search(r'param',new_get_url) :
                            param_page = self.getpage(new_get_url)
                            soup = BeautifulSoup(param_page,'lxml',from_encoding='utf-8').find('div',class_='fuceng' )
                            self.html_parser(param_page,soup)
                              
                    except Exception as e:
                        print Exception,":",e
                        print u'%s数据解析出现问题！' %new_get_url

                    
                        
                
        if len(self.old_urls) == index:
            print u'参数url收集完毕！'
  
        workbook = xlwt.Workbook(encoding='utf-8',style_compression=0)
        sheet = workbook.add_sheet('data',cell_overwrite_ok=True)
        self.writeExcel(sheet)   #对excel初始化写入标题
        if len(self.datas):
            for index,data in enumerate(self.datas):
                sheet.write(index+1,0,data[0].encode('utf-8'))
                sheet.write(index+1,1,data[1].encode('utf-8'))
                sheet.write(index+1,2,data[2].encode('utf-8'))
                sheet.write(index+1,3,data[3])
                sheet.write(index+1,4,data[4])
                sheet.write(index+1,5,data[5])
                sheet.write(index+1,6,data[6])
                sheet.write(index+1,7,data[7])
                sheet.write(index+1,8,data[8])
                sheet.write(index+1,9,data[9])
                sheet.write(index+1,10,data[10])
                sheet.write(index+1,11,data[11])
                sheet.write(index+1,12,data[12])
                sheet.write(index+1,13,data[13])
                sheet.write(index+1,14,data[14])
                sheet.write(index+1,15,data[15])
                sheet.write(index+1,16,data[16])
                sheet.write(index+1,17,data[17])
                sheet.write(index+1,18,data[18])
                sheet.write(index+1,19,data[19])
                sheet.write(index+1,20,data[20])
                
                        
        workbook.save("D:\\shouji.xls")
        end = time.clock()
        print u"已经抓取完成，请核查！共耗时间%s S" %(end-start)
                  
                
if __name__=='__main__':
    maxdex = int(raw_input("请输入计划抓取页数,全网抓输入0,具体页数请输入数字\n"))
    sj = ChinaPhone(maxdex)
    sj.spidermain()
    
    

        
        
        
        
        