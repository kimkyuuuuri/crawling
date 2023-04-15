from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

import json
import ssl
import requests
import openpyxl
import urllib.request
wb = openpyxl.Workbook()
sheet = wb.active



def allbrand():
    context = ssl._create_unverified_context()
    ssl._create_default_https_context = ssl._create_unverified_context
    #req = Request('https://hbx.com/kr/men/brands?utm_source=hypebeast.kr', headers={'User-Agent': 'Mozilla/5.0'})
    req = Request('https://www.sivillage.com/dispctg/brandAtoZTab.siv', headers={'User-Agent': 'Mozilla/5.0'})
    url = urlopen(req,context=context).read()
    _main_page = BeautifulSoup(url, 'html.parser')    
    upper_category =  _main_page.findAll('p','brand-index__item--description')
    upper_category2=_main_page.findAll('p','brand-index__item--brand gold-mark')
    eng_name=""
    kr_name=""
    img_link=""
 
    link=_main_page.findAll('a','brand-index__item--text')
    
    for i,brand in enumerate(link):
            print(i)
            select=brand['href'].split("'")[-2]
            a = brand.find('p','brand-index__item--description')
            kor_name = a.text.split("\n")[-1].split(' ')[0]
            b = brand.find('p','brand-index__item--brand')
            eng_name = b.text.split("\n")[-1].split(' ')[0]
            
            link='https://www.sivillage.com/dispctg/initBrandGoodsCtg.siv?disp_ctg_no='+select
            
            req2 = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
            url = urlopen(req2,context=context).read()
            _main_page2 = BeautifulSoup(url, 'html.parser')
            category=_main_page2.findAll("div","brand_logo")
            
            for i2,brand_for_img in enumerate(category):
       
                select=brand_for_img.select_one('img')
              
               
                img_link=select['src']
               
                try:
                   
                    urllib.request.urlretrieve(img_link,eng_name+".png")
                    sheet.append([eng_name,kor_name,eng_name+".png"])
                except:
                    continue
            
    
        
                    
    
allbrand()
wb.save("m_sivillage.xlsx")

 

