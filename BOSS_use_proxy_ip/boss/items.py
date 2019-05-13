# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,Compose,Join,MapCompose


def handle_start_money(value):
    try:
        new_value = int(value.split("万")[0])*10000
    except:
        new_value = float(value.split("万")[0])*10000
    return new_value


def handle_salary(value):
    return value.split("元")[0]


def remove_tags(value):
    return value.replace('\n','').replace(' ','').replace("查看地图", "")


class BossItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class BossItem(scrapy.Item):
    job_status = scrapy.Field()
    name = scrapy.Field()
    salary = scrapy.Field(
        input_processor=MapCompose(handle_salary)
    )
    detail_location = scrapy.Field()
    location = scrapy.Field()
    experience = scrapy.Field()
    education = scrapy.Field()
    tags = scrapy.Field(
        output_processor=Join(",")
    )
    company = scrapy.Field()
    start_money = scrapy.Field(
        input_processor=MapCompose(handle_start_money)
    )
    start_time = scrapy.Field()
    require = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join("")
    )
    url = scrapy.Field()