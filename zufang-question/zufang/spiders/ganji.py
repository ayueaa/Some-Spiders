import scrapy
from zufang.items import ZufangItem

class GanjiSpider(scrapy.Spider):
    name = "zufang"
    start_urls = ['http://bj.ganji.com/fang1/chaoyang/']

    def parse(self, response):
        zf = ZufangItem()
        title_list = response.xpath(".//div[@class='f-list-item ']/dl/dd[1]/a/text()").extract()
        money_list = response.xpath(".//div[@class='f-list-item ']/dl/dd[5]/div[1]/span[1]/text()").extract()
        for i,j in zip(title_list, money_list):
            zf['title'] = i
            zf['money'] = j
            yield zf