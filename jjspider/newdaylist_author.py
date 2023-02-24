from scrapy import Spider, Request
from datetime import datetime, timedelta
from my_settings import base_urls, headers, version_code, newdaylist_range
import pandas as pd
from items import NovelOfAuthor
from urllib.parse import urlencode
from utils import chinese_to_number

class AuthorSpider(Spider):
  name='newdaylist_author'
  period='[%s-%s]'% ((datetime.today()-timedelta(days=newdaylist_range-1)).strftime('%Y%m%d'),datetime.today().strftime('%Y%m%d'))
  custom_settings = {
    'FEEDS':{
      'data/%s-%s.csv'%(name,period):{ 
        'format':'csv',
        'overwrite':True,
        'encoding':'utf-8'
      }
    }
  }

  def start_requests(self):
    #read data from: newdaylist
    df = pd.read_csv('data/newdaylist-%s.csv' % self.period, index_col='nid', encoding='utf-8')
    print(df.head)
    return [Request(url=base_urls['author']+'?'+urlencode(dict(version=version_code,authorid=str(row['aid']))), headers=headers, callback=self.parse, cb_kwargs={
      'author_id':row['aid'],
      'ndlist_nid':index,
      'ndlist_rank':row['rank'],
      'ndlist_date':row['rank_date']
      }) for index,row in df.iterrows()]

  def parse(self, response, author_id, ndlist_nid, ndlist_rank, ndlist_date):
    data=response.json()
    # print(data)
    for k in data['novellist']:
      novellistname = data['novellist'][k]
      for n in novellistname:
        item=NovelOfAuthor(
          aid=author_id,
          name=data['authorName'],
          score=data['authorScore'],
          follower_count=data['authorFavoriteCount']
        )
        if n['novelid']==str(ndlist_nid):
          item['ndlist_rank']=ndlist_rank
          item['ndlist_date']=ndlist_date
        if n['novelsize']!='0' and n['maxChapterId']!='0' and n['islock']=='0':
          item['nid']=n['novelid']
          item['pub_date']=n['newtopdate']
          yield item
  