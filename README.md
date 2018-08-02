# Bilibili视频信息爬虫

***开发环境：python 3.6.5、Scrapy:1.5.0***

B站的视频信息（播放数量、弹幕数、投币数等）都是动态加载的，所以通过xpath或者css选择器分析原页面是找不到该类信息的，因此分析网页的network，找到了它的api接口：

![image](https://github.com/iszoop/BilibiliSpider/blob/master/pictures/bilibili.PNG)

用浏览器打开Request_URL,就能看到所需要的信息了：

https://github.com/iszoop/BilibiliSpider/blob/master/pictures/api.PNG
