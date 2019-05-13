# -*- coding: utf-8 -*-
import scrapy
import re
from ..items import XiaozhuItem
from ..items import XiaoZhuItemLoader
class DuanzuSpider(scrapy.Spider):
    name = 'duanzu'
    allowed_domains = ['xiaozhu.com']
    start_urls = ['http://jci.xiaozhustatic1.com/e19022701/xzjs?k=Front_Index&httphost=www.xiaozhu.com']
    city_url = "http://{}.xiaozhu.com/"
    handle_httpstatus_list = [403,307]

    def parse(self, response):
        res = response.text
        result = re.findall(r"\bcitys\[\d+\]=new Array\('(\w+)','", res, re.S)  # 至匹配了国内城市，如需包括国外，去掉边界匹配符\b
        for city in result:
            yield scrapy.Request(self.city_url.format(city),callback=self.parse_city_page)

    def parse_city_page(self, response):
        if response.status == 307:
            s = input("请检查网页，完成验证")
            print(s)
        items = response.xpath("//div[@id='page_list']/ul//li/a")
        for item in items:
            info_url = item.xpath("./@href").extract_first()
            yield scrapy.Request(info_url,callback=self.parse_info)
        next_page = response.xpath("//div[@class='pagination_v2 pb0_vou']/a[contains(.,'>')]/@href").extract_first()
        if next_page:
            yield scrapy.Request(next_page, callback=self.parse_city_page)


    def parse_info(self,response):
        if response.status == 307:
            s = input("请检查网页，完成验证")
            print(s)
        l = XiaoZhuItemLoader(item=XiaozhuItem(), response=response)
        l.add_xpath("title", "//div[@class='pho_info']/h4/em/text()")
        l.add_xpath("location", "//div[@class='pho_info']/p/em/a[2]/text()")
        l.add_xpath("address", "//div[@class='pho_info']/p/span/text()")
        l.add_xpath("price", "//div[@class='day_l']/span/text()")
        l.add_xpath("owner", "//div[@class='w_240']/h6/a/@title")
        l.add_xpath("rent_mode", "//li[@class='border_none']/h6/text()")
        l.add_xpath("area", "//li[@class='border_none']/p/text()[1]")
        l.add_xpath("room_num", "//li[@class='border_none']/p/text()[22]")
        l.add_xpath("bed_num", "//li/h6[@class='h_ico3']/text()")
        l.add_xpath("person_visible", "//li/h6[@class='h_ico2']/text()")
        l.add_xpath("room_info", "//div[@class=' intro_item_content']/p//text()")
        l.add_xpath("traffic_info", "//div[@class=' intro_item_content']/p//text()")
        l.add_xpath("comment_num", "//ul[@class='dp_tab']/li[@id='thisroom']/text()")
        l.add_xpath("comment_star", "//span[@class='x_textscore']/text()")
        yield l.load_item()





