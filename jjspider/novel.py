from scrapy import Spider, Request
from datetime import datetime
from my_settings import base_urls,headers,version_code
import pandas as pd
from items import Novel
from utils import split_genre
import re
from html2text import html2text

class NovelSpider(Spider):
  name='novel'
  custom_settings = {
    'FEEDS':{
      'data/novels_of_author_filled.csv':{ 
        'format':'csv',
        'overwrite':False,
        'encoding':'gbk'
      }
    }
  }

  def start_requests(self):
    df = pd.read_csv('data/novels_of_author.csv', encoding='gbk')
    #待优化
    return [Request(url=base_urls['novel']+'?novelId=%s' % nid, headers=headers, callback=self.parse, cb_kwargs={'novel_id':nid}) for nid in df['nid']]

  def parse(self, response, novel_id):
    data=response.json()
    print(data)
    item=Novel()
    item['id']=novel_id
    item['title']=data['novelName']
    item['aid']=data['authorId']
    item['author']=data['authorName']
    item['intro']=None
    item['logline']=data['novelIntroShort']
    item['genre']=data['novelClass']
    item['tags']=data['novelTags']
    item['xx']=split_genre(data['novelClass'])
    item['is_signed']=data['isSign']
    item['is_vip']=data['isVip']
    item['is_locked']=data['islock']
    item['wd_count']=data['novelSize']
    item['created']=None
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
      
if __name__=='__main__':
  data = pd.read_csv('newdaylist.csv', encoding='gbk')
  urls=['xxx'+str(aid) for aid in data['aid']]
  print(urls)