from scrapy import Spider, Request
from datetime import datetime
from my_settings import base_urls,headers
import pandas as pd
from items import Author
class AuthorSpider(Spider):
  name='author'
  custom_settings = {
    'FEEDS':{
      'data/authors.csv':{ 
        'format':'csv',
        'overwrite':False,
        'encoding':'gbk'
      }
    }
  }

  def start_requests(self):
    data = pd.read_csv('newdaylist.csv', encoding='gbk')
    request_urls=[base_urls['author']+str(aid) for aid in data['aid']]
    return [Request(url=url, headers=headers, callback=self.parse) for url in request_urls]

  def parse(self, response, **kwargs):
    author=response.json().get('data')
    rank=0
    for i in author:
      rank+=1
      item=Author()
      item['id']=i['authorID'],
      item['name']=i['authorName'],
      item['novels']=[],
      for k in i['novellist']:
        nl = i['novellist'][k]
        for n in nl:
          if n['novelsize']!='0' and n['maxChapterId']!='0' and n['islock']=='0':
            item['novels'].append((n['novelid'],n['novelname']))
      yield item

if __name__=='__main__':
  data = pd.read_csv('newdaylist.csv', encoding='gbk')
  urls=['xxx'+str(aid) for aid in data['aid']]
  print(urls)