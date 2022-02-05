# -*- coding: utf-8 -*-
import scrapy


class BooksSpider(scrapy.Spider):
    # 每一个爬虫的唯一标识
    # 一个Scrapy项目中可能有多个爬虫，每个爬虫的name属性是其自身的唯一标识，在一个项目中不能有同名的爬虫，本例中的爬虫取名为'books'。
    name = "books"

    # 定义爬虫爬取的起始点，起始点可以是多个，这里只有一个
    # 一个爬虫总要从某个（或某些）页面开始爬取，我们称这样的页面为起始爬取点，start_urls属性用来设置一个爬虫的起始爬取点。在本例中只有一个起始爬取点'http://books.toscrape.com'。
    start_urls = ['http://books.toscrape.com/']

    # 当一个页面下载完成后，Scrapy引擎会回调一个我们指定的页面解析函数（默认为parse方法）解析页面。一个页面解析函数通常需要完成以下两个任务：
    #
    # 　提取页面中的数据（使用XPath或CSS选择器）。
    #
    # 　提取页面中的链接，并产生对链接页面的下载请求。
    def parse(self, response):
        # 提取数据
        # 每一本书的信息在<article class="product_pod">中，我们使用
        # css()方法找到所有这样的article 元素，并依次迭代
        for book in response.css('article.product_pod'):
            # 书名信息在article > h3 > a 元素的title属性里
            # 例如: <a title="A Light in the Attic">A Light in the ...</a>
            name = book.xpath('./h3/a/@title').extract_first()
            # 书价信息在 <p class="price_color">的TEXT中。
            # 例如: <p class="price_color">￡51.77</p>
            price = book.css('p.price_color::text').extract_first()
            yield {
                'name': name,
                'price': price,
            }

            # 提取链接
            # 下一页的url 在ul.pager > li.next > a 里面
            # 例如: <li class="next"><a href="catalogue/page-2.html">next</a></li>
        next_url = response.css('ul.pager li.next a::attr(href)').extract_first()
        if next_url:
            # 如果找到下一页的URL，得到绝对路径，构造新的Request 对象
            next_url = response.urljoin(next_url)
            yield scrapy.Request(next_url, callback=self.parse)
