# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from ..items import ImagesItem
class PexelsSpider(scrapy.Spider):
    name = 'pexels'
    allowed_domains = ['pexels.com']
    start_url = 'https://www.pexels.com/search/dark/?page={}'

    def start_requests(self):
        for page in range(3,20):  #定义爬取页数
            url = self.start_url.format(page)
            yield Request(url,self.parse)

    def parse(self, response):
        item = ImagesItem()
        item['image_urls']= response.xpath('//article/a/img/@data-large-src').extract() #650*950图片
        yield item