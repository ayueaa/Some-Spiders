# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhihuItem(scrapy.Item):

    _id = scrapy.Field()

    title = scrapy.Field()
    topic = scrapy.Field()
    author = scrapy.Field()
    follower_count = scrapy.Field()
    url_token = scrapy.Field()
    user_type = scrapy.Field()
    content = scrapy.Field()
    excerpt = scrapy.Field()
    content_lenth = scrapy.Field()
    create_time = scrapy.Field()
    comment_count = scrapy.Field()
    voteup_count = scrapy.Field()
