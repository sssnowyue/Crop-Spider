# -*- coding: utf-8 -*-
import scrapy
import re
import time
from tutorial.items import CornItem


class CornSpider(scrapy.Spider):
    name = 'corn'
    start_urls = ['http://www.feedtrade.com.cn/yumi/yumi_daily/']

    def parse(self, response):
        titles = response.xpath('//li/a')
        for title in titles:
            t_name = title.xpath('.//text()').extract()[0]
            if u'CFT' in t_name and u'国内' in t_name:
                t_url = title.xpath('.//@href').extract()[0]
                # 测试
                print t_name, t_url
                yield scrapy.Request(t_url, callback=self.parse_dir_contents)
        index = 2
        while index < 4:
            next_url = 'http://www.feedtrade.com.cn/yumi/yumi_daily/index_' + \
                str(index)+'.html'
            index = index+1
            yield scrapy.Request(next_url)

    def parse_dir_contents(self, response):
        item = CornItem()
        tm_str = response.xpath(
            '//td[@height="24"]/text()').extract()[0]
        time = self.getime(tm_str.encode('utf-8'))
        for sel in response.xpath('//div[@class="ReplyContent"]/div/p/text()').extract():
            region = self.reisin(sel)
            if(region):
                min, max = self.getpri(sel.encode('utf-8'))
                if min > 1000 and min < 3000 and max > 1000 and max < 3000:
                    # 测试
                    # print region, min, max, time
                    item['time'] = time
                    item['region'] = region
                    item['min_price'] = min
                    item['max_price'] = max
                    yield item

    def reisin(self, str):  # 地区
        region_lis = [u"哈尔滨", u"齐齐哈尔", u"佳木斯", u"绥化", u"通辽", u"扎兰屯", u"长春", u"公主岭", u"四平", u"榆树", u"沈阳", u"铁岭", u"大连", u"沧州",
                      u"保定", u"石家庄", u"张家口", u"邯郸", u"天津", u"焦作", u"安阳", u"濮阳", u"周口", u"临沂", u"德州", u"青岛", u"聊城", u"潍坊", u"寿光",
                      u"西安", u"大窑湾及北良港", u"鲅鱼圈港", u"锦州港", u"蛇口港", u"上海港", u"南昌", u"徐州", u"长沙", u"武汉", u"成都"]
        for re in region_lis:
            if re in str:
                return re

    def getpri(self, str):  # 价格min与max
        searchObj = re.search(r'(\d*)\-(\d*)元\/吨', str, re.M | re.I)
        if (searchObj):
            min = int(searchObj.group(1))
            max = int(searchObj.group(2))
        else:
            searchObj = re.search(r'(\d*)元\/吨', str, re.M | re.I)
            if(searchObj):
                max = min = int(searchObj.group(1))
            else:
                max = min = None
        return min, max

    def getime(self, str):  # 时间time
        searchObj = re.search(r'(\d*)\-(\d*)\-(\d*)', str, re.M | re.I)
        tm_str = searchObj.group()
        # 转换成时间数组
        timeArray = time.strptime(tm_str, "%Y-%m-%d")
        # 转换成时间戳
        timestamp = time.mktime(timeArray)
        return int(timestamp)
