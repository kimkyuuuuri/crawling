import selenium
from selenium import webdriver as wd
import time
import json
import re
from urllib.request import urlopen, Request
import pandas as pd
from bs4 import BeautifulSoup
import requests
from itertools import repeat
import ssl
import openpyxl
import urllib.request
wb = openpyxl.Workbook()
sheet = wb.active

period=1
year=1
month=1
index=3
num=0

while period < 3 and year <3: 
    
    try:
        if period ==1 and year==1 and month==4:
            year=2
            month=1
        if period ==1 and year==5:
            period=2
            year=1

        celeb_category_id=10
        context = ssl._create_unverified_context()
        driver = wd.Chrome('/Users/kimkyuri/Documents/학교공부/4-1/sluv/crawling/celeb/chromedriver_mac_arm64/chromedriver')
        driver.maximize_window()

        # 드라이버가 해당 url 접속
        url = 'https://serieson.naver.com/v3/broadcasting/products/korea_off_air?sortType=POPULARITY_DESC' 
        driver.get(url)                                                                     
        time.sleep(0.5)
       
        
        # 더보기 
        driver.find_element_by_xpath('//*[@id="content"]/div[2]/button').click()
        time.sleep(0.5)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find_all('li','ListCollection_broadcast_item__pE1Q3')
        for i,drama in enumerate(data):
            data2 =  drama.find_all('a')[0]
            link=data2['href']
            drama_number=link.split('broadcasting/')[1]
            
            url = 'https://apis.naver.com/seriesOnWeb/serieson-web/v2/views/'+drama_number
            driver.get(url)   
            #driver.find_element_by_xpath('//*[@id="content"]/div[2]/ul/li[1]/button/span').click()
            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')
            actors_str= str(soup.text).split('actors":')[1].split(',"screening')[0]
            data_list = eval(actors_str)
            for i in range(len(data_list)):
                num+=1
                print(data_list[i])


        if num==500:
            break
        
       
    except Exception as e:
        print("오류 발생")
        print(e)
        continue
                   
                       
wb.save("drama_actor.xlsx")

