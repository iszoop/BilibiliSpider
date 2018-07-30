# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose,TakeFirst,Join
import datetime
from settings import SQL_DATETIME_FORMAT


class defaultitem(ItemLoader):
    default_output_processor = TakeFirst()


class BilibiliItem(scrapy.Item):
    """
    item 配置
    """
    title = scrapy.Field()
    av_num = scrapy.Field()
    url = scrapy.Field()
    UP = scrapy.Field()
    up_url = scrapy.Field()
    play_nums = scrapy.Field()
    barrage_nums = scrapy.Field()
    coin_nums = scrapy.Field()
    fav_nums = scrapy.Field()
    comment_nums = scrapy.Field()
    video_type = scrapy.Field()
    up_time = scrapy.Field()
    crawl_time = scrapy.Field()

    def get_insert_sql(self):
        """
        item的sql配置
        """
        insert_sql = """
               insert into bilibili(title,av_num, url, UP, up_url, play_nums, barrage_nums, coin_nums,
                 fav_nums, comment_nums,video_type,up_time,crawl_time
                 )
               VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,%s)
               ON DUPLICATE KEY UPDATE play_nums=VALUES(play_nums), barrage_nums=VALUES(barrage_nums), coin_nums=VALUES(coin_nums),
                 fav_nums=VALUES(fav_nums), comment_nums=VALUES(comment_nums)
           """
        # crawl_time = datetime.datetime.fromtimestamp(self["crawl_time"]).strftime(SQL_DATETIME_FORMAT)
        params = (
            self["title"],self["av_num"],self["url"],self["UP"],
            self["up_url"],self["play_nums"],self["barrage_nums"],
            self["coin_nums"],self["fav_nums"],self["comment_nums"],
            self["video_type"],self["up_time"],self["crawl_time"]
        )
        return insert_sql,params

