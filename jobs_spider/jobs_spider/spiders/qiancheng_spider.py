# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class QianchengSpiderSpider(CrawlSpider):
    name = 'qiancheng_spider'
    allowed_domains = ['51job.com']
    start_urls = ['http://search.51job.com/list/010000,000000,0000,00,9,99,python,2,1.html']

    rules = (
        Rule(LinkExtractor(allow=r'http://jobs\.51job\.com/beijing.*/\d+\.html.*'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = {}
        i['job_name'] = response.xpath('.//div[@class="cn"]/h1/@title').extract_first()
        i['job_area'] = response.xpath('.//div[@class="cn"]/span[@class="lname"]/text()').extract_first()
        i['job_price'] = response.xpath('.//div[@class="cn"]/strong/text()').extract_first()
        i['job_company'] = response.xpath('.//div[@class="cn"]/p[@class="cname"]/a/@title').extract_first()
        i['job_company_abstract'] = response.xpath('.//div[@class="cn"]/p[@class="msg ltype"]/text()').extract_first()
        i['job_url'] = response.url
        i['flag'] = "前程无忧"
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        # print(i)
        return i
