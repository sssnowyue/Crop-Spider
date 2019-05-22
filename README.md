# Crop-Spider
【本科毕业设计】基于Scrapy的农业数据爬虫设计与实现
```
.
├── Crops # web服务
│   ├── app.py
│   ├── static # 静态文件
│   │   ├── css
│   │   └── js
│   └── templates # 静态页面
│       ├── corn.html
│       ├── corns.html
│       ├── index.html
│       ├── porcor.html
│       ├── pork.html
│       └── porks.html
├── README.md
└── spider # 爬虫及数据处理
    ├── integration # 数据汇总
    │   └── corn.py
    └── tutorial # 爬虫
        ├── scrapy.cfg # 配置文件
        └── tutorial # 项目的Python模块，从这里引用代码
            ├── __init__.py
            ├── items.py #目标文件
            ├── middlewares.py
            ├── pipelines.py # 管道文件
            ├── settings.py # 设置文件
            └── spiders # 存储爬虫代码文件夹
                ├── __init__.py
                ├── corn_spider.py # 爬取玉米价格
                ├── pork_spider.py # 爬取生猪价格
```
