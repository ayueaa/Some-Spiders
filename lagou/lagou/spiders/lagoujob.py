# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.loader import ItemLoader
from ..items import LagouJobItem
from ..items import LagouItem

class LagoujobSpider(CrawlSpider):
    name = 'lagoujob'
    allowed_domains = ['lagou.com']
    start_urls = ['http://lagou.com/','https://xiaoyuan.lagou.com/']

    rules = (
        Rule(LinkExtractor(allow=r'https://www.lagou.com/gongsi/.*'), follow=True),
        Rule(LinkExtractor(allow=r'https://www.lagou.com/zhaopin/.*'),follow=True),
        Rule(LinkExtractor(allow=r'.*?jobs/\d+\.html'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        if response.xpath('//div[@class="job-name"]/span[@class="outline_tag"]'):
            print(response.url, ":该职位已下线")
        else:
            loader = LagouJobItem(item=LagouItem(),response=response)
            loader.add_xpath('title', "//div[@class='job-name']/span[@class='name']/text()")
            loader.add_xpath('salary', "//dd[@class='job_request']/p[1]/span[@class='salary']/text()")
            loader.add_xpath('experience_require', "//dd[@class='job_request']/p[1]/span[3]/text()")
            loader.add_xpath('location', "//dd[@class='job_request']/p[1]/span[2]/text()")
            loader.add_xpath('edu_bg', "//dd[@class='job_request']/p[1]/span[4]/text()")
            loader.add_xpath('full_or_part', "//dd[@class='job_request']/p[1]/span[5]/text()")
            loader.add_xpath('job_tags', "//ul[@class='position-label clearfix']/li/text()")
            loader.add_xpath('push_time', "//p[@class='publish_time']/text()")
            loader.add_xpath('job_advantage', "//dd[@class='job-advantage']/p/text()")
            loader.add_xpath('site', "//dd[@class='job-address clearfix']/div[@class='work_addr']")
            yield loader.load_item()
