import re
from scrapy import Spider, Request
from utils import to_xlsx

class DailyListSpider(Spider):
  #夹子
  name='dailylist'

  def start_requests(self):
    urls=[
      'http://android.jjwxc.net/bookstore/favObservationByDate?versionCode=277&day=2023-02-07'
    ]
    return [Request(url=url, headers={
  "User-Agent": "Mozilla/5.0 (Linux; Android 5.1; Lenovo) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 "
                  "Chrome/39.0.0.0 Mobile Safari/537.36/JINJIANG-Android/206(Lenovo;android 5.1;Scale/2.0)",
  "Referer": "http://android.jjwxc.net?v=277"
  }, callback=self.parse) for url in urls]

  def parse(self, response, **kwargs):
    novels=response.json().get('data')
    rank=0
    date=re.search(r'(?<=day\=)\d{4}-\d{2}-\d{2}', response.url).group()
    print(date)
    rows=[]
    print(novels[0])
    for n in novels:
      rank+=1
      # 原创:yc=1, 言情:xx==1, 耽美:xx=2
      if n['yc']=='1':
        if n['xx']=='1':
          rows.append((n['novelId'],rank,n['novelName'],n['authorName'],'BG',n['novelClass'],n['novelsizeformat'],n['vipdate'],n['tags'],date))
        elif n['xx']=='2':
          rows.append((n['novelId'],rank,n['novelName'],n['authorName'],'BL',n['novelClass'],n['novelsizeformat'],n['vipdate'],n['tags'],date))          
    savepath="log/newDayList_%s.xlsx"% (date.replace('-',''))
    to_xlsx(rows,savepath,fields=('nid','rank','title','author','xx','genre','word_count','vip_date','tags','date'))
    print(rows[:5])