# Bilibili视频信息爬虫

***开发环境：python 3.6.5、Scrapy:1.5.0***

B站的视频信息（播放数量、弹幕数、投币数等）都是动态加载的，所以通过xpath或者css选择器分析原页面是找不到该类信息的，因此分析网页的network，找到了它的api接口：

![image](https://github.com/iszoop/BilibiliSpider/blob/master/pictures/bilibili.PNG)

用浏览器打开Request_URL,就能看到所需要的信息了：

![image](https://github.com/iszoop/BilibiliSpider/blob/master/pictures/api.PNG)

**网页请求逻辑**

```python
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
```
该爬虫通过遍历av号爬取全部视频信息：

在请求原始url时，先抓取原始网页上可用的信息通过meta发送，分析api地址为：'https://api.bilibili.com/x/web-interface/archive/stat?aid='+av号
再次给api地址发送request请求，抓取剩余信息获取items；结束后请求下一个url。

**使用pyecharts将数据可视化**

bilibili一月各个分区的播放比例

![image](https://github.com/iszoop/BilibiliSpider/blob/master/pictures/%E5%90%84%E5%8C%BA%E6%92%AD%E6%94%BE%E6%AF%94%E4%BE%8B.png)

bilibili一月播放量最高的15位UP

![image](https://github.com/iszoop/BilibiliSpider/blob/master/pictures/Blibili%E4%B8%80%E6%9C%88%E8%A7%86%E9%A2%91%E6%92%AD%E6%94%BE%E6%8E%92%E8%A1%8C.png)




