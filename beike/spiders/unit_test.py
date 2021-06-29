import scrapy
import json
from beike.spiders.getAuth import *
from beike.items import BeikeItem


class UnitTestSpider(scrapy.Spider):
    name = 'unit_test'
    allowed_domains = ['ke.com']

    def start_requests(self):
        url = 'https://app.api.ke.com/house/ershoufang/searchv4'
        headers = {
            'Cookie': 'lianjia_udid=100000000247022;lianjia_ssid=7dc6bd64-27ac-42ef-b186-fc1b40938618;lianjia_uuid=149396e8-df32-442c-8066-ab0e81b67090',
            'Lianjia-City-Id': '110000',
            'User-Agent': 'Beike2.23.1;Android MuMu; Android 6.0.1',
            'Lianjia-Channel': 'Android_ke_tencentt',
            'Lianjia-Version': '2.23.1',
            'Lianjia-Im-Version': '2.34.0',
        }

        for page in range(21, 76501, 20):
            param = {'fullFilters': '0', 'containerType': '0', 'limitCount': '20', 'refer': 'homepage', 'condition': '',
                     'from': 'default_list', 'cityId': '110000', 'limitOffset': str(page)}
            # print("当前页码", page)
            # new_url = url % str(page)
            # print(new_url)
            # Authorization = get_authorization(url2dict(new_url))
            Authorization = get_authorization(param)  # 通过url的参数计算header里面的Authorizatino动态参数
            headers['Authorization'] = Authorization
            # print(headers)
            # yield  scrapy.Request(url=url,headers=headers,callback=self.detail_url,)
            yield scrapy.FormRequest(url=url, headers=headers, formdata=param, method='get', callback=self.detail_url,
                                     cb_kwargs={'headers': headers})

    def detail_url(self, response, headers):
        data = response.text
        data = json.loads(data)

        # print(type(data),data)
        # print(data['data']['list'])

        for list in data['data']['list']:
            if (list['houseCode'].isdigit()):
                # print(list)
                houseCode = list['houseCode']
                communityId = list['communityId']
                fbExpoId = list['fbExpoId']
                detail_url = f"https://app.api.ke.com/house/ershoufang/detailpart0v1?fb_expo_id={fbExpoId}&houseCode={houseCode}&cityId=110000&communityId={communityId}"

                Authorization = get_authorization(url2dict(detail_url))  # 通过url的参数计算header里面的Authorizatino动态参数
                headers['Authorization'] = Authorization
                yield scrapy.Request(url=detail_url, headers=headers, callback=self.parse)

    #
    def parse(self, response):
        detail_data = json.loads(response.text)
        # print(detail_data['data']['basicInfo']['title'])
        info_list = ['basicList', 'infoList', 'infoJumpList']

        ls1 = ['Title', 'Sell', 'Room', 'Area', 'price', 'time', 'Towards', 'floor', 'Building', 'elevator',
               'Decoration', 'Years', 'use', 'Ownership', 'Community', 'other', 'down_payment']
        ls2 = [detail_data['data']['basicInfo']['title']]

        for info in info_list:
            for detail_info in detail_data['data'][info]:
                # ls1.append(detail_info['name'])
                ls2.append(detail_info['value'])
                dic = dict(zip(ls1, ls2))
        print(dic)
        yield BeikeItem(dic)
