# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanMovieItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    movieid = scrapy.Field()
    tag = scrapy.Field()
    title = scrapy.Field()
    directors = scrapy.Field()
    actors = scrapy.Field()
    showtime = scrapy.Field()
    length = scrapy.Field()
    district = scrapy.Field()
    category = scrapy.Field()
    star = scrapy.Field()
    rate = scrapy.Field()
    rate_count = scrapy.Field()
    rate5 = scrapy.Field()
    rate4 = scrapy.Field()
    rate3 = scrapy.Field()
    rate2 = scrapy.Field()
    rate1 = scrapy.Field()
    cover = scrapy.Field()
