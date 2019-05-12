# -*- coding: utf-8 -*-

# Scrapy settings for LianJia project


BOT_NAME = 'LianJia'

SPIDER_MODULES = ['LianJia.spiders']
NEWSPIDER_MODULE = 'LianJia.spiders'


ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 3

# SCHEDULER = "scrapy_redis.scheduler.Scheduler"    #调度
# DUPEFILTER_CLASS = "scrapy_redis.dupefilter.RFPDupeFilter"  #去重
# SCHEDULER_PERSIST = True       #不清理Redis队列
# SCHEDULER_QUEUE_CLASS = "scrapy_redis.queue.SpiderQueue"    #队列

ITEM_PIPELINES = {
   'LianJia.pipelines.LianjiaPipeline': 300,
}

MYSQL_HOST = '127.0.0.1'
MYSQL_USER = 'root'
MYSQL_PASS = '123456'
MYSQL_DBNAME = "lianjia"
