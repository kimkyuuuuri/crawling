import selenium
from selenium import webdriver as wd
import time
from urllib.request import urlopen, Request
import pandas as pd
from bs4 import BeautifulSoup
import requests
from itertools import repeat
import ssl
import openpyxl
import urllib.request
import sys
from urllib.parse import quote


wb = openpyxl.Workbook()
sheet = wb.active
query = quote('박재범')
context = ssl._create_unverified_context()
query = quote('천러')


req = Request('https://music.apple.com/us/search?term='+query, headers={'User-Agent': 'Mozilla/5.0'})
url = urlopen(req,context=context).read()
_main_page = BeautifulSoup(url, 'html.parser')    
upper_category =  _main_page.findAll('div','scrollable-page svelte-11160mi')

try:       
    for i,title in enumerate(upper_category):
                data =  title.findAll('li','grid-item svelte-x9nlm5')
                print(data)
                for k,title2 in enumerate(data):
                    data2 =  title2.findAll('ul','top-search-lockup__description svelte-1an0vgx')
                 
                    if k==1:
                        break

                    for j,title3 in enumerate(data2):
                        data3 =  title3.findAll('li','top-search-lockup__primary svelte-1an0vgx')
                        print(data3[0].text)
                        break
              
                       
except Exception as e:
    print(e)



