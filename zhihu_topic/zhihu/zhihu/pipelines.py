# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class ZhihuMongodbPipeline(object):

    def __init__(self):
        client = pymongo.MongoClient(host='localhost', port=27017)
        db = client["zhihu_topic-IT"]
        self.collection = db["question_answer"]

    def process_item(self, item, spider):
        self.collection.insert(item)
        return item
