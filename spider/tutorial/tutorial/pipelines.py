# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymysql
from tutorial import settings
from scrapy import log
from tutorial.items import CornItem
from tutorial.items import PorkItem


class CornPipeline(object):
    def __init__(self):
        self.connect = pymysql.connect(
            host=settings.MYSQL_HOST,
            db=settings.MYSQL_DBNAME,
            user=settings.MYSQL_USER,
            passwd=settings.MYSQL_PASSWD,
            port=settings.MYSQL_PORT,
            charset='utf8',
            use_unicode=True)
        self.cursor = self.connect.cursor()

    def process_item(self, item, spider):
        if item.__class__ == CornItem:
            try:
                self.cursor.execute("""insert into corn(time,region,min_price,max_price)value (%s,%s,%s,%s)""", (
                    item['time'], item['region'], item['min_price'], item['max_price']))
                self.connect.commit()
            except Exception as error:
                pass
            return item
        elif item.__class__ == PorkItem:
            try:
                self.cursor.execute("""insert into pork(time,region,price)value (%s,%s,%s)""", (
                    item['time'], item['region'], item['price']))
                self.connect.commit()
            except Exception as error:
                pass
            return item
