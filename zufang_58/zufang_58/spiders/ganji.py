# -*- coding: utf-8 -*-
import scrapy
from zufang_58.items import Zufang58Item

class GanjiSpider(scrapy.Spider):
    name = 'ganji'
    allowed_domains = ['bj.ganji.com']
    start_urls = ['http://bj.ganji.com/zufang/']
    new_url="http://bj.ganji.com/zufang/{}x.shtml"
    def parse(self, response):
        item = Zufang58Item()
        items = response.xpath("//div[contains(@class,'ershoufang-list')]")
        for i in items:
            item["title"] = i.xpath(".//dd[1]/a/text()").extract_first()
            item["price"] = i.xpath(".//dd[6]/div[@class='price']//span[1]/text()").extract_first()
            url_num = i.xpath(".//dd/a/@gjalog_fang").extract_first().split("=")[1]
            item["url"] = "http://bj.ganji.com/zufang/{}x.shtml".format(url_num)
            yield item
        next_url = response.xpath("//div[@class='pageBox']/a[@class='next']/@href").extract_first()
        yield scrapy.Request(url=next_url,callback=self.parse)