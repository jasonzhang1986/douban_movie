from scrapy.spiders import CrawlSpider
class Douban(CrawlSpider):
    name = "douban"
    start_urls = ['http://movie.douban.com/top250']
    def parse(self,response):
        print (response.body)