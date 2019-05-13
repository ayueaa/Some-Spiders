# -*- coding: utf-8 -*-
import scrapy
from ..items import XiangshuiItem
class NosetimeSpider(scrapy.Spider):
    name = 'nosetime'
    allowed_domains = ['nosetime.com']
    start_urls = ['https://www.nosetime.com/top200.php?type=trade', 'https://www.nosetime.com/top200.php?type=salon']

    def parse(self, response):
        items = response.xpath('//div[@id="top"]/ul//li')
        for i in items:
            item = XiangshuiItem()
            item['top_num'] = i.xpath('.//div[@class="topnum"]/span/text()').extract_first()
            item['ch_name'] = i.xpath('.//h2/a/text()[1]').extract_first()
            item['en_name'] = i.xpath('.//h2/a/text()[2]').extract_first()
            item['score'] = i.xpath('.//div[@class="score"]/span[2]/text()').extract_first().split("分")[0]
            item['score_num'] = i.xpath('.//div[@class="score"]/span[2]/text()').extract_first().split("分")[1]
            item['brand'] = i.xpath('.//div[@class="intro"]/a[1]/text()').extract_first()
            item['perfumer'] = i.xpath('.//div[@class="intro"]/a[2]/text()').extract_first()
            item['attributes'] = i.xpath('.//div[@class="intro"]/a[3]/text()').extract_first()
            item['fragrance'] = i.xpath('.//div[@class="intro"]/a[4]/text()').extract_first()
            item['top_note'] = " ".join(set(i.xpath('.//div[@class="div1"]//text()').extract()))
            item['middle_note'] = " ".join(set(i.xpath('.//div[@class="div2"]//text()').extract()))
            item['after_note'] = " ".join(set(i.xpath('.//div[@class="div3"]//text()').extract()))
            item['image_url'] = i.xpath(''
                                        ''
                                        './/a[@class="imgsize"]/img/@src').extract_first()
            item['comment'] = i.xpath('.//p[@class="comment-txt"]/text()').extract_first()
            yield item
        next_url = response.xpath('//div[@class="next_news"]/a[contains(.,"下一页")]/@href').extract_first()
        if next_url is not None:
            yield response.follow(next_url, self.parse)