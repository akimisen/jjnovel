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
    df = pd.read_csv('data/newdaylist_author-%s.csv' % self.period, encoding='utf-8')
    df=df.fillna(value={'ndlist_rank':-1,'ndlist_date':'0000/0/0'})
    df['ndlist_rank']=df['ndlist_rank'].astype(int)
    print(df)
    # df = df.fillna(value={'ndlist_date':'','ndlist_rank':None})
    return (Request(url=base_urls['novel']+'?novelId=%s' % novel['nid'], headers=headers, callback=self.parse, cb_kwargs={
      'novel_id':novel['nid'],
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
      item=Novel(
        nid=novel_id,
        title=data['novelName'],
        aid=author_id,
        author=author,
        intro=None,
        logline=data['novelIntroShort'],
        era=split_era(data['novelClass']),
        xx=split_xx(data['novelClass']),
        yc=split_yc(data['novelClass']),
        tags=data['novelTags'],
        is_signed=data['isSign'],
        is_vip=data['isVip'],
        # is_locked=data['islock'],
        word_count=data['novelSize'],
        created=pub_date[:10],
        updated=data['renewDate'][:10],
        chapter_count=data['maxChapterId'],
        score=data['novelScore'],
        like_count=data['novelbefavoritedcount'],
        style=data['novelStyle'],
        ranking=data['ranking'].replace('第','').replace('名',''),
        avg_click=data['novip_clicks'].replace('(章均)',''),
        rating=data['novelReviewScore'].replace('分',''),
        copystatus=data['copystatus'],
        comment_count=data['comment_count'],
        ndlist_rank=ndlist_rank,
        ndlist_date=ndlist_date
      )
      yield item