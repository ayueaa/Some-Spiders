# -*- coding: utf-8 -*-
"""
该spider基于boss直聘网全站爬取（暂未添加公司入口）
"""
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import BossItem
from..items import BossItemLoader


class ZhipinSpider(CrawlSpider):
    name = 'zhipin'
    allowed_domains = ['zhipin.com']
    start_urls = ['http://zhipin.com/']  #,未添加公司接口'https://www.zhipin.com/gongsi'

    rules = (
        Rule(LinkExtractor(allow=r'/c\w+-p\w+/', restrict_xpaths="//div[@id='main']//div[@class='job-menu xh-highlight']"), follow=False),
        #Rule(LinkExtractor(allow=r'/gongsi/.*\.html'), follow=False), 未添加公司接口
        Rule(LinkExtractor(allow=r'/job_detail/.*\.html'), callback='parse_item', follow=True),
        Rule(LinkExtractor(restrict_xpaths="//div[@class='page']/a[@ka='page-next']"), follow=True)
    )

    def parse_item(self, response):
        l = BossItemLoader(item=BossItem(), response=response)
        l.add_xpath('job_status', "//div[@class='info-primary']/div[1]/text()")
        l.add_xpath('name', "//div[@class='info-primary']/div[@class='name']/h1/text()")
        l.add_xpath('salary', "//div[@class='company-info']/div[1]/span/text()")
        l.add_xpath('detail_location', "//div[@class='location-address']/text()")
        l.add_xpath('location', "//div[@class='info-primary']/p/text()[1]")
        l.add_xpath('experience', "//div[@class='info-primary']/p/text()[2]")
        l.add_xpath('education', "//div[@class='info-primary']/p/text()[3]")
        l.add_xpath("tags", "//div[@class='job-tags']/span//text()")
        l.add_xpath("company", "//div[@class='detail-content']//div[@class='name']/text()")
        l.add_xpath("start_money", "//div[@class='level-list']/li[2]/text()")
        l.add_xpath("start_time", "//div[@class='level-list']/li[3]/text()")
        l.add_xpath("require", "//div[@class='job-sec']/div[1]//text()")
        l.add_value("url", response.url)
        yield l.load_item()

