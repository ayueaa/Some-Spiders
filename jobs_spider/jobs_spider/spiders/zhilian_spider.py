# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class ZhilianSpiderSpider(CrawlSpider):
    name = 'zhilian_spider'
    allowed_domains = ['zhaopin.com']
    start_urls = ['http://sou.zhaopin.com/jobs/searchresult.ashx?jl=%E5%8C%97%E4%BA%AC&kw=python&sm=0&p=1']

    rules = (
        Rule(LinkExtractor(allow=r'http://jobs\.zhaopin\.com/.*\.htm'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        i = {}
        i['job_name'] = response.xpath('.//div[@class="fixed-inner-box"]/div[@class="inner-left fl"]/h1/text()').extract_first()
        i['job_area'] = "".join(response.xpath('.//ul[@class="terminal-ul clearfix"]/li/span[contains(text(),"工作地点：")]/../strong//text()').extract())
        i['job_price'] = response.xpath('.//ul[@class="terminal-ul clearfix"]/li/span[contains(text(),"职位月薪：")]/../strong/text()').extract_first()
        i['job_company'] = response.xpath('.//div[@class="fixed-inner-box"]/div[@class="inner-left fl"]/h2/a/text()').extract_first()
        i['job_company_abstract'] = "  ".join(response.xpath('.//div[@class="fixed-inner-box"]/div[@class="inner-left fl"]/div[@class="welfare-tab-box"]//span/text()').extract())
        i['job_abstract'] = response.xpath('.//div[@class="terminalpage-main clearfix"]/div[@class="tab-cont-box"]/div[@class="tab-inner-cont"]//text()').extract()
        i['job_url'] = response.url
        i['flag'] = "智联招聘"
        print(i)
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        return i
