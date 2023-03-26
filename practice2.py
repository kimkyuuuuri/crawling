from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

# 교보문고의 베스트셀러 웹페이지를 가져옵니다.
import json
import ssl
context = ssl._create_unverified_context()
html = urlopen("http://www.kyobobook.co.kr/bestSellerNew/bestseller.laf",context=context)
bsObject = BeautifulSoup(html, "html.parser")




def get_upper_category():
    context = ssl._create_unverified_context()
    req = Request('https://www.musinsa.com/ranking/brand', headers={'User-Agent': 'Mozilla/5.0'})
    url = urlopen(req,context=context).read()
   # url = urlopen("http://store.musinsa.com" ,context=context)
    _main_page = BeautifulSoup(url, 'html.parser')
   # main_url = urlopen('http://store.musinsa.com',context=context)

    
    upper_category =  _main_page.findAll('p','imgD')
    for i,music in enumerate(upper_category):
    # input 태그안에 title 속성값을 parsing한다.
        select=music.select_one('img')
        print(select['src'])
        print(i)
    
    #print(cate)
    # input 태그안에 title 속성값을 parsing한다.
 #   print(music)
   # print("{}위: {}".format(i+1, music.input['thumbnail']))
    # print("{}위: {}".format(i + 1, music.find('input')['brandLogo']))
    
    print('<전체 카테고리 목록>')
    for category in upper_category:
        print(category.get_text())
    return upper_category

get_upper_category()

# 책의 상세 웹페이지 주소를 추출하여 리스트에 저장합니다.
book_page_urls = []
txt=bsObject.find_all('div','prod_info_box')
print(txt)

#이미지까지 가져오려면 한 depth 더 들어가야한다.

for cover in txt:   # {'class':'cover'}가 아닌 이유가 뭘까....
    link = cover.select_one('a').get('href')		# link = cover.select_one('a').get('href')와 같은 뜻
    #book_page_urls.append(link)
    print(link)


# 메타 정보로부터 필요한 정보를 추출합니다.메타 정보에 없는 저자 정보만 따로 가져왔습니다.
for index, book_page_url in enumerate(book_page_urls): #함수는 기본적으로 인덱스와 원소로 이루어진 터플(tuple)을 만듦
    html = urlopen(book_page_url)
    bsObject = BeautifulSoup(html, "html.parser")
    title = bsObject.find('meta',{'property':'eg:itemName'}.get('content'))
    author = bsObject.select('span.name a')[0].text
    image = bsObject.select('div.cover img')[0].get('src')
    #image = bsObject.find('meta', {'property':'eg:itemImage'}).get('content')
    url = bsObject.find('meta',{'property':'eg:itemUrl'}).get('content')
    origin_price = bsObject.find('meta',{'property':'eg:originalPrice'}).get('content')
    sale_price = bsObject.find('meta',{'property':'eg:salePrice'}).get('content')
    print(index+1 , title, author, image, url, origin_price, sale_price)



# td 태그에 check라는 class가 있는 td 태그를 모두 가져온다.
#musics = soup.find_all('img')
#print(musics)

# musics의 각 태그들에 대해서 
#for i, music in enumerate(musics):
    # input 태그안에 title 속성값을 parsing한다.
 #   print(music)
   # print("{}위: {}".format(i+1, music.input['thumbnail']))
    # print("{}위: {}".format(i + 1, music.find('input')['title']))

