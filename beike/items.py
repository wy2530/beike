# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import datetime


class BeikeItem(scrapy.Item):
    Title = scrapy.Field()  # 标题名
    Sell = scrapy.Field()  # 售价
    Room = scrapy.Field()  # 房型
    Area = scrapy.Field()  # 建筑面积
    price = scrapy.Field()  # 单价
    time = scrapy.Field()  # 挂牌
    Towards = scrapy.Field()  # 朝向
    floor = scrapy.Field()  # 楼层
    Building = scrapy.Field()  # 楼型
    elevator = scrapy.Field()  # 电梯
    Decoration = scrapy.Field()  # 装修
    Years = scrapy.Field()  # 年代
    use = scrapy.Field()  # 用途
    Ownership = scrapy.Field()  # 权属
    Community = scrapy.Field()  # 小区
    other = scrapy.Field()  # 其他
    down_payment = scrapy.Field()  # 首付


class web_Item(scrapy.Item):
    title = scrapy.Field()
    info = scrapy.Field()
