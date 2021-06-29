from requests import get

url = 'https://app.api.ke.com/house/ershoufang/searchv4?fullFilters=0&containerType=0&limitCount=20&refer=homepage&condition=&from=default_list&cityId=110000&limitOffset=61'
headers = {
    'Cookie': 'lianjia_udid=100000000247022;lianjia_ssid=7dc6bd64-27ac-42ef-b186-fc1b40938618;lianjia_uuid=149396e8-df32-442c-8066-ab0e81b67090',
    'Lianjia-City-Id': '110000',
    'User-Agent': 'Beike2.23.1;Android MuMu; Android 6.0.1',
    'Lianjia-Channel': 'Android_ke_tencentt',
    'Lianjia-Version': '2.23.1',
    'Authorization': 'MjAxODAxMTFfYW5kcm9pZDpjZjE3OGU5MGM1OWRlZTM5NzdjMGE5YTI5OGQ4NGQ4NTMwMzc5OGE3',
    'Lianjia-Im-Version': '2.34.0',
}

rsp = get(url=url ,headers=headers).text
print(rsp)
