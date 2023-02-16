from scrapy import Spider, Request
from datetime import datetime
from my_settings import base_urls,headers,version_code
import pandas as pd
from items import Novel
from utils import split_genre
import re

class NovelSpider(Spider):
  name='novel'
  custom_settings = {
    'FEEDS':{
      'data/novels_of_authors_filled.csv':{ 
        'format':'csv',
        'overwrite':False,
        'encoding':'utf-8'
      }
    }
  }

  def start_requests(self):
    df = pd.read_csv('data/novels_of_authors-newdaylist_[20230116-20230216].csv', index_col='nid', encoding='utf-8')
    return (Request(url=base_urls['novel']+'?novelId=%s' % index, headers=headers, callback=self.parse, cb_kwargs={
      'novel_id':index,
      'pub_date':novel['pub_date'],
      'author_id':novel['aid'],
      'author':novel['name']
      }) for index,novel in df.iterrows())

  def parse(self, response, novel_id, pub_date, author_id, author):
    data=response.json()
    print(data)
    item=Novel()
    item['id']=novel_id
    item['title']=data['novelName']
    item['aid']=author_id
    item['author']=author
    item['intro']=None
    item['logline']=data['novelIntroShort']
    item['genre']=data['novelClass']
    item['tags']=data['novelTags']
    item['xx']=split_genre(data['novelClass'])
    item['is_signed']=data['isSign']
    item['is_vip']=data['isVip']
    item['is_locked']=data['islock']
    item['wd_count']=data['novelSize']
    item['created']=pub_date
    item['updated']=data['renewDate']
    item['chpt_count']=data['maxChapterId']
    item['score']=data['novelScore']
    item['flw_count']=data['novelbefavoritedcount']
    item['style']=data['novelStyle']
    item['ranking']=data['ranking']
    item['avg_click']=data['novip_clicks']
    item['rating']=data['novelReviewScore']
    item['copystatus']=data['copystatus']
    item['cmt_count']=data['comment_count']
    yield item