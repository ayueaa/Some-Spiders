# -*- coding: utf-8 -*-
import scrapy
from bole.items import BoleItem

class ArticleSpider(scrapy.Spider):

    name = 'article'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        post_nodes = response.xpath('//div[@id="archive"]/div[@class="post floated-thumb"]//a')
        for post_node in post_nodes:
            img_url = post_node.xpath('./img/@src').extract_first()
            post_url = post_node.xpath('./@href').extract_first()
            yield scrapy.Request(url=post_url, meta={'front_image_url': img_url}, callback=self.parse_2)
        # next_url = response.xpath('//a[@class="next page-numbers"]/@href').extract_first() 注释为另一种实现方式
        next_url = response.xpath('//a[@class="next page-numbers"]/@href') #后面使用follw 可不提取具体连接，follow会自动提取
        if next_url:
            # yield scrapy.Request(url=next_url,callback=self.parse)
            for a in next_url:
                yield response.follow(a, callback=self.parse)


    def parse_2(self, response):

        item = BoleItem()
        item["title"] = response.xpath('//div[@class="entry-header"]/h1/text()').extract_first()
        item["date_time"] = response.xpath('//div[@class="entry-meta"]/p/text()').extract_first().strip()
        item["kind"] = response.xpath('//div[@class="entry-meta"]/p/a[1]/text()').extract_first()
        item["collect"] = response.xpath('//div[@class="post-adds"]/span[2]/text()').extract_first().strip().split('收')[0]
        item["image_urls"] = [response.meta['front_image_url']]
        yield item
