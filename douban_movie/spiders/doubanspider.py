from scrapy.spiders import CrawlSpider
from scrapy.http import Request
import mysql.connector
from bs4 import BeautifulSoup
import re
import os
import random
import pickle
from douban_movie.items import DoubanMovieItem
from scrapy.conf import settings


class Douban(CrawlSpider):
    name = "douban"
    index = 0
    count = 0
    start_urls = []
    movie = None

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        self.count = self.getMovieCount()
        self.index = self.load_db_lineNo()
        self.get_movie_from_db()
        print(self.movie)
        if self.movie:
            url = 'https://movie.douban.com/subject/%d/' % self.movie[0]
            self.start_urls.append(url)

    def load_db_lineNo(self):
        d = {'lineNo': 0}
        try:
            with open(os.path.join(os.getcwd(), 'lineNo.txt'), 'rb') as f:
                d = pickle.load(f)
        except Exception as e:
            print(e)
        return d['lineNo']

    def save_db_lineNo(self, lineNo):
        a = {'lineNo': lineNo}
        with open('lineNo.txt', 'wb') as f:
            pickle.dump(a, f)

    def getMovieCount(self):
        conn = mysql.connector.connect(user='root', password='password')
        cursor = conn.cursor()
        cursor.execute('USE douban')

        sql = r'select count(*) from movielist'
        print(sql)
        cursor.execute(sql)
        result = cursor.fetchone()
        conn.commit()
        conn.close()
        return result[0]

    def get_movie_from_db(self):
        self.movie = None
        conn = mysql.connector.connect(user='root', password='password')
        cursor = conn.cursor()
        cursor.execute('USE douban')

        sql = r'select * from movielist limit %d,1' % self.index
        print(sql)
        cursor.execute(sql)
        self.movie = cursor.fetchone()
        conn.commit()
        conn.close()
        self.index += 1

    def parse(self,response):
        print(response.body)
        self.parse_content(response)
        self.save_db_lineNo(self.index)
        if self.index < self.count:
            self.get_movie_from_db()
            if self.movie:
                url = 'https://movie.douban.com/subject/%d/' % self.movie[0]
                print('url = %s' % url)
                yield Request(url, callback=self.parse, headers={'User-Agent': random.choice(settings.get('USER_AGENTS'))})

    def parse_content(self, response):
        movieid = self.movie[0]
        tag = self.movie[1]
        title = self.movie[2]
        director = self.movie[3]
        actor = self.movie[4]
        rate = self.movie[5]
        star = self.movie[6]
        cover = self.movie[7]
        html = BeautifulSoup(response.body, 'lxml')
        info = html.select('#info')
        if len(info) == 0:
            print(response.text)
            return [-2]
        info = html.select('#info')[0].get_text().split('\n')
        print(info)
        # print(len(info))
        category = ''
        district = ''
        showtime = ''
        length = ''
        for item in info:
            item = item.split(':')
            if item[0] == '类型':
                category = item[-1].strip()
            elif item[0] == '制片国家/地区':
                district = item[-1].strip()
            elif item[0] == '上映日期':
                showtime = item[-1].strip().split('-')[0]
            elif item[0] == '片长':
                length = item[-1].strip()
                length = re.findall('\d+', length)[0]

        category = category.replace(r'/', ',')
        if len(district) > 0:
            district = district[:50]

        if len(category) > 0:
            category = category[:30]
        rate_count = html.select(
            '#interest_sectl > div.rating_wrap.clearbox > div.rating_self.clearfix > div > div.rating_sum > a > span')[
            0].get_text()

        # interest_sectl > div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-child(1) > span.rating_per
        rate5 = html.select(
            '#interest_sectl > div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-of-type(1) > span.rating_per')[
            0].get_text().split('%')[0]
        rate4 = html.select(
            '#interest_sectl > div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-of-type(2) > span.rating_per')[
            0].get_text().split('%')[0]
        rate3 = html.select(
            '#interest_sectl > div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-of-type(3) > span.rating_per')[
            0].get_text().split('%')[0]
        rate2 = html.select(
            '#interest_sectl > div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-of-type(4) > span.rating_per')[
            0].get_text().split('%')[0]
        rate1 = html.select(
            '#interest_sectl > div.rating_wrap.clearbox > div.ratings-on-weight > div:nth-of-type(5) > span.rating_per')[
            0].get_text().split('%')[0]

        item = DoubanMovieItem()
        item['movieid'] = movieid
        item['title'] = title
        item['tag'] = tag
        item['directors'] = director
        item['actors'] = actor
        item['showtime'] = showtime
        item['length'] = length
        item['district'] = district
        item['category'] = category
        item['star'] = star
        item['rate'] = rate
        item['rate_count'] = rate_count
        item['rate5'] = rate5
        item['rate4'] = rate4
        item['rate3'] = rate3
        item['rate2'] = rate2
        item['rate1'] = rate1
        item['cover'] = cover
        print('###### ')
        print(item)
        print('######')
