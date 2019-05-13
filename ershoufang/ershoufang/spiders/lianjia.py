# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from..items import ErshoufangItem

class LianjiaSpider(CrawlSpider):
    name = 'lianjia'
    allowed_domains = ['cd.lianjia.com']
    start_urls = ['https://cd.lianjia.com/ershoufang/']
    rules = (
        Rule(LinkExtractor(allow=r'cd\.lianjia\.com/ershoufang/\d+\.html'), callback='parse_item'),
        Rule(LinkExtractor(allow=r'ershoufang/\w+/[pg\d+]?$'), follow=True),
        # Rule(LinkExtractor(allow=r'ditiefang/\w+/[pg\d+]?$'), follow=True),   #地铁房筛选
        Rule(LinkExtractor(allow=r'ershoufang/pg\d+/$'), follow=True)  #页码链接

    )

    def parse_item(self, response):
        item =ErshoufangItem()
        item["url"] = response.url
        item["source"] = "LianJia"
        yield item