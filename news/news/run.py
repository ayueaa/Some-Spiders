from scrapy import cmdline
import time
import threading

cmdline.execute("scrapy crawl toutiao -s JOB_DIR=crawls/toutiao-1".split())
