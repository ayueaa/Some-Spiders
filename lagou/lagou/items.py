# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import Join,TakeFirst,Compose,MapCompose
from scrapy.loader import ItemLoader
from w3lib.html import remove_tags

class LagouJobItem(ItemLoader):
    default_output_processor = TakeFirst()

def remove_splash(value):
    return value.replace('/' ,'').replace(' ' ,"").replace('\n' ,"")

def remove_other(value):
    return value.replace('查看地图', '')

def remove_blank(value):
    return value.split(" ")[0].strip()

def handle_attr(value):
    return remove_tags(value)

class LagouItem(scrapy.Item):
    title = scrapy.Field()
    salary = scrapy.Field()
    location = scrapy.Field(input_processor=MapCompose(remove_splash))
    experience_require = scrapy.Field(input_processor=MapCompose(remove_splash))
    edu_bg = scrapy.Field(input_processor=MapCompose(remove_splash))
    full_or_part = scrapy.Field()
    job_tags = scrapy.Field()
    push_time = scrapy.Field(input_processor=MapCompose(remove_blank))
    job_advantage = scrapy.Field()
    site = scrapy.Field(input_processor=MapCompose(handle_attr,remove_splash,remove_other))

