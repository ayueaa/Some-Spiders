# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from fake_useragent import UserAgent
import random
import base64

# 代理服务器
proxyServer = "http://http-dyn.abuyun.com:9020"

# 代理隧道验证信息
proxyUser = "H4UNY11303R53B3D"
proxyPass = "7619F6E8DC6A9BC6"

proxyAuth = "Basic " + base64.urlsafe_b64encode(bytes((proxyUser + ":" + proxyPass), "ascii")).decode("utf8")

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        request.meta["proxy"] = proxyServer
        request.headers["Proxy-Authorization"] = proxyAuth

class BossDownloaderMiddleware(object):

    def __init__(self):
        self.ua = UserAgent()

    def process_request(self, request, spider):
        request.headers['User-Agent'] = self.ua.random
    #     proxy = self.get_random_proxy()
    #     request.meta['proxy'] = proxy
	#
    # def get_random_proxy(self):
    #     with open('visible_proxies.txt','r') as f:
    #         ips = f.read()
    #         return random.choice(ips.split('\n'))


