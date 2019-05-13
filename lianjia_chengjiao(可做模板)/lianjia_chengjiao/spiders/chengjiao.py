# -*- coding: utf-8 -*-
import scrapy
import re
import datetime
from ..items import LianjiaChengjiaoItem

class ChengjiaoSpider(scrapy.Spider):
    name = 'chengjiao'
    allowed_domains = ['cd.lianjia.com']
    start_url = "https://cd.lianjia.com/xiaoqu/"
    #分小区页面
    next_region_url = "https://cd.lianjia.com{}pg{}/"
    #已售房源页面
    solded_url = "https://cd.lianjia.com/chengjiao/pg{}c{}/"


    def start_requests(self):
        yield scrapy.Request(self.start_url,callback=self.parse)


    #解析获取主地区链接,如锦江区\成华区
    def parse(self, response):
        regions = response.xpath("//div[@data-role='ershoufang']/div/a/@href").extract()
        for region in regions:
            region_url = "https://cd.lianjia.com" + region
            yield scrapy.Request(region_url, callback=self.parse_region)

    #解析获取分地区链接,如川大\红牌楼
    def parse_region(self, response):
        next_regions = response.xpath("//div[@data-role='ershoufang']/div[2]/a/@href").extract()
        for next_region in next_regions:
            yield scrapy.Request(self.next_region_url.format(next_region, 1), meta={"page": 1,"next_region":next_region}, callback=self.parse_next_region)

    #解析获取分地区下的小区链接,如川大花园小区
    def parse_next_region(self, response):
        #当前页
        page = int(response.meta.get("page"))
        next_region = response.meta.get("next_region")
        next_region_name = response.meta.get("next_region_name")
        items = response.xpath("//ul[@class='listContent']/li")
        for item in items:
            #获取小区id
            village_id = item.xpath("./@data-id").extract_first()
            # 获取小区主地区
            region = item.xpath(".//a[@class='district']/text()").extract_first().strip()
            # 获取小区分地区
            next_region_name = item.xpath(".//a[@class='bizcircle']/text()").extract_first().strip()
            yield scrapy.Request(self.solded_url.format(1, village_id), callback=self.parse_solded_page,
                                 meta={"village_id": village_id, "region": region, "next_region": next_region,"page": 1, "next_region_name":next_region_name})
        # total为小区总数
        total = response.xpath("//div[@class='resultDes clear']/h2[@class='total fl']/span/text()").extract_first().strip()
        # 平均页数,需转换为整数页
        ave_page = int(total)/30
        if page < ave_page:
            page += 1
            yield scrapy.Request(self.next_region_url.format(next_region, page), callback=self.parse_next_region,
                                 meta={"page": page, "next_region": next_region})


    #解析小区已售房源信息
    def parse_solded_page(self, response):
        page = int(response.meta.get("page"))
        village_id = response.meta.get("village_id")
        region = response.meta.get("region")
        next_region_name = response.meta.get("next_region_name")
        next_region = response.meta.get("next_region")
        total_num = int(response.xpath("//div[@class='total fl']/span/text()").extract_first().strip())
        if total_num != 0:
            items = response.xpath("//ul[@class='listContent']/li")
            for item in items:
                i = LianjiaChengjiaoItem()
                title = item.xpath(".//div[@class='title']/a/text()").extract_first()
                if "车位" not in title:
                    village_name = title.split(" ")[0]
                    room_num = title.split(" ")[1]
                    area = title.split(" ")[2]
                    price_info = item.xpath(".//div[@class='totalPrice']/span/text()").extract_first()
                    if "*" in price_info:
                        total_price = item.xpath(".//span[@class='dealCycleTxt']/span[1]/text()").extract_first().split("牌")[1].split("万")[0]
                        push_time = str(datetime.date.today())
                    else:
                        total_price = price_info.split("万")[0].strip()
                        push_time =response.xpath(".//div[@class='dealDate']/text()").extract_first().replace(".", "-")

                    try:
                        total_time = item.xpath(".//span[@class='dealCycleTxt']/span[2]/text()").extract_first()
                        i['total_time'] = int(total_time.split("期")[1].split("天")[0])
                    except:
                        total_time = item.xpath(".//span[@class='dealCycleTxt']/span/text()").extract_first()
                        i['total_time'] = int(total_time.split("期")[1].split("天")[0])
                    house_info = item.xpath(".//div[@class='houseInfo']/text()").extract_first()
                    i['village_id'] = village_id
                    i['region'] = region
                    i['next_region_name'] = next_region_name
                    i['village_name'] = village_name
                    i['room_num'] = room_num
                    i['area'] = float(area.split("平")[0])
                    i['total_price'] = int(float(total_price)*10000)
                    i['push_time'] = push_time
                    i["forward"] = house_info.split("|")[0].strip()
                    i["elevator"] = house_info.split("|")[-1].strip()
                    i["url"] = response.url
                    i["unit_price"] = int((float(total_price)*10000)/(float(area.split("平")[0])))
                    yield i

            ave_page = total_num/30
            if page < ave_page:
                page += 1
                yield scrapy.Request(self.solded_url.format(page, village_id), callback=self.parse_solded_page,
                                     meta={"village_id": village_id, "region": region, "next_region": next_region,"page": page,'next_region_name':next_region_name})