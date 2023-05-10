
import requests
from bs4 import BeautifulSoup
import re
import pymongo
from urllib.parse import urljoin
from urllib.request import urlopen, Request
import requests
from bs4 import BeautifulSoup
import re
import pymongo
from urllib.parse import urljoin
from itertools import count
import requests
import openpyxl
import urllib.request
import ssl
context = ssl._create_unverified_context()
wb = openpyxl.Workbook()
sheet = wb.active

pk=77
celeb_category_id=0

actor_url = 'http://www.cine21.com/rank/person/content'

formdata_dict = dict()
formdata_dict['section'] = 'actor'
formdata_dict['period_start'] = '2019-4'
formdata_dict['gender'] = 'all'


for page in count(1):
    try:
        formdata_dict['page'] = page


        res = requests.post(actor_url, data=formdata_dict)

        soup = BeautifulSoup(res.text,'html.parser')

        actors = soup.select('li.people_li div.name')
        if len(actors) == 0:
            break
            
        hits = soup.select('ul.num_info > li > strong')
        movies = soup.select('ul.mov_list')
        rankings = soup.select('li.people_li span.grade ')


        for index, actor in enumerate(actors):
            actor_item_dict = dict()
        
            actor_name = re.sub('\(\w*\)','',actor.text)
     
            actor_detail_url = actor.select_one('a').attrs['href']
            actor_detail_full_url = urljoin(actor_url,actor_detail_url)
        
            res = requests.get(actor_detail_full_url)
            soup = BeautifulSoup(res.text,'html.parser')

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
            
            pk+=1
       
         
            print(actor_name)
            if pk==1000:
                wb.save("actor_cinema_2019.xlsx")
                
            sheet.append([pk,celeb_category_id, eng_names[0],actor_name])
            
    except Exception as e:
        print(e)
        continue    
            
            

       
                 
                                
wb.save("actor_cinema_test.xlsx")
        
