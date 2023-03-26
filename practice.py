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

def toJson(mnet_dict):
    with open('mnet_chart.json', 'w', encoding='utf-8') as file :
        json.dump(mnet_dict, file, ensure_ascii=False, indent='\t')

from collections import OrderedDict

LENGTH = min(len(img), len(brand), len(name), len(ref_no), len(price_origin), len(price_final))
    products = OrderedDict()

    print("processing data to json")
    # json 형태 저장하는걸 바꾸려면 여기수정
    for idx in range(0, LENGTH):
        products['no_' + str(idx + 1)] = {
            'img': img[idx].get_attribute("data-original"),
            'brand': brand[idx].text,
            'name': name[idx].text,
            'ref_no': ref_no[idx].text,
            'price': {
                'sale': price_origin[idx].text,
                'won': price_final[idx].text
            }
        }  
