# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo


class BeikePipeline:
    def __init__(self):
        self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)  #
        self.db = self.client['bk']
        self.table = self.db['bk_shop']

    def process_item(self, item, spider):
        self.table.insert(dict(item))
        return item


class webPipline:
    def __init__(self):
        self.client = pymongo.MongoClient(host='127.0.0.1', port=27017)  #
        self.db = self.client['bk']
        self.table = self.db['web_info']

    def process_item(self, item, spider):
        self.table.insert(dict(item))
        return item
