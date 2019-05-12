# -*- coding: utf-8 -*-
import scrapy
import requests
import re
import time
from ..items import LianjiaItem
#from scrapy_redis.spiders import RedisSpider


class LianJiaSpider(scrapy.Spider):
    name = 'lianjiaspider'
    district = ['doncheng','xicheng','chaoyang','haidian','fengtai','shijingshan','tongzhou','changping','daxing','shunyi']
    start_urls = []
    for d in district:
    	for page in range(1, 100):
    			start_urls.append('http://bj.lianjia.com/ershoufang/'+d+'/pg'+str(page)+'/')

    def start_requests(self):

        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 \
                         Safari/537.36 SE 2.X MetaSr 1.0'
        headers = {'User-Agent': user_agent}
        for start_url in self.start_urls:
            yield scrapy.Request(url=start_url, headers=headers, method='GET', callback=self.parse)

    def parse(self, response):
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.22 \
                                 Safari/537.36 SE 2.X MetaSr 1.0'
        headers = {'User-Agent': user_agent}
        house_list = response.xpath('//li[@class="clear LOGCLICKDATA"]')
        for house in house_list:
            try:
                house_url = house.xpath('./a/@href').extract()[0]
                house_title = house.xpath('./div/div[1]/a/text()').extract()[0]
                house_id = house.xpath('./div/div[1]/a/@data-housecode').extract()[0]
                district = response.url.split('/')[-3]
                yield scrapy.Request(url=house_url, meta={'title': house_title, 'id': house_id, 'district': district}, headers=headers, callback=self.parse_detail)
            except Exception as e:
                print(e)
        time.sleep(3)

    def get_latitude(self, community):  # 通过百度API获取经纬度
        community = "北京市" + community
        base = "http://api.map.baidu.com/geocoder?address=" + community + "&output=json&" \
                                                                          "key=1WCR9gE9P64K1fxLUZu7sigboxoRVT8o"
        response = requests.get(base)
        answer = response.json()
        return answer['result']['location']['lat'], answer['result']['location']['lng']



    def parse_detail(self, response):
        'https://bj.lianjia.com/ershoufang/101104239798.html'
        try:
            item = LianjiaItem()
            item['id'] = response.meta['id']
            item['title'] = response.meta['title']
            item['district'] = response.meta['district']
            item['community'] = response.xpath('//div[@class="communityName"]/a/text()').extract()[0]
            item['model'] = response.xpath('//div[@class="room"]/div[1]/text()').extract()[0]
            item['area'] = response.xpath('//div[@class="area"]/div[1]/text()').extract()[0]

            item['focus_num'] = response.xpath('//span[@id="favCount"]/text()').extract()[0]
            item['focus_num'] = int(item['focus_num'])
            item['watch_num'] = response.xpath('//span[@id="cartCount"]/text()').extract()[0]
            item['watch_num'] = int(item['watch_num'])
            item['build_time'] = response.xpath('//div[@class="area"]/div[2]/text()').extract()[0]
            item['price'] = response.xpath('//span[@class="total"]/text()').extract()[0]
            item['price'] = float(item['price'])
            item['average_price'] = response.xpath('//span[@class="unitPriceValue"]/text()').extract()[0]
            item['average_price'] = float(item['average_price'])
            item['link'] = response.url
            item['Latitude'], item['Longitude'] = self.get_latitude(item['community'])
        except Exception:
            pass
        time.sleep(3)
        yield item
