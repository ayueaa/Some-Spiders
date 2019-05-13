# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BiibiliItem(scrapy.Item):
    aid = scrapy.Field()
    author = scrapy.Field()
    comment = scrapy.Field()
    copyright = scrapy.Field()
    created = scrapy.Field()
    description = scrapy.Field()
    favorites = scrapy.Field()
    is_pay = scrapy.Field()
    length = scrapy.Field()
    mid = scrapy.Field()
    pic = scrapy.Field()
    play = scrapy.Field()
    review = scrapy.Field()
    subtitle = scrapy.Field()
    title = scrapy.Field()
    typeid = scrapy.Field()
    video_review = scrapy.Field()
    pages = scrapy.Field()
    count = scrapy.Field()
