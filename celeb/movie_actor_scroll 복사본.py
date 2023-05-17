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

formdata_dict = dict()
formdata_dict['section'] = 'actor'
formdata_dict['period_start'] = '2012-4'
formdata_dict['gender'] = 'all'


celeb_category_id=10
context = ssl._create_unverified_context()
driver = wd.Chrome('/Users/kimkyuri/Documents/학교공부/4-1/sluv/crawling/celeb/chromedriver_mac_arm64/chromedriver')
driver.maximize_window()

            # 드라이버가 해당 url 접속
url = 'https://serieson.naver.com/v3/broadcasting/products/korea_off_air?sortType=POPULARITY_DESC' 
driver.get(url)                                                                     
time.sleep(0.5)
for i in range(10):
   
    driver.find_element_by_xpath('//*[@id="content"]/div[2]/button').click()
    time.sleep(0.5)
    



html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
data = soup.find_all('li','ListCollection_broadcast_item__pE1Q3')
for i,drama in enumerate(data):
    try:
        data2 =  drama.find_all('a')[0]
        link=data2['href']
        print(link)
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
            actor_name = data_list[i]
                    #print(data_list[i])
            actor_url = 'http://www.cine21.com/search/person/?q='
            actor_url = actor_url + urllib.parse.quote(actor_name)
                    

            req2 = Request(actor_url, headers={'User-Agent': 'Mozilla/5.0'})
            url = urlopen(req2,context=context).read()
            _main_page2 = BeautifulSoup(url, 'html.parser')
            detail=_main_page2.findAll("p")
                    

                    
            for index, data in enumerate(detail):
                data2=data.findAll("a")
                actor_num=data2[0]['href'].split('=')[1]
                #print(actor_num)
                break

            actor_detail_url= 'http://www.cine21.com/db/person/info/?person_id='
            actor_detail_url = actor_detail_url + urllib.parse.quote(str(actor_num))
                    

            req2 = Request(actor_detail_url, headers={'User-Agent': 'Mozilla/5.0'})
            url = urlopen(req2,context=context).read()

                   # print(actor_detail_url)

            
            soup = BeautifulSoup(url,'html.parser')
            actor_item_dict = dict()

            for li_tag in soup.select('ul.default_info li'):
                actor_item_field = li_tag.select_one('span.tit').text 
                     
                actor_item_value = re.sub('<span.*?>.*?</span>','',str(li_tag))
                actor_item_value = re.sub('<.*?>','',actor_item_value) 
                      
                regex = re.compile(r'[\n\r\t]')
                actor_item_value = regex.sub('',actor_item_value)
                        
                actor_item_dict[actor_item_field] = actor_item_value

            if actor_item_dict['성별'] == '남':
                celeb_category_id= 11
            else:
                celeb_category_id= 12
                        

            naver_url = 'https://dict.naver.com/name-to-roman/translation/?query='
            name_url = naver_url + urllib.parse.quote(actor_name)

            req = Request(name_url, headers={'User-Agent': 'Mozilla/5.0'})
            res = urlopen(req,context=context)

            html = res.read().decode('utf-8')
            bs = BeautifulSoup(html, 'html.parser')
            name_tags = bs.select('#container > div > table > tbody > tr > td > a')
            eng_names = [name_tag.text for name_tag in name_tags]
                    
                   
                 
            print(actor_name)
              
            if num==800:
                 wb.save("actor_drama.xlsx")
                 break
                
            sheet.append([num,celeb_category_id, eng_names[0],actor_name])
                        



            #if num==5:
                                       
             #   wb.save("drama_actor.xlsx")
              #  break
            
       
    except Exception as e:
        print("오류 발생")
        print(e)
        continue

                   
wb.save("actor_drama2.xlsx")

