from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

# 교보문고의 베스트셀러 웹페이지를 가져옵니다.
import json
import ssl
import requests
import openpyxl
wb = openpyxl.Workbook()
sheet = wb.active


def top100img():
    context = ssl._create_unverified_context()
    req = Request('https://www.musinsa.com/ranking/brand', headers={'User-Agent': 'Mozilla/5.0'})
    url = urlopen(req,context=context).read()
    _main_page = BeautifulSoup(url, 'html.parser')    
    upper_category =  _main_page.findAll('p','imgD')
    for i,music in enumerate(upper_category):
    # input 태그안에 title 속성값을 parsing한다.
        select=music.select_one('img')
        print(select['src'])
        print(i)
  
 #   print(music)
   # print("{}위: {}".format(i+1, music.input['thumbnail']))
    # print("{}위: {}".format(i + 1, music.find('input')['brandLogo']))


#top100img()



def allbrand(page):
    context = ssl._create_unverified_context()
    req = Request('https://www.musinsa.com/dp/fragments/brands?categoryCode=&type=&sortCode=BRAND_RANK&listViewType=small&page='+str(page), headers={'User-Agent': 'Mozilla/5.0'})
    url = urlopen(req,context=context).read()
    _main_page = BeautifulSoup(url, 'html.parser')    
    upper_category =  _main_page.findAll('a', 'gtm-catch-click')
   
    #print(upper_category)
    for i,music in enumerate(upper_category):
        if(i%2==0):
            
            #print(music)
            #print(music.attrs)
            
            link='https://www.musinsa.com'+music['href']
            a=music['data-gtm-label']
            b=music.text
            #print(link)
            #print("링크입니다")
            req2 = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
            url = urlopen(req2,context=context).read()
            _main_page2 = BeautifulSoup(url, 'html.parser')
            upper_category1=_main_page2.findAll("div","brand_logo brandLogo")
            for i2,music2 in enumerate(upper_category1):
       
                select=music2.select_one('img')
                c="https:"+select['src']

            sheet.append([a,b,c])
                    
     
       
        
        #print(select1)
        
            
            




def allbrand3():
    custom_header = {
    'referer' : 'https://www.musinsa.com',
    'user-agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'  }

#해당 접속 사이트가 아닌 원본데이터가 오는 url 추적. network에서 가지고 온다.
    url = "https://www.musinsa.com/dp/fragments/brands?categoryCode=&type=&sortCode=BRAND_RANK&listViewType=small&page=1"

    req = requests.get(url, headers = custom_header)    #custom_header를 사용하지 않으면 접근 불가

    if req.status_code == requests.codes.ok:    
        print("접속 성공")
        _main_page = BeautifulSoup(req, 'html.parser') 
        upper_category =  _main_page.findAll('a')
        print(upper_category)
       
        

#for i in range(1,355):
for i in range(1,5):
    allbrand(i)
    print(i)
wb.save("musinsa_testing.xlsx")



def allbrand2(page):
    context = ssl._create_unverified_context()
    req = Request('https://www.musinsa.com/brands?categoryCode=&type=&sortCode=BRAND_RANK&page=5&size=100', headers={'User-Agent': 'Mozilla/5.0'})
    print('모든브랜드')
    #url = urlopen(req,context=context).read()
    #_main_page = BeautifulSoup(url, 'html.parser')    
    
        #print("접속 성공")
        #stock_data = json.loads(req.text)        #json에 반환된 데이터가 들어가 있다.
        #for rank in stock_data['data']:         #stock_data는 'data' key값에 모든 정보가 들어가 있다.
         #   print(rank)
