from scrapy import Spider, Request
from datetime import datetime
from my_settings import base_urls,headers,version_code
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
    df = pd.read_csv('data/newdaylist.csv', encoding='gbk')
    #待优化
    return [Request(url=base_urls['author']+'?authorid=%s&versionCode=277' % aid, headers=headers, callback=self.parse) for aid in df['aid']]

  def parse(self, response, **kwargs):
    data=response.json()
    print(data)
    item=Author()
    item['id']=data['authorId'],
    item['name']=data['authorName'],
    item['score']=data['authorScore']
    item['flw_count']=data['authorFavoriteCount']
    item['novels']=list()
    print('item dict:')
    print(item.__dict__)
    for k in data['novellist']:
      novellistname = data['novellist'][k]
      for n in novellistname:
        if n['novelsize']!='0' and n['maxChapterId']!='0' and n['islock']=='0':
          print((data['authorName'],n['novelid'],n['novelname']))
          item['novels'].append(n['novelid'])
    yield item      
      
if __name__=='__main__':
  data = pd.read_csv('newdaylist.csv', encoding='gbk')
  urls=['xxx'+str(aid) for aid in data['aid']]
  print(urls)