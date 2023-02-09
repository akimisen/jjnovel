from scrapy import Spider, Request
from utils import split_genre
from openpyxl import Workbook
from my_settings import headers, base_urls
from pandas import DataFrame as df
from items import NewDayListItem,Novel
from datetime import datetime

#夹子
class NewDayListSpider(Spider):
  name='newdaylist'
  custom_settings = {
    'FEEDS':{
      'newdaylist_%s.csv':{ 
        'format':'csv',
        'overwrite':False,
        'encoding':'gbk'
      }
    }
  }

  def start_requests(self):
    request_urls=[base_urls['newdaylist']+datetime.today().strftime('%Y-%m-%d')]
    return [Request(url=url, headers=headers, callback=self.parse) for url in request_urls]

  def parse(self, response, **kwargs):
    newdaylist=response.json().get('data')
    rank=0
    for i in newdaylist:
      rank+=1
      item=NewDayListItem(
        date=datetime.today().strftime('%Y-%m-%d'),
        vip_date=i['vipdate'],
        rank=rank,
        nid=i['novelId'],
        title=i['novelName'],
        aid=i['authorId'],
        author=i['authorName'],
        genre=i['novelClass'],
        yc=i['yc'],
        xx=split_genre(i['novelClass']),
        word_count_w=i['novelsizeformat'],
        tags=i['tags']
      )
      yield item
    
if __name__=='__main__':
  print(NewDayListItem.__dict__)