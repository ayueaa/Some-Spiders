# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.pipelines.images import ImagesPipeline
from scrapy import Request


class XiangshuiImagesPipeline(ImagesPipeline):

    def get_media_requests(self, item, info):
        yield Request(item['image_url'], meta={'item':item})

    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        filename = item['ch_name']+".jpg"
        return filename

