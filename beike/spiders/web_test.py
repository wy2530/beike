import scrapy
import time
import math
from beike.items import web_Item


class WebTestSpider(scrapy.Spider):
    name = 'web_test'
    allowed_domains = ['ke.com']

    def start_requests(self):
        headers = {
            #     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
            #  'Cookie': 'lianjia_uuid=29e84f42-496e-4db5-88dc-2feaaf2ae7e3; select_city=110000; lianjia_ssid=be8a89a9-ad6d-4b6f-876f-83ad3b1c107f;'
            'Cookie': 'lianjia_uuid=29e84f42-496e-4db5-88dc-2feaaf2ae7e3; select_city=110000; ; digv_extends=%7B%22utmTrackId%22%3A%2280418605%22%7D; lianjia_ssid=f9523d21-410c-4306-b510-1af21f1d0676; lianjia_uuid=7063f789-97e2-4f87-8147-7d04cc12885a; select_city=110000'
        }

        for start in range(0, 20, 10):  # 先尝试10个数据
            end = int(start + 10)
            # 1.找价格区间
            url = f'https://bj.ke.com/ershoufang/bp{start}ep{end}/'
            # print(url)
            yield scrapy.Request(url=url, callback=self.deal_page,
                                 cb_kwargs={'url': url, 'start': start, 'headers': headers})

    def deal_page(self, response, url, start, headers):
        # 2. 价格区间内的套房总数
        total_house = eval(
            response.xpath('//*[@id="beike"]/div[1]/div[4]/div[1]/div[2]/div[1]/h2/span/text()').extract()[0])
        # print(total_house)
        # 3. 计算页码需要多少页
        total_page = math.ceil(total_house / 30)  # 向上取整，判断页数
        print(total_house, total_page)

        for page in range(1, total_page + 1):
            new_url = url.rstrip('/') + 'pg' + str(page) + '/'
            # print(new_url)
            yield scrapy.Request(url=new_url, callback=self.deal_detail, headers=headers,
                                 cb_kwargs={'start': start, 'url': new_url})

    def deal_detail(self, response, start, url):
        # response已经到页面了
        # print("当前区间为价格在/万", start, "到", start + 10)
        # print("当前url为:", url)
        # 标题
        # title_list = response.xpath('//*[@class="VIEWDATA CLICKDATA maidian-detail"]/text()').extract()

        detail_url_list = response.xpath('//*[@class="VIEWDATA CLICKDATA maidian-detail"]//@href').extract()

        for detail_url in detail_url_list:
            # print(detail_url)
            yield scrapy.Request(url=detail_url, callback=self.parse)

    def parse(self, response):
        title = response.xpath('//*[@id="beike"]/div[1]/div[2]/div[2]/div/div/div[1]/h1/@title').extract()[0]
        base_info_name = response.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/span/text()').extract()
        base_info = response.xpath('//*[@id="introduction"]/div/div/div[1]/div[2]/ul/li/text()').extract()

        ls1 = ['Title', 'Sell', 'Room', 'Area', 'price', 'time', 'Towards', 'floor', 'Building', 'elevator',
               'Decoration', 'Years', 'use', 'Ownership', 'Community', 'other', 'down_payment']
        # print(base_info_name)
        dic = dict(zip(base_info_name, base_info))
        print(dic)

