 
#from urllib.request import urlopen
#from bs4 import BeautifulSoup
##html = urlopen("http://www.pythonscraping.com/pages/page1.html")
#html = urlopen("http://www.weibo.com")
#bsObj = BeautifulSoup(html.read(),"html.parser")
#print(bsObj.body)

   

import re
import string
import os
import sys
import urllib
import urllib.request
from bs4 import BeautifulSoup
import requests
from lxml import etree

#print(sys.getdefaultencoding())

if(len(sys.argv)>=2):
    user_id = (int)(sys.argv[1])
else:
    #user_id = (int)(input('Enter user_id: '))
    user_id = 1431835440

cookie = {"Cookie": "_T_WM=36563fe54a7c7b57eba59ade6385f73f; ALF=1481185387; SCF=Aq8Z7xoitpIM1m6XgxHcMXhsBs2b-qb3tEAtcAHLTm_gf8bxcSZra6PvMiAaO0M6FDDiavN_eqVwD1fTREPIsrw.; SUB=_2A251JfsjDeTxGedK6FMZ8yvIzzyIHXVW6YVrrDV6PUJbktBeLWP5kW2eYcoYQL1MZa_MJZaqh9hqFT1AXg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WWaM8Jiz_UMiDVu9ko_OvJg5JpX5o2p5NHD95QpShep1hefShB7Ws4DqcjKi--Ri-isi-8Wi--NiK.XiKLs-ntt; SUHB=0HTn1JmiOb9hbZ; SSOLoginState=1478593395"}
url = 'http://weibo.cn/u/%d?filter=1&page=1'%user_id

html = requests.get(url, cookies = cookie).content
selector = etree.HTML(html)
#pageNum = (int)(selector.xpath('//input[@name="mp"]')[0].attrib['value'])
pageNum = 1

result = ""
urllist_set = set()
word_count = 1
image_count = 1

print('爬虫准备就绪...')

for page in range(1,pageNum+1):

  #获取lxml页面
  url = 'http://weibo.cn/u/%d?filter=1&page=%d'%(user_id,page) 
  lxml = requests.get(url, cookies = cookie).content

  #文字爬取
  selector = etree.HTML(lxml)
  content = selector.xpath('//span[@class="ctt"]')
  for each in content:
    text = each.xpath('string(.)')
    if word_count>=4:
      text = "%d :"%(word_count-3) +text+"\n\n"
    else :
      text = text+"\n\n"
    result = result + text
    word_count += 1
    
  #图片爬取
  soup = BeautifulSoup(lxml, "lxml")
  urllist = soup.find_all('a',href=re.compile(r'^http://weibo.cn/mblog/oripic',re.I))
  first = 0
  for imgurl in urllist:
    urllist_set.add(requests.get(imgurl['href'], cookies = cookie).url)
    image_count +=1

fo = open("C:/MyProjects/temp/%s"%user_id, "wb")
fo.write(result.encode(encoding ='utf-8'))
fo.close()
word_path=os.getcwd()+'\\%d'%user_id
print('文字微博爬取完毕')

link = ""
fo2 = open("C:/MyProjects/temp/%s_imageurls"%user_id, "wb")
for eachlink in urllist_set:
  link = link + eachlink +"\n"
fo2.write(link.encode(encoding ='utf-8'))
fo2.close()
print('图片链接爬取完毕')

user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
headers={'User-Agent':user_agent,} 


if not urllist_set:
  print('该页面中不存在图片')
else:
  #下载图片,保存在当前目录的pythonimg文件夹下
  image_path=os.getcwd()+'\\weibo_image'
  if os.path.exists(image_path) is False:
    os.mkdir(image_path)
  x=1
  for imgurl in urllist_set:
    temp= image_path + '\\%s.jpg' % x
    print('正在下载第%s张图片' % x)
    try:
      #urllib.request.urlretrieve(urllib2.urlopen(imgurl).geturl(),temp,headers)
      request=urllib.request.Request(imgurl,None,headers)
      response = urllib.request.urlopen(request)
      data = response.read()
      jpgfile = open(temp, "wb");
      jpgfile.write(data);
      jpgfile.close();
      
    except:
      print("该图片下载失败:%s"%imgurl)
    x+=1
    
print('原创微博爬取完毕，共%d条，保存路径%s'%(word_count-4,word_path))
print('微博图片爬取完毕，共%d张，保存路径%s'%(image_count-1,image_path))