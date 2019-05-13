# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class LianjiaChengjiaoItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    village_id = scrapy.Field()
    region = scrapy.Field()
    village_name = scrapy.Field()
    room_num = scrapy.Field()
    area = scrapy.Field()
    total_price = scrapy.Field()
    push_time = scrapy.Field()
    total_time = scrapy.Field()
    next_region_name = scrapy.Field()
    forward = scrapy.Field()
    elevator = scrapy.Field()
    url = scrapy.Field()
    unit_price = scrapy.Field()