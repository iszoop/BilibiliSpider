# _*_ coding:utf-8 _*_
__author__ = 'iszoop'
__date__ = '2018/8/1 10:50'

import MySQLdb


conn = MySQLdb.connect(host="127.0.0.1",user="root",passwd="sep26th94",db="spider",charset="utf8")
cursor =conn.cursor()
def get_play_data():
#从数据库获取各分区的播放量
    random_sql = """
             SELECT video_type,play_nums FROM bilibili

           """
    result = cursor.execute(random_sql)
    datas = cursor.fetchall()
    dic = {}
    for data in datas:
        if data[0] in dic.keys():
            type = {data[0]: dic[data[0]]+data[1]}
            dic.update(type)
        else:
            dic[data[0]] = data[1]
    return dic

def get_rank_data():
#从数据库获取一个月的播放排行
    random_sql = """
                 SELECT UP,play_nums FROM bilibili

               """
    result = cursor.execute(random_sql)
    datas = cursor.fetchall()
    dic = {}
    num =0
    for data in datas:
        if data[0] in dic.keys():
            type = {data[0]: dic[data[0]] + data[1]}
            dic.update(type)
            num+=1
            print(num)
        else:
            dic[data[0]] = data[1]
            a=sorted(dic)
            num+=1
            print(num)
    print(sorted(dic)[0:9])
    return sorted(dic)[0:9]



if __name__ == "__main__":
    # get_play_data = get_play_data()
    get_rank_data = get_rank_data()








