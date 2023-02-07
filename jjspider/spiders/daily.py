import scrapy

class DailySpider(scrapy.Spider):
  #千字金榜

  def start_requests(self):
    urls=[
      'http://android.jjwxc.net/bookstore/favObservationByDate?versionCode=277&day='
    ]
    return [scrapy.Request(url=url, callback=self.parse) for url in urls]

  def parse(self, response, **kwargs):
    url = response.url
    title = response.css('h1::text').extract_first()
    print('URL is: {}'.format(url))
    print('Title is: {}'.format(title))