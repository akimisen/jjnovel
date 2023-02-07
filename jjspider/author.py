from scrapy import CrawlSpider, Request

class AuthorSpider(CrawlSpider):
  name='author'
  def start_requests(self):

    return super().start_requests()


  def parse(self, response, **kwargs):
    return super().parse(response, **kwargs)
  pass