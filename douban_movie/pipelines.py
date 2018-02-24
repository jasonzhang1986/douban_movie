# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import mysql.connector
from scrapy.exceptions import DropItem


class DoubanMoviePipeline(object):
    def __init__(self):
        self.conn = mysql.connector.connect(user='root', password='password')
        self.cursor = self.conn.cursor()

    def process_item(self, item, spider):
        sql = 'select * from moviedetail where movieid = \'%d\'' % item['movieid']
        print(sql)
        self.cursor.execute(sql)
        values = self.cursor.fetchall()
        if len(values) > 0:
            print("alread exists %d" % item['movieid'])
            raise DropItem("alread exists %d" % item['movieid'])
        sql = r'insert into moviedetail (movieid, tag, title, directors, actors, showtime, length, district, category, star, rate, rate_count, rate5, rate4, rate3, rate2, rate1, cover) values ("%d", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%d", "%s", "%d", "%s", "%s", "%s", "%s", "%s", "%s")' % (
            item['movieid'], item['tag'], item['title'], item['directors'], item['actors'], item['showtime'], item['length'], item['district'], item['category'], item['star'], item['rate'], item['rate_count'], item['rate5'], item['rate4'], item['rate3'], item['rate2'], item['item1'], item['cover'])
        print(sql)
        self.cursor.execute(sql)
        self.conn.commit()
        return item
