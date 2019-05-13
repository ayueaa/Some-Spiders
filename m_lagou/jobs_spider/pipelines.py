# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

class JobsSpiderPipeline(object):

    def __init__(self):
        client = pymongo.MongoClient('localhost',27017)
        scrapy_db = client['scrapy_db']
        self.coll = scrapy_db['job_scrapy']

    def process_item(self, item, spider):
        self.coll.insert_one(item)
        return item

"""
sqlite:小型关系型数据库
    sql语句：专门用于关系型数据库的语言
    sqlalchemy：Python库，实现ORM

关系型数据库【固定表格字段】：
    sqlite【小型】
    mysql【中型】
    sql server【中型】
    oracle【大型】
非关系型数据库【不固定字段】：基于json格式数据，灵活、IO快
    redis：常用于缓存汇总
    mongodb
"""