from scrapy import Spider, Request
from datetime import datetime, timedelta
from my_settings import base_urls,headers,version_code,newdaylist_range
import pandas as pd
from items import Novel
from utils import split_xx, split_era, split_yc, chinese_to_number
import re

class NovelSpider(Spider):
  name='newdaylist_author_novels'
  period='[%s-%s]'% ((datetime.today()-timedelta(days=newdaylist_range-1)).strftime('%Y%m%d'),datetime.today().strftime('%Y%m%d'))
  custom_settings = {
    'FEEDS':{
      'data/%s-[raw]%s.csv'%(name,period):{ 
        'format':'csv',
        'overwrite':True,
        'encoding':'utf-8'
      }
    }
  }

  def start_requests(self):
    df = pd.read_csv('data/newdaylist_author-[20230217-20230223].csv', index_col='nid', encoding='utf-8')
    df = df.fillna('')
    # df = df.fillna(value={'ndlist_date':'','ndlist_rank':None})
    return (Request(url=base_urls['novel']+'?novelId=%s' % index, headers=headers, callback=self.parse, cb_kwargs={
      'novel_id':index,
      'pub_date':novel['pub_date'][:10],
      'author_id':novel['aid'],
      'author':novel['name'],
      'ndlist_rank':novel['ndlist_rank'],
      'ndlist_date':novel['ndlist_date']
      }) for index,novel in df.iterrows())

  def parse(self, response, novel_id, pub_date, author_id, author, ndlist_rank, ndlist_date):
    data=response.json()
    # print(data)
    if data:
      item=Novel()
      item['nid']=novel_id
      item['title']=data['novelName']
      item['aid']=author_id
      item['author']=author
      item['intro']=None
      item['logline']=data['novelIntroShort']
      item['era']=split_era(data['novelClass'])
      item['xx']=split_xx(data['novelClass'])
      item['yc']=split_yc(data['novelClass'])
      item['tags']=data['novelTags']
      item['is_signed']=data['isSign']
      item['is_vip']=data['isVip']
      # item['is_locked']=data['islock']
      item['word_count']=data['novelSize']
      item['created']=pub_date[:10]
      item['updated']=data['renewDate'][:10]
      item['chapter_count']=data['maxChapterId']
      item['score']=data['novelScore']
      item['like_count']=data['novelbefavoritedcount']
      item['style']=data['novelStyle']
      item['ranking']=data['ranking'].replace('第','').replace('名','')
      item['avg_click']=data['novip_clicks'].replace('(章均)','')
      item['rating']=data['novelReviewScore'].replace('分','')
      item['copystatus']=data['copystatus']
      item['comment_count']=data['comment_count']
      item['ndlist_rank']=ndlist_rank if ndlist_rank else None,
      item['ndlist_date']=ndlist_date if ndlist_date else None
      yield item