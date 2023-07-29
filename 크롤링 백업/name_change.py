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
context = ssl._create_unverified_context()
index=77

try:
    excel=pd.read_excel('/Users/kimkyuri/Documents/학교공부/4-1/sluv/crawling/celeb/actor.xlsx')
   
    data = pd.DataFrame.to_numpy(excel)
    for i in range(len(data)):
        kor_name=str(data[i]).split("['")[1].split("']")[0]
        index+=1
   
  
    naver_url = 'https://dict.naver.com/name-to-roman/translation/?query='
    name_url = naver_url + urllib.parse.quote(kor_name)

    req = Request(name_url, headers={'User-Agent': 'Mozilla/5.0'})
    res = urlopen(req,context=context)

    html = res.read().decode('utf-8')
    bs = BeautifulSoup(html, 'html.parser')
    name_tags = bs.select('#container > div > table > tbody > tr > td > a')
    eng_names = [name_tag.text for name_tag in name_tags]

    print(eng_names[0])
              
                       
except Exception as e:
    print(e)



