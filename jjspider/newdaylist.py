from scrapy import Spider, Request
from utils import split_genre
from openpyxl import Workbook
from my_settings import headers, base_urls, newdaylist_range
from pandas import DataFrame as df
from items import NewDayListItem,Novel
from datetime import datetime, timedelta
from urllib.parse import urlencode

#夹子
class NewDayListSpider(Spider):
  name='newdaylist'
  custom_settings = {
    'FEEDS':{
      'data/newdaylist.csv':{ 
        'format':'csv',
        'overwrite':False,
        'encoding':'gbk'
      }
    }
  }

  def start_requests(self):
    #get newdaylist in one month
    dates=[
      {'date':(datetime.today()-timedelta(days=i)).strftime('%Y-%m-%d')} for i in range(newdaylist_range)
    ]
    # print(dates)
    return [Request(url=base_urls['newdaylist']+'?'+urlencode(date), headers=headers, callback=self.parse, cb_kwargs={'list_date':date['date']}) for date in dates]

  def parse(self, response, list_date):
    newdaylist=response.json().get('data')
    rank=0
    for i in newdaylist:
      rank+=1
      item=NewDayListItem(
        date=list_date,
        vip_date=i['vipdate'],
        rank=rank,
        nid=i['novelId'],
        title=i['novelName'],
        aid=i['authorId'],
        author=i['authorName'],
        genre=i['novelClass'],
        yc=i['yc'],
        xx=split_genre(i['novelClass']),
        wd_count=i['novelsizeformat'],
        tags=i['tags']
      )
      yield item
    
if __name__=='__main__':
  print([{'date':(datetime.today()-timedelta(days=i)).strftime('%Y-%m-%d')} for i in range(newdaylist_range)])