#coding=utf-8
import geturl as getstart
from multiprocessing import Pool
import requests,re
##import pymongo
import time
from bs4 import BeautifulSoup
##clients=pymongo.MongoClient('127.0.0.1')
##db=clients['hexun']
##col1=db['fund']
##col2=db['detail']
col1=[]
col2=[]
url='http://fund.eastmoney.com/allfund.html'

def run_detail2(code,name,url):
        soup=getstart.geturl_utf8(url)
        tags=soup.find_all(class_='ui-font-middle ui-color-red ui-num')
        print("loc2", len(tags))
        if (len(tags) >= 9):
                m1=tags[3].string
                y1=tags[4].string
                m3=tags[5].string
                y3=tags[6].string
                m6=tags[7].string
                rece=tags[8].string
                detail={'代码':code,'名称':name,'近1月':m1,'近3月':m3,'近6月':m6,'近1年':y1,'近3年':y3,'成立来':rece}
                #print(detail)
                col2.insert(0, detail)
        else:
                print("loc3", code, name, url)
                print(tags)
	


def run_detail1(code,name,url):
        soup=getstart.geturl_utf8(url)
        tags=soup.select('dd')
        try:
                print("loc1", len(tags))
                m1=(tags[1].find_all('span')[1].string)
                y1=(tags[2].find_all('span')[1].string)
                m3=(tags[4].find_all('span')[1].string)
                y3=(tags[5].find_all('span')[1].string)
                m6=(tags[7].find_all('span')[1].string)
                rece=(tags[8].find_all('span')[1].string)
                detail={'代码':code,'名称':name,'近1月':m1,'近3月':m3,'近6月':m6,'近1年':y1,'近3年':y3,'成立来':rece}
                #print(detail)
                col2.insert(0, detail)
        except:
                run_detail2(code,name,url)

soup=getstart.geturl_gbk(url)
tags=soup.select('.num_right > li')
for tag in tags:
	if tag.a is None:
		continue
	else:
		content=tag.a.text
		code=re.findall(r'\d+',content)[0]
		#print(code)
		name=content.split('）')[1]
		#print(name)
		url=tag.a['href']
		#print(content)
		content_dict={'code':code,'name':name,'url':url}
		#print (content_dict)
		col1.insert(0, content_dict)
		time.sleep(0.1)
		run_detail1(code,name,url)

print(col1)

print(col2)
