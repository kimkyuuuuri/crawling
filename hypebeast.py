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
    req = Request('https://hypebeast.kr/brands', headers={'User-Agent': 'Mozilla/5.0'})
    url = urlopen(req,context=context).read()
    _main_page = BeautifulSoup(url, 'html.parser')    
    #upper_category =  _main_page.findAll('li','uppercase hypebae:capitalize')
    
    upper_category2 =  _main_page.findAll('a','directory-list-name-container')
    upper_category3 =  _main_page.findAll('div',id='directory-brand-list')
    
    #print(upper_category3)
    
    
    for i,brand in enumerate(upper_category3):
            k= brand.findAll('index')
            for i2,brand2 in enumerate(k):
                print(brand2.keys())
                
            
            #link='https://hypebeast.kr/brands/'+brand.select_one(s'a')['href'].split('/')[-1]
            #print(link)
            #print(brand.select_one('a')['href'])
            print(4)
        
                    
    
allbrand()
wb.save("hypebeast.xlsx")

#wb쓰면 출력되는데 안하면 안됨! 
