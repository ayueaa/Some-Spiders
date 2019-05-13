# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.pipelines.images import ImagesPipeline

class XiangshuiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    top_num = scrapy.Field()
    ch_name = scrapy.Field()
    en_name = scrapy.Field()
    score = scrapy.Field()
    score_num = scrapy.Field()
    brand = scrapy.Field()
    perfumer = scrapy.Field()
    attributes = scrapy.Field()
    fragrance = scrapy.Field()
    top_note = scrapy.Field()
    middle_note = scrapy.Field()
    after_note = scrapy.Field()
    image_url = scrapy.Field()
    images = scrapy.Field()
    comment = scrapy.Field()

