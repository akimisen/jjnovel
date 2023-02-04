import requests
import re
from datetime import datetime
from openpyxl import Workbook
from collections.abc import Iterable

def to_xlsx(data,savepath,fields=None):
  wb=Workbook()
  ws=wb.active

  # append fields
  if fields:
    ws.append(fields)

  # iter and append data
  if isinstance(data, Iterable):
    for r in data:
      ws.append(r)
  wb.save(savepath)

def tasks_from_videoIntro():
  url='http://www.jjwxc.net/videoIntroduction.php'
  r=requests.get(url)
  r.encoding='gbk'
  # with open('html-gbk.txt','w') as f:
  #   f.write(r.text)
  #regex for novel_info: id,title,author,genre
  #regex for chinese characters: \u300A([u4e00-u9fa5_a-zA-Z0-9]+\u300B
  match=re.findall(r"(?<=www\.jjwxc\.net/onebook\.php\?novelid=)(\d{7})\" target\=\"_blank\">\u300A(.*?)\u300B</a></td><td><a href=\"//www\.jjwxc\.net/oneauthor\.php\?authorid=\d+\" target=\"_blank\">(.*?)</a></td><td>(.*?)(?=</td>)", r.text)
  if match:
    # remove duplicates
    # nid,title,author,genre
    tasks=(i for i in match if (i[-1].find('言情')>0 or i[-1].find('纯爱')>0))
    #print('count:%d\nexample:%s' % (len(tasks),tasks[0]))
    savepath="log/videoIntro-%s.xlsx"% datetime.now().strftime("%Y%m%d_%H%M%S")
    to_xlsx(tasks,savepath,('nid','title','author','genre'))
  return tasks

def tasks_from_newDayList():
  url='http://app.jjwxc.org/androidapi/newDayList?channelMore=1'
  headers = {
  "User-Agent": "Mozilla/5.0 (Linux; Android 5.1; Lenovo) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 "
                  "Chrome/39.0.0.0 Mobile Safari/537.36/JINJIANG-Android/206(Lenovo;android 5.1;Scale/2.0)",
  "Referer": "http://android.jjwxc.net?v=207"
  # "server": "nginx",
  # "content-type": "text/plain;charset=utf-8",
  # "transfer-encoding": "chunked",
  # "keep-alive": "timeout=20",
  # "cache-control": "no-store, no-cache, must-revalidate, post-check=0, pre-check=0",
  # "hostname": "*.*.12.204",
  # "x-frame-options": "SAMEORIGIN",
  # "content-encoding": "gzipH"
}
  r=requests.get(url,headers=headers)
  tasks=[]
  if r.json().get('data'):
    novels=r.json()['data']['data']
    rank=0
    for n in novels:
      rank+=1
      # 原创:yc=1, 言情:xx==1, 耽美:xx=2
      if n['yc']=='1' and (n['xx']=='1' or n['xx']=='2'):
        tasks.append((n['novelId'],rank,n['novelName'],n['authorName'],n['novelClass'],n['novelsizeformat'],n['vipdate'][:10],n['tags'],datetime.now().strftime("%Y-%m-%d")))
    savepath="log/newDayList-%s.xlsx"% datetime.now().strftime("%Y%m%d_%H%M%S")
    to_xlsx(tasks,savepath,('nid','rank','title','author','genre','word_count','vip_date','tags','date'))
  #print('Task Count for newDayList: %d' % len(tasks))
  return tasks

if __name__=='__main__':
  tasks_from_videoIntro()
  tasks_from_newDayList()
