from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import csv
import json
context = ssl._create_unverified_context()
html = urlopen("https://news.naver.com/", context=context)
bsObject = BeautifulSoup(html,"html.parser")

for link in bsObject.find_all('a'):
    print(link.text.strip(),link.get('href'))

#참고 https://db-log.tistory.com/entry/33-%ED%81%AC%EB%A1%A4%EB%A7%81%ED%95%9C-%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%A5%BC-json-%ED%8C%8C%EC%9D%BC-%EB%A7%8C%EB%93%A4%EA%B8%B0
