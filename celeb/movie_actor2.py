import selenium
from selenium import webdriver as wd
import time
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
        url = 'https://www.kobis.or.kr/kobis/business/stat/boxs/findFormerBoxOfficeList.do' 
        driver.get(url)                                                                     
        time.sleep(0.5)
       
        
        # 국적 
        driver.find_element_by_xpath('//*[@id="sRepNationCd"]/option[2]').click()
        time.sleep(0.5)
     
        # 조회 
        driver.find_element_by_xpath('//*[@id="searchForm"]/div/div[4]/button').click()
        time.sleep(1)

 
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find_all('td','tal')
        for i,movie in enumerate(data):
            data2 =  movie.findAll('a')[0]
            
            code=data2['onclick'].split("'movie','")[1].split("'")[0]
            function = "mstView('movie','" + code + "')"
            driver.execute_script (function)
            time.sleep(1)

            html = driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            # 현재 영화가 하나로만 도는 문제 있음 !!
            

            table = driver.find_element_by_xpath('//*[@id="'+code+'_staff"]/dl/div[2]/dd/table[1]/tbody/tr/td')
            table_html = table.get_attribute('outerHTML')
            soup = BeautifulSoup(table_html, 'html.parser')
            actor_data = soup.find_all('a')
    
            

            for j, actor in enumerate(actor_data):
               
                code=actor['onclick'].split("'people','")[1].split("'")[0]
                print(actor.text.split("(")[0])
               
       
    except Exception as e:
        print("오류 발생")
        print(e)
        break
                   
                       
#wb.save("melon_singer.xlsx")

