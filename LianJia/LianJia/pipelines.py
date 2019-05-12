# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from scrapy import log
from scrapy.conf import settings
from .items import LianjiaItem

class LianjiaPipeline(object):
    def __init__(self):
        self.conn = pymysql.connect(settings['MYSQL_HOST'],
                                    settings['MYSQL_USER'],
                                    settings['MYSQL_PASS'],
                                    settings['MYSQL_DBNAME'],
                                    autocommit=True)
        self.conn.set_charset('utf8')
        self.cursor = self.conn.cursor()
        self.INSERT_HOUSE = ("INSERT INTO tbl_house_new (id, title, community, model, area, "
                            "focus_num, watch_num, build_time, price, average_price, link, Latitude, Longitude, district) VALUES "
                            "('%s', '%s', '%s', '%s', '%s', %d, %d, '%s', %f, %f, '%s', %f, %f, '%s');")

    def process_item(self, item, spider):
        if isinstance(item, LianjiaItem):
            id = item['id']
            title = item['title']
            community = item['community']
            model = item['model']
            area = item['area']
            focus_num = item['focus_num']
            watch_num = item['watch_num']
            build_time = item['build_time']
            price = item['price']
            average_price = item['average_price']
            link = item['link']
            Latitude = item['Latitude']
            Longitude = item['Longitude']
            district = item['district']
            # 插入数据库
            house = (id, title, community, model, area, focus_num, watch_num, build_time, price, average_price, link,
                     Latitude, Longitude, district)
            try:
                self.cursor.execute(self.INSERT_HOUSE % house)
                log.msg("Successfully insert house "+id)
            except Exception as e:
                log.msg("MySQL Insert House Table Exception !!!", level=log.ERROR)
        return item
