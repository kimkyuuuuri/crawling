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
        if(i%2==0):
            link='https://www.musinsa.com'+brand['href']
            req2 = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
            url = urlopen(req2,context=context).read()
            _main_page2 = BeautifulSoup(url, 'html.parser')
            category=_main_page2.findAll("div","brand_logo brandLogo")
            for i2,brand_for_img in enumerate(category):
               
                select=brand_for_img.select_one('img')
                kr_name=select['alt'].split('(')[0]
                eng_name=select['alt'].split('(')[1].split(')')[0]
                img_link="https:"+select['src']
                image_name = eng_name.replace(" ", "")
                print(image_name)
                try:
                    urllib.request.urlretrieve(img_link,image_name+".png")
                    sheet.append([eng_name,kr_name,image_name+'png'])
                except:
                    continue
                    
     

for i in range(1,356):
    allbrand(i)
    print(i)
wb.save("musinsa_brand_공백제거.xlsx")

