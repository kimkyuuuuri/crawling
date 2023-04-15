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
wb = openpyxl.Workbook()
sheet = wb.active

period = 1
month = 1
result_df = pd.DataFrame()
index=1
index_backup=1

while period < 2 and month<3:
    try:
        context = ssl._create_unverified_context()
        driver = wd.Chrome('/Users/kimkyuri/Documents/학교공부/4-1/sluv/crawling/celeb/chromedriver_mac_arm64/chromedriver')
        driver.maximize_window()

        # 드라이버가 해당 url 접속
        url = 'https://www.melon.com/chart/index.htm' # 멜론차트 페이지
        driver.get(url)                                                                     
        time.sleep(0.5)
       

        # 차트파인더 클릭
        driver.find_element_by_xpath('//*[@id="gnb_menu"]/ul[1]/li[1]/div/div/button/span').click()
        time.sleep(0.5)
     
        # 월간차트 클릭
        driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/h4[2]/a').click()
        time.sleep(1)
    

        # 연대선택 
        driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/div/div[1]/div[1]/ul/li[{}]/span/label'.format(period)).click()
        time.sleep(1)
        

        # 연도선택
        
        driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/div/div[2]/div[1]/ul/li[1]/span/label').click()
        time.sleep(1)
        

        # 월선택 8월 클릭
        driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/div/div[3]/div[1]/ul/li[{}]/span/label'.format(month)).click()
        time.sleep(1)
       
        

        # 장르선택 종합 클릭
        
        driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/div/div[5]/div[1]/ul/li[3]/span/label').click()
        time.sleep(1)
        print(1)
    
        
        # 검색버튼 클릭
        driver.find_element_by_xpath('//*[@id="d_srch_form"]/div[2]/button/span/span').click()
        time.sleep(1)
        month+=1
        if month >12:
            period+=1
            month=1
        
        # html 정보 가져오기
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
       
        upper_category =  soup.findAll('span','checkEllipsis')
        #upper_category =  soup.findAll('div','fc_mgray')
        
        for i,title in enumerate(upper_category):
            test =  title.findAll('a','fc_mgray')
            for j,test2 in enumerate(test):
            
                artist_id=(test2['href'].split("'")[1].split("'")[0])
                artist_link="https://www.melon.com/artist/timeline.htm?artistId="+artist_id

                req2 = Request(artist_link, headers={'User-Agent': 'Mozilla/5.0'})
                url = urlopen(req2,context=context).read()
                _artist_page = BeautifulSoup(url, 'html.parser')
                
                artist_info = _artist_page.findAll("div", "wrap_atist_info")
                name = _artist_page.findAll("p","title_atist")
                member_name = _artist_page.findAll("p","wrap_atistname")
                
                
                for i3,artist in enumerate(artist_info):
                    name = artist.findAll("p","title_atist")
                    member_name = artist.findAll("div","wrap_atistname")
                    for i4,artist4 in enumerate(name):
                        
                        for i5,artist5 in enumerate(artist4):
                            if i5%2==1:
                                print(artist5.text)
                                sheet.append([index,0,artist5.text])
                                index_backup=index
                                index+=1
                                
                            
                        
                    for j,member in enumerate(member_name):
                        test=member.findAll("a","atistname")
                        for i5,artist5 in enumerate(test):
                            
                           
                            sheet.append([index,index_backup,artist5.text])
                            index+=1
                          
                        

            
                    
                
            #print(artist_id)
                                    
            
        
              
                    
     
      
        
       
    except:
        print(period)
        break

wb.save("melon_singer.xlsx")

#wb.save("musinsa_brand_new_add.xlsx")

#wb쓰면 출력되는데 안하면 안됨! 
