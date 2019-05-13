# -*- coding: utf-8 -*-
import scrapy


class TaskSpider(scrapy.Spider):
    name = 'task'
    allowed_domains = ['task.com']
    start_urls = ['http://task.com/']

    def parse(self, response):
        pass
