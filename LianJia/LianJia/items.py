# -*- coding: utf-8 -*-

import scrapy


class LianjiaItem(scrapy.Item):
    # id 标题 小区  户型   面积   关注人数  看房人数  建造时间  价格   均价  详情链接  经纬度 行政区
    id = scrapy.Field()
    title = scrapy.Field()
    community = scrapy.Field()
    model = scrapy.Field()
    area = scrapy.Field()
    focus_num = scrapy.Field()
    watch_num = scrapy.Field()
    build_time = scrapy.Field()
    price = scrapy.Field()
    average_price = scrapy.Field()
    link = scrapy.Field()
    Latitude = scrapy.Field()
    Longitude = scrapy.Field()
    district = scrapy.Field()
