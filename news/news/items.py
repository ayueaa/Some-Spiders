# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class NewsItem(scrapy.Item):

    title = scrapy.Field()
    abstract = scrapy.Field()
    chinese_tag = scrapy.Field()
    comments_count = scrapy.Field()
    behot_time = scrapy.Field()
    source = scrapy.Field()
    source_url = scrapy.Field()
    tag = scrapy.Field()
    label = scrapy.Field()
    group_id = scrapy.Field()
    #hot_comments = scrapy.Field()


