# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,Compose,Join,MapCompose
import re

class XiaoZhuItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def extract_figure(value):
    num = int(re.findall(r"(\d+)", value)[0])
    return num

def remove_tag(value):
    try:
        x = re.findall(r"(.*?)\n", value)[0]
        return x
    except:
        return value


class XiaozhuItem(scrapy.Item):
    title = scrapy.Field(
        input_processor=MapCompose(remove_tag)
    )
    location = scrapy.Field()
    address = scrapy.Field(
        input_processor=MapCompose(remove_tag)
    )
    price = scrapy.Field(
        input_processor=MapCompose(extract_figure)
    )
    owner = scrapy.Field()
    rent_mode = scrapy.Field()
    area = scrapy.Field(
        input_processor=MapCompose(extract_figure)
    )
    room_num = scrapy.Field(
        input_processor=MapCompose(extract_figure)
    )
    bed_num = scrapy.Field(
        input_processor=MapCompose(extract_figure)
    )
    person_visible = scrapy.Field(
        input_processor=MapCompose(extract_figure)
    )
    room_info = scrapy.Field()
    traffic_info = scrapy.Field()
    comment_num = scrapy.Field(
        input_processor=MapCompose(extract_figure)
    )
    comment_star = scrapy.Field(
        input_processor=MapCompose(extract_figure)
    )

