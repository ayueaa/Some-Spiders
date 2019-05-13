# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MeiweiItem(scrapy.Item):
    shop_id = scrapy.Field()
    shop_name = scrapy.Field()
    branchName = scrapy.Field()
    tLogo = scrapy.Field()
    style = scrapy.Field()
    avgPric = scrapy.Field()
    distance = scrapy.Field()
    address = scrapy.Field()
    latitude = scrapy.Field()
    longitude = scrapy.Field()
