# -*- coding: utf-8 -*-
import scrapy
import re
import time
from tutorial.items import PorkItem


class PorkSpider(scrapy.Spider):
    name = 'pork'
    start_urls = ['http://www.feedtrade.com.cn/livestock/pigsprice/']

    def parse(self, response):
        titles = response.xpath('//li/a')
        for title in titles:
            t_name = title.xpath('.//text()').extract()[0]
            if u'综合日报' in t_name:
                t_url = title.xpath('.//@href').extract()[0]
                # 测试
                # print t_name, t_url
                yield scrapy.Request(t_url, callback=self.parse_dir_contents)
        index = 2
        while index < 8:
            next_url = 'http://www.feedtrade.com.cn/livestock/pigsprice/index_' + \
                str(index)+'.html'
            index = index+1
            yield scrapy.Request(next_url)

    def parse_dir_contents(self, response):
        item = PorkItem()
        tm_str = response.xpath(
            '//h1/text()').extract()[0]
        time = self.getime(tm_str.encode('utf-8'))
        for tr in response.xpath('//tr[@style="height:15.0pt"]'):
            if(tr.xpath('.//td[6]')):
                region_str = tr.xpath(
                    './/td[2]/text()').extract()[0].encode('utf-8').replace(" ", "")
                if region_str == "省市" or region_str == "":
                    continue
                else:
                    region = re.sub(r"市|省", "", region_str)
                    price = float(tr.xpath('.//td[3]/text()').extract()[0])
            elif(tr.xpath('.//td[5]')):
                region = re.sub(r"市|省", "", tr.xpath('.//td[1]/text()').extract()[
                                0].replace(" ", "").encode('utf-8'))
                price = float(tr.xpath('.//td[2]/text()').extract()[0])
            else:
                continue
            # 测试
            # print region, price, time
            item['time'] = time
            item['region'] = region
            item['price'] = price
            yield item

    def getime(self, str):  # 时间time
        searchObj = re.search(r'(\d*)年(\d*)月(\d*)日', str, re.M | re.I)
        tm_str = searchObj.group()
        # 转换成时间数组
        timeArray = time.strptime(tm_str, "%Y年%m月%d日")
        # 转换成时间戳
        timestamp = time.mktime(timeArray)
        return int(timestamp)-24*60*60
