# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request

from items import defaultitem,BilibiliItem
try:
    import urlparse as parse
except:
    from urllib import parse

import json
import re
import datetime


class BilibiliSpider(scrapy.Spider):
    name = 'bilibili'
    allowed_domains = ['www.bilibili.com','space.bilibili.com',"api.bilibili.com"]
    start_urls = ['https://www.bilibili.com/video/av18167273']        #设置起始页


    def parse(self, response):
        """
        分析返回的页面，并抓取可用的静态数据
        """
        key_word = re.match(".*(video).*",response.url)
        if key_word and response.status == 200:                        #筛选出有效页面
            status = response.css(".error-text::text")
            match_re = re.match(".*?(\d+).*", response.url)
            av_num = match_re.group(1)
            if status:                                                 #去除视频丢失的页面
                match_re = int(av_num)+1

                yield Request(url='https://www.bilibili.com/video/av{0}'.format(match_re),callback=self.parse)
            else:
                title = response.css("#viewbox_report h1 span::text").extract()
                url = response.url
                UP = response.css(".info a[href]::text").extract()
                up_url = response.css(".info a::attr(href)").extract()
                video_type = response.css("span.crumb:nth-child(2) > a:nth-child(1)::text").extract()
                up_time = response.css(".tm-info.tminfo time::text").extract()

                yield scrapy.Request("https://api.bilibili.com/x/web-interface/archive/stat?aid={0}".format(av_num),
                                    meta={
                                        "title":title,"url":url, "UP":UP,"up_url":up_url,"video_type":video_type,
                                        'up_time':up_time,"av_num":av_num,
                                    },callback=self.parse_item)             #爬取静态数据

            yield Request(url='https://www.bilibili.com/video/av{0}'.format(match_re), callback=self.parse) #爬取json数据
        else:
            av_num = 0
            if response.status == 404:                          #跳过404页面
                fail_url = response.request._url
                match_re = re.match(".*av(\d+).*",fail_url)
                av_num = int(match_re.group(1))+1
            elif response.status == 302 or 301:                 #跳过重定向页面
                referer = response.meta["redirect_urls"]
                match_re = re.match(".*?(\d+).*", referer[0])
                av_num = int(match_re.group(1))+1

            yield Request(url='https://www.bilibili.com/video/av{0}'.format(av_num), callback=self.parse)


    def parse_item(self,response):
        """抓取动态数据"""
        json_view = json.loads(response.text)
        if json_view["code"] == 0:

            numbers = json_view["data"]
            play_nums = numbers["view"]
            barrage_nums = numbers["danmaku"]
            coin_nums = numbers["coin"]
            fav_nums = numbers["favorite"]
            comment_nums = numbers["reply"]

            item_loader = defaultitem(item=BilibiliItem(),response=response)
            item_loader.add_value("av_num",response.meta.get("av_num"))
            item_loader.add_value("title", response.meta.get("title", ""))
            item_loader.add_value("url", response.meta.get("url", ""))
            item_loader.add_value("UP", response.meta.get("UP", ""))
            item_loader.add_value("up_url", response.meta.get("up_url", ""))
            item_loader.add_value("video_type", response.meta.get("video_type", ""))
            item_loader.add_value("up_time", response.meta.get("up_time", ""))
            item_loader.add_value("play_nums",play_nums)
            item_loader.add_value("barrage_nums", barrage_nums)
            item_loader.add_value("coin_nums", coin_nums)
            item_loader.add_value("fav_nums", fav_nums)
            item_loader.add_value("comment_nums", comment_nums)
            item_loader.add_value("crawl_time",datetime.datetime.now())

            video_item = item_loader.load_item()
            yield video_item





