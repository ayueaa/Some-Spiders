from scrapy import cmdline
cmdline.execute("scrapy crawl aochangzhang -o item.csv -t csv".split(" "))
