# -*- coding: utf-8 -*-
import scrapy
import json
from..items import MeiweiItem

class NowaitSpider(scrapy.Spider):
    name = 'nowait'
    allowed_domains = []
    url = 'https://capi.mwee.cn/app-api/h5/shop/hotqueuelist'
    cityid = 1
    page = 1
    formdata = {
        'cityid': "%s" % cityid,
        'data[ordersortids]': '20',
        'data[pagesize]': '20',
        'data[page]': "%s" % page,
        'fromw': '1',
    }
    num =0
    def start_requests(self):

        yield scrapy.FormRequest(url=self.url, formdata=self.formdata, callback=self.parse,meta={"page":self.page,"cityid":self.cityid})

    def parse(self, response):
        page = response.meta.get("page")
        cityid = response.meta.get("cityid")
        formdata = {
            'cityid': "%s" % cityid,
            'data[ordersortids]': '20',
            'data[pagesize]': '20',
            'data[page]': "%s" % page,
            'fromw': '1',
        }
        res = json.loads(response.text)
        total = res.get("data").get("total")

        items = res.get("data").get("shops")
        for i in items:
            self.num += 1
            print("——————————————————当前城市应有总数:", total, '—————————————————')
            print("——————————————————当前采集总数:", self.num,"——————————————————")
            print("——————————————————该城市当前采集页码:", page, '—————————————————')
            print("——————————————————当前城市代码:", cityid, '—————————————————')

            item = MeiweiItem()
            item['shop_id'] = i.get("shopId")
            item['shop_name'] = i.get("shopName")
            item ['branchName'] = i.get("branchName")
            item['tLogo'] = i.get("tLogo")
            item['style'] = i.get("styleCooking")
            item['avgPric'] = i.get("avgPric")
            item['distance'] = i.get("distance")
            item['address'] = i.get("address")
            item['latitude'] = i.get("latitude")
            item['longitude'] = i.get("longitude")
            yield item
        if page < int(total)/20:
            page += 1

            yield scrapy.FormRequest(url=self.url, formdata=formdata, callback=self.parse,dont_filter=True,meta={"page":page,"cityid":cityid})
        else:
            page =1
            cityid += 1
            yield scrapy.FormRequest(url=self.url, formdata=formdata, callback=self.parse,dont_filter=True,meta={"page":page,"cityid":cityid})

