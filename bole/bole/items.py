# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BoleItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    date_time = scrapy.Field()
    kind = scrapy.Field()
    collect = scrapy.Field()
    image_urls = scrapy.Field()
