# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import ZhihuItem
import time

class ZhihuTopicSpider(scrapy.Spider):
    name = 'zhihu_topic'
    allowed_domains = ['zhihu.com']
    start_urls = ['https://www.zhihu.com/topics']
    topic_api_url = "https://www.zhihu.com/api/v4/topics/{}/feeds/essence?limit={}&offset={}"
    answer_api_url ='https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit={}&offset={}&platform=desktop&sort_by=default'

    def parse(self, response):
        if response.status == 403:
            s =input("请检查网页，填写验证码，完成后输入ok：")
            print(s)
        lis = response.xpath("//ul[@class ='zm-topic-cat-main clearfix']/li")
        for li in lis:
            name = li.xpath("./a/@href").extract_first()
            topic_id = li.xpath("./@data-id").extract_first()
            yield scrapy.FormRequest(url='https://www.zhihu.com/node/TopicsPlazzaListV2', callback=self.parse_2,
                                     dont_filter=True, meta={'offset': 0, 'topic_id': topic_id, 'name': name},
                                     formdata={
                                         'method': 'next',
                                         'params': json.dumps({"topic_id": topic_id, "offset": 0, "hash_id": ""}),
                                     })

    def parse_2(self, response):
        if response.status == 403:
            s = input("请检查网页，填写验证码，完成后按任意键：")
            print(s)
        offset = response.meta.get("offset")
        topic_id = response.meta.get("topic_id")
        name = response.meta.get("name")
        text = json.loads(response.text)
        msgs = text.get("msg")
        offset += len(msgs)
        for msg in msgs:
            msg = scrapy.Selector(text=msg)
            url_id = msg.xpath(".//a/@href").extract_first().split("/")[-1]
            title = msg.xpath(".//p/text()").extract_first()
            topic = msg.xpath(".//strong/text()").extract_first()
            # print(url_id,title,topic)
            yield scrapy.Request(url=self.topic_api_url.format(url_id, 10, 0), callback=self.parse_topic_api,
                                 dont_filter=True,
                                 meta={'limit': 10, 'offset': 0, 'url_id': url_id, 'title': title, 'topic': topic,}
                                 )
        if len(msgs) != 0:
            yield scrapy.FormRequest(url='https://www.zhihu.com/node/TopicsPlazzaListV2', callback=self.parse_2,
                                     dont_filter=True, meta={'offset': offset, 'topic_id': topic_id,'name': name},
                                     formdata={
                                         'method': 'next',
                                         'params': json.dumps({"topic_id": topic_id, "offset": offset, "hash_id": ""}),
                                     })

    def parse_topic_api(self, response):

        limit = response.meta.get('limit')
        offset = response.meta.get('offset')
        url_id = response.meta.get('url_id')
        title = response.meta.get('title')
        topic = response.meta.get('topic')

        datas = json.loads(response.text).get("data")
        offset += len(datas)

        for data in datas:
            if 'zhuanlan' in data['target']['url']:
                pass
            else:
                title = data.get("target").get("question").get("title")
                question_id = data.get("target").get("question").get("id")
                print(title, question_id)
                yield scrapy.Request(url=self.answer_api_url.format(question_id, 5, 0), callback=self.parse_answers,
                                     dont_filter=True,
                                     meta={'limit': 5, 'offset': 0, 'question_id': question_id, 'title': title, 'topic': topic,}
                                     )

        if not len(datas) < 10:
            yield scrapy.Request(url=self.topic_api_url.format(url_id, limit, offset), callback=self.parse_topic_api,
                                 dont_filter=True,
                                 meta={'limit': limit, 'offset': offset, 'url_id': url_id, 'title': title, 'topic': topic, }
                                 )
        else:
            print("offset_num:",offset)

    def parse_answers(self,response):
        limit = response.meta.get('limit')
        offset = response.meta.get('offset')
        question_id = response.meta.get('question_id')
        title = response.meta.get('title')
        topic = response.meta.get('topic')
        res = json.loads(response.text)

        totals = res.get("paging").get("totals")    #回答总数
        datas = res.get("data")
        offset+=len(datas)

        for data in datas:
            author = data.get("author").get("name")
            follower_count = data.get("author").get("follower_count")
            url_token = data.get("author").get("url_token")
            user_type = data.get("author").get("user_type")
            content = data.get("content")
            excerpt = data.get("excerpt")
            content_lenth = len(content)
            create_time = time.localtime(data.get("created_time"))
            comment_count =data.get("comment_count")
            voteup_count =data.get("voteup_count")

            item =ZhihuItem()

            item['title'] = title
            item['topic'] = topic
            item['author'] = author
            item['follower_count'] = follower_count
            item['url_token'] = url_token
            item['user_type'] = user_type
            item['content'] = content
            item['excerpt'] = excerpt
            item['content_lenth'] = content_lenth
            item['create_time'] = time.strftime('%Y-%m-%d', create_time)
            item['voteup_count'] = voteup_count
            item['comment_count'] = comment_count
            yield item

        if offset < totals:
            yield scrapy.Request(url=self.answer_api_url.format(question_id, limit, offset), callback=self.parse_answers,
                                 dont_filter=True,
                                 meta={'limit': limit, 'offset': offset, 'question_id': question_id, 'title': title,
                                       'topic': topic, }
                                 )
