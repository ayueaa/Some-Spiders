# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import NewsItem
import time
import re


class ToutiaoSpider(scrapy.Spider):
    name = 'toutiao'
    allowed_domains = []
    classes = ["news_hot", "news_tech", "news_entertainment", "news_game", "news_sports", "news_car", "news_finance", "news_military", "news_world", "news_fashion", "news_travel", "news_discovery" ]
    comment_api = "https://www.toutiao.com/api/comment/list/?group_id={}&item_id={}&offset=0&count=5"
    base_url = "https://www.toutiao.com/api/pc/feed/?category={}&utm_source=toutiao&widen=1&max_behot_time={}&max_behot_time_tmp={}&tadrequire=true"

    def start_requests(self):
        start_urls = [self.base_url.format(i, 0, 0) for i in self.classes]
        print(start_urls)
        for url in start_urls:
            kw = re.findall(r"\?category=(.*?)&", url)[0]
            yield scrapy.Request(url, callback=self.parse, dont_filter=True, meta={"kw": kw})

    def parse(self, response):
        kw = response.meta.get("kw")
        print(kw)
        result = json.loads(response.text)
        try:
            next_time = result.get("next").get("max_behot_time")
            print(next_time)
            max_behot_time = max_behot_time_tmp = next_time
            data = result.get("data")
            for i in data:
                item = NewsItem()
                item["title"] = i.get("title")
                item["abstract"] = i.get("abstract")
                item["chinese_tag"] = i.get("chinese_tag")
                item["comments_count"] = i.get("comments_count")
                _time = time.localtime(i.get("behot_tim"))
                item["behot_time"] = time.strftime("%Y-%m-%d %H:%M:%S", _time)
                item["source"] = i.get("source")
                source_url = "https://www.toutiao.com"+i.get("source_url")
                item["source_url"] = source_url
                item["tag"] = i.get("tag")
                item["label"] = ",".join(i.get("label"))
                group_id = i.get("group_id")
                item["group_id"] = group_id
                #yield scrapy.Request(url=self.comment_api.format(group_id,group_id),callback=self.parse_commnet)
                yield item
            if next_time != 0:
                yield scrapy.Request(self.base_url.format(kw, max_behot_time, max_behot_time_tmp), callback=self.parse,
                                     meta={"kw": kw}, dont_filter=True)
        except:
            pass
    # def parse_commnet(self,response):
    #     item = NewsItem()
    #     result = json.loads(response.text).get("data").get("comments")
    #     item["hot_comments"] = result
    #     yield item





