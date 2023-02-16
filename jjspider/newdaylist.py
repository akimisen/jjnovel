from scrapy import Spider, Request
from utils import split_xx, split_era, split_yc
from openpyxl import Workbook
from my_settings import headers, base_urls, newdaylist_range, version_code
from pandas import DataFrame as df
from items import NewDayListItem,Novel
from datetime import datetime, timedelta
from urllib.parse import urlencode

#夹子
class NewDayListSpider(Spider):
  name='newdaylist'
  custom_settings = {
    'FEEDS':{
      'data/%s-[%s-%s].csv' % (name,(datetime.today()-timedelta(days=newdaylist_range-1)).strftime('%Y%m%d'),datetime.today().strftime('%Y%m%d')):{
        'format':'csv',
        'overwrite':True,
        'encoding':'utf-8'
      }
    }
  }

  def start_requests(self):
    #get newdaylist in date range,1 month by default 
    params=[
      {
        # 'version':version_code,
        'day':(datetime.today()-timedelta(days=i)).strftime('%Y-%m-%d')
      } for i in range(newdaylist_range)
    ]
    # print(dates)
    return [Request(url=base_urls['newdaylist']+'?'+urlencode(param), headers=headers, callback=self.parse, cb_kwargs={'rank_date':param['day']}) for param in params]

  def parse(self, response, rank_date):
    newdaylist=response.json().get('data')
    if newdaylist:
      rank=0
      for i in newdaylist:
        rank+=1
        item=NewDayListItem(
          rank_date=rank_date,
          vip_date=i['vipdate'][:10],
          rank=rank,
          nid=i['novelId'],
          title=i['novelName'],
          aid=i['authorId'],
          author=i['authorName'],
          era=split_era(i['novelClass']),
          yc=split_yc(i['novelClass']),
          xx=split_xx(i['novelClass']),
          word_count=i['novelsizeformat'],
          tags=i['tags']
        )
        yield item
    
if __name__=='__main__':
  print([{'date':(datetime.today()-timedelta(days=i)).strftime('%Y-%m-%d')} for i in range(newdaylist_range)])