# -*- coding: utf-8 -*-
import scrapy,json


class LagouMSpider(scrapy.Spider):
    name = "lagou_m"
    allowed_domains = ["lagou.com"]
    # start_urls = ['http://lagou.com/']

    def __init__(self):
        self.positionName = ["python","java","c","c++","c#","javascript","php","ruby"]
        # self.positionName = "python"
        self.pageNo = 1
        self.url = "https://m.lagou.com/search.json?city=%E5%85%A8%E5%9B%BD&positionName={}&pageNo={}&pageSize=15"
        self.headers={
            "Accept":"application/json",
            "Accept-Encoding":"gzip, deflate, br",
            "Accept-Language":"zh-CN,zh;q=0.8,zh-TW;q=0.6",
            "Connection":"keep-alive",
            "Host":"m.lagou.com",
            "Referer":"https://m.lagou.com/search.html",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36",
            "X-Requested-With":"XMLHttpRequest",
        }

    def start_requests(self):
        for name in self.positionName:
            url = self.url.format(name,self.pageNo)
            yield scrapy.Request(url=url,headers=self.headers,callback=self.parse,meta={'po':name,'no':self.pageNo})

    def parse(self, response):
        data = json.loads(response.text)
        results = data['content']['data']['page']['result']
        # print(data,len(results))
        if len(results) > 0:
            for result in results:
                i = {}
                i['job_name'] = result['positionName']
                i['job_area'] = result['city']
                i['job_price'] = result['salary']
                i['job_company'] = result['companyFullName']
                i['job_company_logo'] = "https://static.lagou.com/"+result['companyLogo']
                i['job_url'] = "https://m.lagou.com/jobs/{}.html".format(result['positionId'])
                i['flag'] = "flag"
                yield i

            po = response.meta.get('po')
            no = response.meta.get('no')
            url = self.url.format(po, str(no+1))
            yield scrapy.Request(url=url, headers=self.headers, callback=self.parse,
                                     meta={'po': po, 'no': no+1})