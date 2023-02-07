import scrapy

class Author(scrapy.Item):
  url=scrapy.Field()
  id=scrapy.Field()
  name=scrapy.Field()
  score=scrapy.Field()
  novels=scrapy.Field()
  flw_count=scrapy.Field()


class Novel(scrapy.Item):
  url=scrapy.Field()
  id=scrapy.Field()
  title=scrapy.Field()
  aid=scrapy.Field()
  author=scrapy.Field()
  intro=scrapy.Field()
  genre=scrapy.Field()
  xx=scrapy.Field()
  tags=scrapy.Field()
  is_signed=scrapy.Field()
  is_vip=scrapy.Field()
  is_locked=scrapy.Field()
  word_count=scrapy.Field()
  created_at=scrapy.Field()
  updated_at=scrapy.Field()
  chpt_count=scrapy.Field()
  score=scrapy.Field()
  flw_count=scrapy.Field()
  style=scrapy.Field()
  ranking=scrapy.Field()
  avg_click=scrapy.Field()
  rating=scrapy.Field()
  copystatus=scrapy.Field()
  comment_count=scrapy.Field()

class Novel(scrapy.Item):
  pass