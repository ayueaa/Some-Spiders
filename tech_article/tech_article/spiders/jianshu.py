# -*- coding: utf-8 -*-
import scrapy
import re



class JianshuSpider(scrapy.Spider):

    KEYWORD = "python"
    MAX_PAGE = 1
    name = 'jianshu'
    allowed_domains = ['jianshu.com']
    csrf_url = 'https://www.jianshu.com/search?q={}&page=1&type=collection'
    post_url = "https://www.jianshu.com/search/do?q={}&type=collection&page={}&order_by=top"


    def start_requests(self):
        yield scrapy.Request(self.csrf_url.format(self.KEYWORD), callback=self.parse_csrf_token)

    def parse_csrf_token(self, response):
        csrf_token = re.findall(r'.*?csrf-token" content="(.*?)" />', response.text, re.S)[0]
        print(csrf_token)
        data = {
            'x-csrf-token': csrf_token
        }
        for page in range(1, self.MAX_PAGE+1):
            yield scrapy.FormRequest(self.post_url.format(self.KEYWORD, page), formdata=data,
                                     callback=self.parse_page, dont_filter=True)

    def parse_page(self, response):
        print(response.url)