# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class  Ganji2Spider(CrawlSpider):
    name = 'ganji_2'
    allowed_domains = ['ganji.com']
    start_urls = ['https://cn.58.com/ershouche/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths='//div[@class="info_list"]/ul'), callback='parse_item'),
    )

    def parse_item(self, response):
        i = {}
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
