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
import re
import urllib.request
wb = openpyxl.Workbook()
sheet = wb.active


period = 1
year=1
month = 1
index=0
index_backup=1
celeb_category_id=10
artist_name=''
member_artist_name=''
name=''
idList=[]

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
        url = 'https://www.melon.com/chart/index.htm' 
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
        #driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/div/div[2]/div[1]/ul/li[1]/span/label').click()
        driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/div/div[2]/div[1]/ul/li[{}]/span/label'.format(year)).click()
        time.sleep(1)
        

        # 월선택 8월 클릭
        driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/div/div[3]/div[1]/ul/li[{}]/span/label'.format(month)).click()
        time.sleep(1)
       
        

        # 장르선택 종합 클릭
        if year==1 and period==1:
            driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/div/div[5]/div[1]/ul/li[3]/span/label').click()
        elif year ==2 and month>5 and period==1:
            driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/div/div[5]/div[1]/ul/li[3]/span/label').click()
        
        else:
            driver.find_element_by_xpath('//*[@id="d_chart_search"]/div/div/div[5]/div[1]/ul/li[1]/span/label').click()
        
        time.sleep(1)
        
    
        
        # 검색 버튼 클릭
        driver.find_element_by_xpath('//*[@id="d_srch_form"]/div[2]/button/span/span').click()
        time.sleep(1)
        month+=1                  
        if month == 13:
            year+=1
            month=1
        if year == 11:
            period+=1
            year=1
        
            
        print("period")
        print(period)

        print("year")
        print(year)

        print("month")
        print(month)
        
        # html 정보 가져오기
        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        upper_category =  soup.findAll('span','checkEllipsis')
        
        for i,title in enumerate(upper_category):
            data =  title.findAll('a','fc_mgray')
            for j,data2 in enumerate(data):
                artist_id=(data2['href'].split("'")[1].split("'")[0])
                if artist_id in idList:
                    continue

                else:
                    idList.append(artist_id)
                artist_link="https://www.melon.com/artist/timeline.htm?artistId="+artist_id

                
                req2 = Request(artist_link, headers={'User-Agent': 'Mozilla/5.0'})
                url = urlopen(req2,context=context).read()
                _artist_page = BeautifulSoup(url, 'html.parser')

                #솔로일 경우 category_id = 10
                celeb_category_id=10
                
                artist_info = _artist_page.findAll("div", "wrap_atist_info")
                name = _artist_page.findAll("p","title_atist")
                member_name = _artist_page.findAll("p","wrap_atistname")
                
                artist_detail_link="https://m2.melon.com/artist/detail/info.htm?artistId="+artist_id
                req = Request(artist_detail_link, headers={'User-Agent': 'Mozilla/5.0'})
                url = urlopen(req,context=context).read()
                _artist_detail_page = BeautifulSoup(url, 'html.parser')
                artist_detail_info = _artist_detail_page.findAll("div","item-detail")

                
                                  
                for i2,artist2 in enumerate(artist_detail_info):
                    artist_detail_info2 = artist2.findAll("div","txt-g")
                    
                    # 여성, 남성, 혼성 그룹인 케이스를 나눠 category_id 저장 
                    for i3,artist3 in enumerate(artist_detail_info2):
                        if '/' in artist3.text and '그룹' in artist3.text and '여성' in artist3.text and '\n' in artist3.text:
                            celeb_category_id=7
                            break
                        elif '/' in artist3.text and '그룹' in artist3.text and '남성' in artist3.text and '\n' in artist3.text:
                             celeb_category_id=8
                             break
                        elif '/' in artist3.text and '그룹' in artist3.text and '혼성' in artist3.text and '\n' in artist3.text:
                             celeb_category_id=9
                             break
                
                
                
                for i3,artist3 in enumerate(artist_info):
                    name = artist3.findAll("p","title_atist")
                    member_name = artist3.findAll("div","wrap_atistname")
                    for i4,artist4 in enumerate(name):
                        
                        for i5,artist5 in enumerate(artist4):
                            if i5%2==1:
                                name=artist4.text.split('아티스트명')[1]
                                index+=1


                                if (celeb_category_id!=10):
                                    index_backup=index

                                
                                kor_name=''
                                                             
                                if  len(re.sub(r"[a-zA-Z]", "", artist_name).split('(')[0]) !=1:
                                    kor_name = re.sub(r"[a-zA-Z]", "", artist_name).split('(')[0].strip()
                                elif len(re.sub(r"[a-zA-Z]", "", artist_name))==1:
                                    kor_name=''
                                elif len(re.sub(r"[a-zA-Z]", "", artist_name)) !=0 :
                                    kor_name = re.sub(r"[a-zA-Z]", "", artist_name).split('(')[1].split(')')[0].strip()
                                

                                eng_name_group  = re.sub(r"[ㄱ-ㅣ가-힣()]", "", name).strip()
                                if len(eng_name_group)==0:
                                    naver_url = 'https://dict.naver.com/name-to-roman/translation/?query='
                                    name_url = naver_url + urllib.parse.quote(kor_name)

                                    req = Request(name_url, headers={'User-Agent': 'Mozilla/5.0'})
                                    res = urlopen(req,context=context)

                                    html = res.read().decode('utf-8')
                                    bs = BeautifulSoup(html, 'html.parser')
                                    name_tags = bs.select('#container > div > table > tbody > tr > td > a')
                                    eng_names = [name_tag.text for name_tag in name_tags]
                                    if len(eng_names)>0:
                                        eng_name_group = eng_names[0]
                                                            
                           
                                sheet.append([index,"",celeb_category_id,name,artist_id, kor_name, eng_name_group])
                                
                             
                    # 그룹의 멤버 저장 
                    for k,member in enumerate(member_name):
                        member_name2=member.findAll("a","atistname")
                       
                        for i6,artist6 in enumerate(member_name2):
                            
                            artist_id2=artist6['href'].split("(")[1].split(")")[0]
                            if artist_id2 in idList:
                                continue
                            else:
                                idList.append(artist_id2)
                                artist_name=artist6.text
                                index+=1
               
                                print(artist_name)
                               
                                
                                kor_name=''
                                #kor_name = re.sub(r"[^가-힣]", "", name)
                               
                                
                                if  len(re.sub(r"[a-zA-Z]", "", artist_name).split('(')[0]) !=1:
                                    kor_name = re.sub(r"[a-zA-Z]", "", artist_name).split('(')[0].strip()
                                elif len(re.sub(r"[a-zA-Z]", "", artist_name))==1:
                                    kor_name=''
                                elif len(re.sub(r"[a-zA-Z]", "", artist_name)) !=0 :
                                    kor_name = re.sub(r"[a-zA-Z]", "", artist_name).split('(')[1].split(')')[0].strip()
                                
                                
                                #eng_name = re.sub(r"[^a-zA-Z\s]", "", name)
                                eng_name  = re.sub(r"[ㄱ-ㅣ가-힣()']", "", artist_name).strip()
                                if len(eng_name)==0 or eng_name==eng_name_group:
                                    naver_url = 'https://dict.naver.com/name-to-roman/translation/?query='
                                    name_url = naver_url + urllib.parse.quote(kor_name)

                                    req = Request(name_url, headers={'User-Agent': 'Mozilla/5.0'})
                                    res = urlopen(req,context=context)

                                    html = res.read().decode('utf-8')
                                    bs = BeautifulSoup(html, 'html.parser')
                                    name_tags = bs.select('#container > div > table > tbody > tr > td > a')
                                    eng_names = [name_tag.text for name_tag in name_tags]
                                    if len(eng_names)>0:
                                        eng_name = eng_names[0]
                                    
                             
                                sheet.append([index,index_backup,celeb_category_id,artist_name,artist_id2, kor_name, eng_name])
                                
    
       
    except Exception as e:
        print("오류 발생")
        print(e)
        continue
                   
                       
wb.save("melon_singer.xlsx")

