# -*- coding: utf-8 -*-
import scrapy
import json
from ..items import ZhihuItem
import time

class ZhihuTopicSpider(scrapy.Spider):

    handle_httpstatus_list = [403]
    name = 'zhihu_topic-IT'
    allowed_domains = ['zhihu.com']
    #topic_api_url = "https://www.zhihu.com/api/v4/topics/19552832/feeds/essence?limit={}&offset={}"  #python话题
    #topic_api_url = "https://www.zhihu.com/api/v4/topics/19587634/feeds/essence?limit={}&offset={}"   #IT话题,只需改变数字序列就可改变话题
    topic_api_url = "https://www.zhihu.com/api/v4/topics/19556498/feeds/essence?limit={}&offset={}"  #互联网话题
    answer_api_url ='https://www.zhihu.com/api/v4/questions/{}/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2Cis_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2Ccollapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2Cvoteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2Creview_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2Cis_thanked%2Cis_nothelp%2Cis_labeled%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit={}&offset={}&platform=desktop&sort_by=default'

    def start_requests(self):
        yield scrapy.Request(self.topic_api_url, callback=self.parse_topic_api,meta={"offset":0,"limit":10,"topic":"IT行业"})



    def parse_topic_api(self, response):
        if response.status == 403:
            s =input("请检查网页，填写验证码，完成后输入ok：")
            print(s)

        limit = response.meta.get('limit')
        offset = response.meta.get('offset')
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
            yield scrapy.Request(url=self.topic_api_url.format(limit, offset), callback=self.parse_topic_api,
                                 dont_filter=True,
                                 meta={'limit': limit, 'offset': offset, 'topic': topic, }
                                 )
        else:
            print("offset_num:",offset)

    def parse_answers(self,response):
        if response.status == 403:
            s =input("请检查网页，填写验证码，完成后输入ok：")
            print(s)
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
