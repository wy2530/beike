import hashlib
import base64
import re

AppSecret = "d5e343d453aecca8b14b2dc687c381ca"
AppId = "20180111_android"


def get_authorization(url_dict):
    global AppSecret
    global AppId
    sorted_dict = {key: url_dict[key] for key in sorted(url_dict)}
    localObject1 = ''.join([key + '=' + str(sorted_dict[key]) for key in sorted_dict.keys()])
    localObject1 = AppSecret + localObject1
    localObject1_sha1 = hashlib.sha1(localObject1.encode()).hexdigest()
    authorization_source = AppId + ":" + localObject1_sha1
    authorization = base64.b64encode(authorization_source.encode())
    return authorization.decode()


def url2dict(url):
    params = re.search(r'.*\?(.*)', url).group(1)
    params_list = params.split("&")
    params_dict = {}
    for item in params_list:
        key = re.search(r'(.*)=(.*)', item).group(1)
        value = re.search(r'(.*)=(.*)', item).group(2) if not item.endswith("=") else ""
        params_dict[key] = value
    return params_dict


# MjAxODAxMTFfYW5kcm9pZDo5YzY2YWJjZTkwNTBiZDRhZjA2MDE1YTQyODE4MzU2NzEwNGM1ZTFi
if __name__ == '__main__':
    url = 'https://app.api.ke.com/house/ershoufang/searchv4?fullFilters=0&containerType=0&limitCount=20&refer=homepage&condition=&from=default_list&cityId=110000&limitOffset=21'
    print(get_authorization(url2dict(url)))
