import pymongo
import pandas as pd

#连接到数据库
#连接到数据库
client = pymongo.MongoClient("localhost",27017)
lianjia = client["ershoufang"]
info = lianjia["lianjia_solded"]
location = lianjia['locations']
new_info = lianjia['cd_lianjia_solded_total_2']

#将数据表1（包含原始10w+房源信息）转化为DataFrame
data1 = pd.DataFrame(list(info.find()))
print(data1.head())
#将数据表2（包含7k+小区经纬度信息）转化为DataFrame
data2 = pd.DataFrame(list(location.find()))
print(data2.head())
#多表查询，以house_name为共同键，向表一合并，与mysql的查询功能类似，得到合并后的DataFrame
result =pd.merge(data1,data2,left_on="village_name", right_on='house_name', how="left").drop(['_id_x','_id_y'],axis="columns")
#衔接上面代码，用于插入数据库，遍历插入的，不知道有没有简单的办法啊~
for i in range(len(result)):
    s = result.loc[i]
#这里加了str（）函数是无奈之举，DataFrame中的专有float64等数字格式使MongoDB无法识别，写入会报错，暂时先全部转换为字符串格式写入吧
    dic = {index:str(s[index]) for index in s.index}
    new_info.insert_one(dic)
    print(dic)