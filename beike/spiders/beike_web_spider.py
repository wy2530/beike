import scrapy
import re
import json


class BeikeSpiderWebSpider(scrapy.Spider):
    name = 'beike_web_spider'

    def start_requests(self):
        for price in range(0, 10000, 10):
            url = "https://bj.ke.com/ershoufang/"
            url = url + "bp" + str(price) + "ep" + str(price + 10)
            # print(url)
            # print("当前筛选条件为",str(price),"到",str(price+10),"万的的北京二手房源信息")
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
                'Cookie': 'lianjia_uuid=29e84f42-496e-4db5-88dc-2feaaf2ae7e3; select_city=110000; lianjia_ssid=be8a89a9-ad6d-4b6f-876f-83ad3b1c107f;'
            }
            yield scrapy.Request(url=url, headers=headers, callback=self.get_house_and_page,
                                 cb_kwargs={"url": url, "headers": headers, "price": price})

    def get_house_and_page(self, response, url, headers, price):
        # 获取当前url对应的总房源数
        total_house = eval(
            response.xpath('//*[@id="beike"]/div[1]/div[4]/div[1]/div[2]/div[1]/h2/span/text()').extract()[0])
        # print("当前筛选条件下的房源总数为", total_house)

        # 获取当前url下房源的总页数，只要小于100页都没问题
        page_div = response.xpath('//*[@class="page-box house-lst-page-box"]').extract()[0]
        # print(page_div)

        pattern = re.compile(r'page-data=.+\'')
        result = pattern.findall(page_div)
        json_Page = result[0].split('=')[1]
        page = json.loads(eval(json_Page))
        totalPage = page['totalPage']
        # print('总页数为：',totalPage)
        for i in range(1, totalPage + 1):
            new_url = url.rstrip('/') + "pg" + str(i)
            # print(new_url)
            yield scrapy.Request(url=new_url, headers=headers, callback=self.parse,
                                 cb_kwargs={"i": i, "price": price, "total_house": total_house, "totalPage": totalPage})

    def parse(self, response, i, price, total_house, totalPage):
        # 获取当前页面的所有title,返回list
        title_list = response.xpath('//*[@class="VIEWDATA CLICKDATA maidian-detail"]/text()').extract()
        href_list = response.xpath('//*[@class="VIEWDATA CLICKDATA maidian-detail"]//@href').extract()
        print("-" * 20)
        print("当前筛选条件为", str(price), "到", str(price + 10), "万的的北京二手房源信息")
        print("当前筛选条件下的房源总数为", total_house)
        print('总页数为：', totalPage)
        print("当前页面为第", i, "页，房源总数为", len(title_list))
        print("title列表为", title_list)
        print("url列表为", href_list)
        print("-" * 20)
