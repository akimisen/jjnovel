import requests, re, os
from datetime import datetime
from utils import to_xlsx

def tasks_from_videoIntro():
  url='http://www.jjwxc.net/videoIntroduction.php'
  r=requests.get(url)
  r.encoding='gbk'
  with open('tmp','w') as f:
    f.write(r.text)
  #regex for novel_info: nid,title,aid,author_name,genre,signed_date
  #regex for chinese characters: \u300A([u4e00-u9fa5_a-zA-Z0-9]+\u300B
  match=re.findall(r"(?<=www\.jjwxc\.net/onebook\.php\?novelid=)(\d{7})\" target\=\"_blank\">\u300A(.*?)\u300B</a></td><td><a href=\"//www\.jjwxc\.net/oneauthor\.php\?authorid=(\d+)\" target=\"_blank\">(.*?)</a></td><td>(.*?)</td><td>(\d{4}\-\d{2})?</td>", r.text)
  if match:
    # remove duplicates
    # nid,title,aid,author_name,genre,signed_date
    print(match[0])
    #BL,BG
    _tasks=[i for i in match if (i[-2].find('言情')>0 or i[-2].find('纯爱')>0)]
    tasks=list(dict.fromkeys(_tasks))
    savepath="log/videoIntro-%s.xlsx"% datetime.now().strftime("%Y%m%d")
    to_xlsx(tasks,savepath,('nid','title','author_id','author_name','genre','signed_date'))
  return tasks

def tasks_from_newDayList(date):
  #date format: 2020-01-01
  url='http://android.jjwxc.net/bookstore/favObservationByDate?versionCode=277&day=%s' % date
  #url='http://app.jjwxc.org/androidapi/newDayList?channelMore=1'
  headers = {
  "User-Agent": "Mozilla/5.0 (Linux; Android 5.1; Lenovo) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 "
                  "Chrome/39.0.0.0 Mobile Safari/537.36/JINJIANG-Android/206(Lenovo;android 5.1;Scale/2.0)",
  "Referer": "http://android.jjwxc.net?v=277"
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
    novels=r.json()['data']
    rank=0
    for n in novels:
      rank+=1
      # 原创:yc=1, 言情:xx==1, 耽美:xx=2
      if n['yc']=='1':
        if n['xx']=='1':
          tasks.append((n['novelId'],rank,n['novelName'],n['authorName'],'BG',n['novelClass'],n['novelsizeformat'],n['vipdate'][:10],n['tags'],date))
        elif n['xx']=='2':
          tasks.append((n['novelId'],rank,n['novelName'],n['authorName'],'BL',n['novelClass'],n['novelsizeformat'],n['vipdate'][:10],n['tags'],date))          
    savepath="log/newDayList_%s.xlsx"% (date.replace('-',''))
    to_xlsx(tasks,savepath,('nid','rank','title','author','xx','genre','word_count','vip_date','tags','date'))
  #print('Task Count for newDayList: %d' % len(tasks))
  return tasks

if __name__=='__main__':
  date=datetime.now().strftime("%Y-%m-%d")
  tasks_from_videoIntro()
  tasks_from_newDayList(date)