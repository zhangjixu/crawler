#### 爬取手机 app 信息，需要的工具类
* 1 Fiddler 抓包工具
* 2 phantomjs 无界面浏览器

#### Fiddler 抓包工具
```
    Fiddler 不仅仅可以抓取 PC 上开发 web 时候的数据包，而且可以抓取移动端(Android, Iphone, WindowPhone 等都可以)
    下载地址：https://www.telerik.com/download/fiddler/fiddler4
```

#### phantomjs 浏览器
```
   有的浏览器页面是通过 js 动态生成的 html body 内容，对于我们解析很不方便 使用这个工具可以帮助我们捕获到 js 生成的 body 内容
   下载地址: http://phantomjs.org/download.html
```

#### 抓取今日头条某个主题的新闻
```
    1. 设置 Fiddler 允许别的机器把 HTTP/HTTPS 请求发送到 Fiddler 上来，并且设置手机 wifi 的代理模式为手动， 代理 ip 为安装 Fiddler 的电脑 ip
    2. 手机打开今日头条 app 利用电脑端的 Fiddler 捕获到今日头条的 url。
    3. 使用 BeautifulSoup 框架解析 url 中的 json 数据，拿到 json 数据中各个新闻的 url （一般每次可以捕获 20 条新闻 url）
    4. 拿到新闻具体的 url 后，使用 selenium 以及 phantomjs（可以把 js 动态生成的 body 内容捕获） 去请求 url
    5. 拿到 html 格式的数据进行解析（和 web 端页面解析一致） 
```