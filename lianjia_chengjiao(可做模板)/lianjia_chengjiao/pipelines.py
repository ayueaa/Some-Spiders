# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import pymongo
from scrapy.exceptions import DropItem


class MongoPipeline(object):
    collection_name = 'lianjia_solded'   #定义分表名字，勿漏
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mogo_db = mongo_db
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DB')
        )
    def open_spider(self,spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mogo_db]

    def process_item(self,item,spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item

    def close_spider(self,spider):
        self.client.close()
    #关闭了url去重
# class DuplicatesPipleline(object):
#     def __init__(self):
#         self.ids_seen = set()
#
#     def process_item(self,item,spider):
#         if item['url'] in self.ids_seen:
#             raise DropItem('Duplicate item found: %s' % item)
#         else:
#             self.ids_seen.add(item['url'])
#             return item
