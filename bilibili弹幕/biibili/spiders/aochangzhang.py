# -*- coding: utf-8 -*-
import scrapy
import json
from biibili.items import BiibiliItem

class AochangzhangSpider(scrapy.Spider):
    name = 'aochangzhang'
    allowed_domains = []
    start_urls = 'https://space.bilibili.com/ajax/member/getSubmitVideos?mid=122879&pagesize=30&tid=0&page={}&keyword=&order=pubdate'

    def start_requests(self):
        page = 1
        yield scrapy.Request(self.start_urls.format(page), meta={"page": 1}, callback=self.parse)

    def parse(self, response):
        current_page = response.meta.get("page")

        results = json.loads(response.text)
        pages = results.get("data").get("pages")
        count = results.get("data").get("count")
        vlist = results.get("data").get("vlist")
        for video in vlist:
            item = BiibiliItem()
            item['aid'] = video.get("aid")
            item['author'] = video.get("author")
            item['comment'] = video.get("comment")
            item['copyright'] = video.get("copyright")
            item['created'] = video.get("created")
            item['description'] = video.get("description")
            item['favorites'] = video.get("favorites")
            item['is_pay'] = video.get("is_pay")
            item['length'] = video.get("length")
            item['mid'] = video.get("mid")
            item['pic'] = video.get("pic")
            item['play'] = video.get("play")
            item['review'] = video.get("review")
            item['subtitle'] = video.get("subtitle")
            item['title'] = video.get("title")
            item['typeid'] = video.get("typeid")
            item['video_review'] = video.get("video_review")
            item["pages"] = pages
            item["count"] = count
            yield item
        if current_page <= int(pages):
            current_page += 1
            yield scrapy.Request(self.start_urls.format(current_page), callback=self.parse,
                                 dont_filter=True, meta={"page": current_page})
