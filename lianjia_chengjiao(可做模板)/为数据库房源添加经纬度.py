import pymongo
import pandas as pd
import requests
import re
from multiprocessing import Pool
#数据库连接
client = pymongo.MongoClient("localhost",27017)
db = client['ershoufang']
collection = db["lianjia_solded"]
location = db['locations']

#高德地图获取地理信息的api接口
gaode_api_url = "https://restapi.amap.com/v3/geocode/geo?address={}&output=XML&key=c9ac8c7e25cddfd71c8d58da50199181"
headers = {
    "User-Agent" : "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36"
}

def get_location_info(loc):
    """
    利用高德开放平台，解析小区全部位置信息（包含经纬度），存入数据库
    :param loc: 小区名字
    :return: 具体位置信息
    """
    new_loc = "成都市" + loc
    parse_adress_url = gaode_api_url.format(new_loc)
    response = requests.get(parse_adress_url, headers=headers).text
    # 加入判断防止空白信息返回
    if re.search(r"<count>1</count>", response, re.S):
        # 提取api反馈的地理信息
        detail_info = re.findall(r"_address>(.*?)</.*?<district>(.*?)</district>.*?<location>(.*?)</location>", response, re.S)[0]
        result = {
            'house_name': loc,
            'adress': detail_info[0],
            'district': detail_info[1],
            'location': detail_info[2],
            'longitude': detail_info[2].split(",")[0],
            'latitude': detail_info[2].split(",")[1]
        }
        # 插入数据库
        location.insert_one(result)
        print(result)
    else:
        print("Something Wrong！未获取到api信息！")


if __name__ == '__main__':
    #从数据库中获取源小区名
    data = pd.DataFrame(list(collection.find())).drop(['elevator', 'url', 'village_id'], axis='columns')
    # 小区名
    locs = data["village_name"]
    locs_num = pd.value_counts(locs, sort=True)
    #开启进程池
    p = Pool(3)
    for loc in locs_num.index[6000:]:  # 高德api限制每天请求不超过6000个
        p.apply_async(get_location_info, (loc,))
    p.close()
    p.join()






