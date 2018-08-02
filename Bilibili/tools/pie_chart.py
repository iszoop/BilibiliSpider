# _*_ coding:utf-8 _*_
__author__ = 'iszoop'
__date__ = '2018/8/1 12:08'
from pyecharts import Pie

from get_data import get_play_data,get_rank_data
from pyecharts import Bar


def pie_chart():
#生成饼图
    datas = get_play_data()
    type = []
    play_nums =[]
    for key,value in datas.items():
        type.append(key)
        play_nums.append(value)
    pie = Pie(page_title='B站1月播放量',height=800,width=1200)

    pie.add("", type, play_nums, is_label_show=True)
    pie.render()

def bar_chart():
#生成直方图
    datas = get_rank_data()
    UP = []
    play_nums = []
    for key, value in datas.items():
        type.append(key)
        play_nums.append(value)

    bar =Bar("Blibili一月视频播放排行",height=800,width=1200)

    bar.add("播放量", UP, play_nums,xaxis_interval=0, xaxis_rotate=30,is_label_show=True)
    bar.render()



if __name__ == "__main__":
    bar = bar_chart()
