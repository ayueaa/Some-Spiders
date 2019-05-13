# -*- coding: utf-8 -*-
import scrapy
from scrapy_redis.spiders import RedisSpider

class Text2Spider(scrapy.Spider):
    name = 'text2'
    allowed_domains = ['text.com']
    start_urls = ['http://text.com/']

    def parse(self, response):
        pass