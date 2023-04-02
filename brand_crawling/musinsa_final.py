from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

import json
import ssl
import requests
import openpyxl
import urllib.request
wb = openpyxl.Workbook()
sheet = wb.active



def allbrand(page):
    context = ssl._create_unverified_context()
    ssl._create_default_https_context = ssl._create_unverified_context
    req = Request('https://www.musinsa.com/dp/fragments/brands?categoryCode=&type=&sortCode=BRAND_RANK&listViewType=small&page='+str(page), headers={'User-Agent': 'Mozilla/5.0'})
    url = urlopen(req,context=context).read()
    _main_page = BeautifulSoup(url, 'html.parser')    
    upper_category =  _main_page.findAll('a', 'gtm-catch-click')
    eng_name=""
    kr_name=""
    img_link=""
    for i,brand in enumerate(upper_category):
        if(i%2==1):
            eng_name=brand.text.split("\n")[0]
           
            sheet.append([eng_name,kr_name,img_link])
        
        elif(i%2==0):
            
            #print(brand)
            #print(brand.attrs)
            
            link='https://www.musinsa.com'+brand['href']
            #a=brand['data-gtm-label']
            kr_name=brand.text
       
          
            req2 = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
            url = urlopen(req2,context=context).read()
            _main_page2 = BeautifulSoup(url, 'html.parser')
            category=_main_page2.findAll("div","brand_logo brandLogo")
            for i2,brand_for_img in enumerate(category):
       
                select=brand_for_img.select_one('img')
                img_link="https:"+select['src']
                urllib.request.urlretrieve(img_link,eng_name+".png")
                

        
                    
     


#for i in range(1,355):
for i in range(1,5):
    allbrand(i)
    print(i)
wb.save("musinsa_brand.xlsx")

#wb쓰면 출력되는데 안하면 안됨! 
