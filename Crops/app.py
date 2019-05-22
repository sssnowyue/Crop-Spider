# -*- encoding: utf-8 -*-
import os.path
import tornado.web
import tornado.httpserver
import tornado.ioloop
import tornado.options
from tornado import gen
from tornado.options import define, options
from tornado_mysql import pools
import json
import time

define("port", default=8004, help="run on the given port", type=int)
pools.DEBUG = True
POOL = pools.Pool(
    dict(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='********',
        db='Crops',
        charset='utf8'
    ),
    max_idle_connections=5,
    max_recycle_sec=10
)


class IndexHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('index.html')


class CornHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, region, month):
        data_dict = dict()
        min_list = list()
        max_list = list()
        # 半年、一年、一年半、两年、三年
        ticks = time.time()-30*24*60*60*int(month)
        sql = "SELECT time,min_price,max_price FROM corn WHERE region='%s' AND time>%s ORDER BY time ASC" % (
            region.encode('utf-8'), ticks)
        cur = yield POOL.execute(sql)
        datas = cur.fetchall()
        sql2 = "SELECT max(max_price),min(min_price) FROM corn WHERE region='%s' AND time>%s" % (
            region.encode('utf-8'), ticks)
        cur2 = yield POOL.execute(sql2)
        max_min = cur2.fetchall()
        for data in datas:
            min_list.append([data[0]*1000, data[1]])
            max_list.append([data[0]*1000, data[2]])
        self.render('corn.html', max=max_list, min=min_list,
                    region=region, month=month, max_price=max_min[0][0], min_price=max_min[0][1])


class PorkHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, region, month):
        price = list()
        # 几个月
        ticks = time.time()-30*24*60*60*int(month)
        sql1 = "SELECT time,price FROM pork WHERE region='%s' AND time>%s ORDER BY time ASC" % (
            region.encode('utf-8'), ticks)
        cur1 = yield POOL.execute(sql1)
        datas = cur1.fetchall()
        sql2 = "SELECT max(price),min(price) FROM pork WHERE region='%s' AND time>%s" % (
            region.encode('utf-8'), ticks)
        cur2 = yield POOL.execute(sql2)
        max_min = cur2.fetchall()
        for data in datas:
            price.append([data[0]*1000, float(data[1])])
        self.render('pork.html', price=price, region=region,
                    month=month, max=max_min[0][0], min=max_min[0][1])

class CornsHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, month):
        alldata=dict()
        # 几个月
        ticks = time.time()-30*24*60*60*int(month)
        sql = "SELECT max(max_price),min(min_price) FROM corn_pro WHERE time>%s" % (ticks)
        cur = yield POOL.execute(sql)
        max_min = cur.fetchall()

        for region in ["辽宁","吉林","黑龙江","天津","河北","内蒙古","江苏","山东","河南","湖北","湖南","江西","广东","四川","陕西","上海"]:
            sql1 = "SELECT time,(max_price+min_price)/2 FROM corn_pro WHERE province='%s' AND time>%s ORDER BY time ASC" % (region, ticks)
            cur1 = yield POOL.execute(sql1)
            datas = cur1.fetchall()
            price = list()
            for data in datas:
                price.append([data[0]*1000, float(data[1])])
            alldata[region]=price
        self.render('corns.html', month=month, max=max_min[0][0], min=max_min[0][1],datas=alldata)

class PorksHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, month):
        alldata=dict()
        # 几个月
        ticks = time.time()-30*24*60*60*int(month)
        sql = "SELECT max(price),min(price) FROM pork WHERE time>%s" % (ticks)
        cur = yield POOL.execute(sql)
        max_min = cur.fetchall()

        for region in ["辽宁","吉林","黑龙江","北京","天津","河北","山西","内蒙古","江苏","浙江","安徽","福建","山东","河南","湖北","湖南","江西","广东","广西","重庆","四川","贵州","云南","陕西","甘肃","新疆"]:
            sql1 = "SELECT time,price FROM pork WHERE region='%s' AND time>%s ORDER BY time ASC" % (region, ticks)
            cur1 = yield POOL.execute(sql1)
            datas = cur1.fetchall()
            price = list()
            for data in datas:
                price.append([data[0]*1000, float(data[1])])
            alldata[region]=price
        self.render('porks.html', month=month, max=max_min[0][0], min=max_min[0][1],datas=alldata)

class PorcorHandler(tornado.web.RequestHandler):
    @tornado.web.asynchronous
    @tornado.gen.coroutine
    def get(self, region, month):
        pork_price = list()
        corn_price = list()
        pork_time = list()
        corn_time = list()
        pcratio = list()
        ratios = list()
        # 几个月
        ticks = time.time()-30*24*60*60*int(month)
        #pork
        sql1 = "SELECT time,price FROM pork WHERE region='%s' AND time>%s ORDER BY time ASC" % (
            region.encode('utf-8'), ticks)
        cur1 = yield POOL.execute(sql1)
        datas1 = cur1.fetchall()
        sql2 = "SELECT max(price),min(price) FROM pork WHERE region='%s' AND time>%s" % (
            region.encode('utf-8'), ticks)
        cur2 = yield POOL.execute(sql2)
        max_min1 = cur2.fetchall()
        for data1 in datas1:
            pork_price.append([data1[0]*1000, float(data1[1])])
            pork_time.append(data1[0]*1000)
        #corn
        sql3 = "SELECT time,min_price,max_price FROM corn_pro WHERE province='%s' AND time>%s ORDER BY time ASC" % (
            region.encode('utf-8'), ticks)
        cur3 = yield POOL.execute(sql3)
        datas2 = cur3.fetchall()
        sql4 = "SELECT max(max_price),min(min_price) FROM corn_pro WHERE province='%s' AND time>%s" % (
            region.encode('utf-8'), ticks)
        cur4 = yield POOL.execute(sql4)
        max_min2 = cur4.fetchall()
        for data2 in datas2:
            corn_price.append([data2[0]*1000, (data2[1]+data2[2])/200])
            corn_time.append(data2[0]*1000)
        #猪粮比
        for pork in pork_time:
            if pork in corn_time:
                ratio=pork_price[pork_time.index(pork)][1]*10/corn_price[corn_time.index(pork)][1]
                pcratio.append([pork,ratio])
                ratios.append(ratio)
        #总
        data={
            "pork" : pork_price,
            "corn" : corn_price,
            "max" : max(max_min1[0][0],max_min2[0][0]/100),
            "min" : min(max_min1[0][1],max_min2[0][1]/100),
            "pcratio" : pcratio,
            "max_ra" : max(ratios),
            "min_ra" : min(ratios),
            "hig" : abs(max(ratios)-9.5)+9.5
        }
        
        self.render('porcor.html', data=data, region = region,month = month)

if __name__ == '__main__':
    tornado.options.parse_command_line()
    app = tornado.web.Application(
        handlers=[
            (r'/', IndexHandler),
            (r'/corn/(.*)/([1-9]\d*)', CornHandler),
            (r'/pork/(.*)/([1-9]\d*)', PorkHandler),
            (r'/corns/([1-9]\d*)', CornsHandler),
            (r'/porks/([1-9]\d*)', PorksHandler),
            (r'/porcor/(.*)/([1-9]\d*)', PorcorHandler)
        ],
        template_path=os.path.join(os.path.dirname(__file__), "templates"),
        debug=True
    )
    http_server = tornado.httpserver.HTTPServer(app)
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()
