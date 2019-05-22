# -*- coding: utf-8 -*-
import pymysql
import time
db = pymysql.connect("localhost", "root", "************", "Crops")
cursor = db.cursor()

pros = {
    "黑龙江": ["哈尔滨", "齐齐哈尔", "佳木斯", "绥化"],
    "内蒙古": ["通辽", "扎兰屯"],
    "吉林": ["长春", "公主岭", "四平", "榆树"],
    "辽宁": ["沈阳", "铁岭", "大连", "大窑湾及北良港", "鲅鱼圈港", "锦州港"],
    "河北": ["沧州", "保定", "石家庄", "张家口", "邯郸"],
    "天津": ["天津"],
    "河南": ["焦作", "安阳", "濮阳", "周口"],
    "山东": ["临沂", "德州", "青岛", "聊城", "潍坊", "寿光"],
    "陕西": ["西安"],
    "广东": ["蛇口港"],
    "上海": ["上海港"],
    "江西": ["南昌"],
    "江苏": ["徐州"],
    "湖南": ["长沙"],
    "湖北": ["武汉"],
    "四川": ["成都"]
}
n = m = 0
for key, value in pros.items():
    cities = ""
    for va in value:
        cities = cities+",'"+va+"'"
    tm = 1558540800
    tm_start = tm
    # tm_end = tm-2*365*24*60*60
    tm_end = tm-30*24*60*60
    while tm > tm_end:
        sql = "INSERT INTO corn_pro(province,time,max_price,min_price) SELECT \"" + key + \
            "\","+str(tm)+",AVG(max_price),AVG(min_price) FROM corn WHERE region IN (" + \
            cities[1:]+") AND time="+str(tm)
        tm = tm-24*60*60
        try:
            cursor.execute(sql)
            db.commit()
            n = n+1
            print "第", n, "条插入成功"
        except:
            m = m+1
            print "第", m, "条插入成功"
            db.rollback()
db.close()
