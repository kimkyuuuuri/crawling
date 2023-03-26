import time
import requests
from bs4 import BeautifulSoup
def getPcode(page):
    pCodeList = []
    for i in range(1,page+1):
        print(i,"페이지 입니다")
        headers = {
               "Referer" : "http://prod.danawa.com/",
               "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36"
                }

        params = {"page" : page, "listCategoryCode" : 206, "categoryCode" : 206, "physicsCate1":72, 
                  "physicsCate2":73,"physicsCate3":0, "physicsCate4":0, "viewMethod": "LIST", "sortMethod":"BoardCount",
                  "listCount":30, "group": 10, "depth": 2, "brandName":"","makerName":"","searchOptionName":"",
                  "sDiscountProductRate":0, "sInitialPriceDisplay":"N", 
                  "sPowerLinkKeyword":"세탁기", "oCurrentCategoryCode":"a:2:{i:1;i:144;i:2;i:206;}", 
                  "innerSearchKeyword":"",
                  "listPackageType":1, "categoryMappingCode":176, "priceUnit":0, "priceUnitValue":0, "priceUnitClass":"",
                  "cmRecommendSort":"N", "cmRecommendSortDefault":"N", "bundleImagePreview":"N", "nPackageLimit":5, 
                  "nPriceUnit":0, "isDpgZoneUICategory": "N", "sProductListApi":"search","priceRangeMinPrice":"","priceRangeMaxPrice":"",
                 "btnAllOptUse":"false"}

        res = requests.post("http://prod.danawa.com/list/ajax/getProductList.ajax.php", headers = headers, data=params)
        soup = BeautifulSoup(res.text, "html.parser")
        a = soup.findAll("a", attrs = {"name":"productName"})
        
        for i in range(len(a)):
            pCodeList.append(a[i]['href'][35:-12])
        
    return pCodeList

print(getPcode(4))
