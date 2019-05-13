# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ZhilianItem(scrapy.Item):

    job_name = scrapy.Field()
    city = scrapy.Field()
    area = scrapy.Field()
    type = scrapy.Field()
    edu = scrapy.Field()
    jobTag = scrapy.Field()
    url = scrapy.Field()
    update_time = scrapy.Field()
    experience = scrapy.Field()
    average_salary = scrapy.Field()
    low_salary = scrapy.Field()
    high_salary = scrapy.Field()
