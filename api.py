import requests, json
# from my_settings import headers, VERSION_CODE, URLS
from collections.abc import Iterable
# from utils import to_xlsx


headers = {
  'reload':'true',
  'cacheShowed':'true',
  'Referer':'http://android.jjwxc.net?v=277',
  'User-Agent':'Mozilla/5.0 (Linux; Android 12; LIO-AN00 Build/HUAWEILIO-AN00; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/92.0.4515.105 Mobile Safari/537.36/JINJIANG-Android/277(LIO-AN00;Scale/3.0)',
  'versiontype':'reading',
  'VERSIONTYPE':'reading',
  'source':'android',
  'versionCode':'277',
  'Version-Code':'277',
  'Connection':'Keep-Alive',
  'Accept-Encoding':'gzip'
}
class Novel:
  def __init__(self,id) -> None:
    _info = requests.get("http://app-cdn.jjwxc.net/androidapi/novelbasicinfo", params={
        "novelId": str(id)
    }, headers=headers).json()
    if _info and _info['novelId']==str(id):
      self.id=str(id)
      self.title=_info['novelName']
      self.aid=_info['authorId']
      self.author=_info['authorName']
      self.intro=_info['novelIntro']
      self.genre=_info['novelClass']
      self.tags=_info['novelTags']
      self.signed=_info['isSign']
      self.is_vip=_info['isVip']
      self.locked=_info['islock']
      self.word_count=_info['novelSize']
      self.created_at=None
      self.updated_at=_info['renewDate']
      self.chapter_count=_info['maxChapterId']
      self.score=_info['novelScore']
      self.follower_count=_info['novelbefavoritedcount']
      self.style=_info['novelStyle']
      self.ranking=_info['ranking']
      self.avg_click=_info['novip_clicks']
      self.rating=_info['novelReviewScore']
      self.copystatus=_info['copystatus']
      self.comment_count=_info['comment_count']

  def get_comments(self):
    pass    

  def download_free_chpt(self):
    pass

  def collect_chapters(self):
    _chapters = requests.get("http://app-cdn.jjwxc.net/androidapi/chapterList", params={
        "novelId": self.id,
        "more": 0,
        "whole": 1
    }, headers=headers).json().get('chapterlist')
    chapters=[]
    if _chapters and isinstance(_chapters,Iterable):
      for i in _chapters:
        if i['chaptertype']=='0':
          chapters.append(dict(nid=i['novelid'],cid=i['chapterid'],name=i['chaptername'],locked=i['islock'],created_at=i['lastpost_time'],updated_at=i['chapterdate'],word_count=i['chaptersize'],is_vip=i['isvip'],click=i['chapterclick']))
      return chapters
    return None

  # @property
  # def chapters(self):
  #   return self.collect_chapters()


class Author:
  def __init__(self,id) -> None:
    response=requests.get("http://app.jjwxc.org/androidapi/authorColumn", params={
      "authorid": str(id),
      "versionCode": '277'
    }, headers=headers)
    print(response.url)
    _info = response.json()
    if _info:
      self.id=str(id)
      self.name=_info['authorName']
      self.follower_count=_info['authorFavoriteCount']
      self.score=_info['authorScore']
      self.novels=[]
      for k in _info['novellist']:
        nl = _info['novellist'][k]
        for n in nl:
          if n['novelsize']!='0' and n['maxChapterId']!='0' and n['islock']=='0':
            self.novels.append((n['novelid'],n['novelname']))
        # copystatus=n['copystatus'],tags=n['tags'],locked=n['islock'],word_count=n['novelsize'],updated_at=n['newtopdate'],chpt_count=n['chapterCount']))
  def download_all(self):
    pass

if __name__=='__main__':
  a = Author(2636270)
  print(a.novels)