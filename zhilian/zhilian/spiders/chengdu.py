# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import ZhilianItem


class ChengduSpider(scrapy.Spider):
    name = 'chengdu'
    allowed_domains = ['zhaopin.com']
    start_urls = ['https://www.zhaopin.com/chengdu/']

    cd_url = 'https://fe-api.zhaopin.com/c/i/sou?start={}&pageSize=90&cityId=801&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kw={}&kt=3'
    def parse(self, response):
        job = response.xpath("//ol/li[1]//div[@class='zp-jobNavigater__pop--list']/a/text()").extract()
        start = 0
        for kw in job:
            new_url = self.cd_url.format(start, kw)
            yield scrapy.Request(new_url, callback=self.parse_page, meta={'start': start,'kw': kw})

    def parse_page(self, response):
        start = response.meta.get("start")
        kw = response.meta.get("kw")

        res = json.loads(response.text).get("data").get("results")
        total = json.loads(response.text).get("data").get("numTotal")
        for i in res:
            item = ZhilianItem()
            item["job_name"] = i.get("jobName")
            salary = i.get("salary").replace("K", "000")
            try:
                average_salary = int((int(salary.split("-")[0]) + int(salary.split("-")[1]))/2)
                low_salary = int(salary.split("-")[0])
                high_salary = int(salary.split("-")[1])
            except:
                average_salary = None
            item["average_salary"] = average_salary
            item["city"] = i.get("city").get("display")
            item["area"] = i.get("businessArea")
            item["type"] = i.get("emplType")
            item["edu"] = i.get("eduLevel").get("name")
            item["jobTag"] = i.get("jobTag").get("searchTag")
            item["url"] = i.get("positionURL")
            item["update_time"] = i.get("updateDate")
            item["experience"] = i.get("workingExp").get("name")
            item["low_salary"] = low_salary
            item["high_salary"] = high_salary
            yield item

        start+=len(res)
        if start < total:
            yield scrapy.Request(self.cd_url.format(start, kw), meta={"start": start, "kw": kw}, callback=self.parse_page, dont_filter=True)
