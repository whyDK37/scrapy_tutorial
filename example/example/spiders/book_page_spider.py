# -*- coding: utf-8 -*-
import scrapy
import re
import csv


class BooksSpider(scrapy.Spider):
    # 每一个爬虫的唯一标识
    # 一个Scrapy项目中可能有多个爬虫，每个爬虫的name属性是其自身的唯一标识，在一个项目中不能有同名的爬虫，本例中的爬虫取名为'books'。
    name = "book-page"

    # 定义爬虫爬取的起始点，起始点可以是多个，这里只有一个
    # 一个爬虫总要从某个（或某些）页面开始爬取，我们称这样的页面为起始爬取点，start_urls属性用来设置一个爬虫的起始爬取点。在本例中只有一个起始爬取点'http://books.toscrape.com'。
    start_urls = ['https://sobooks.cc/books/19393.html', 'https://sobooks.cc/books/13321.html']

    def start_requests(self):
        data = {
            'e_secret_key': "258886"
        }
        # for url in self.start_urls:
        #     yield scrapy.FormRequest(url=url, formdata=data, callback=self.parse)

        # read url from csv
        with open('books2.csv') as csvDataFile:
            # read file as csv file
            csvReader = csv.reader(csvDataFile)
            # for every row, print the row
            for row in csvReader:
                url = row[3]
                if (url.find('http') >= 0):
                    yield scrapy.FormRequest(url=url, formdata=data, callback=self.parse)

    # 当一个页面下载完成后，Scrapy引擎会回调一个我们指定的页面解析函数（默认为parse方法）解析页面。一个页面解析函数通常需要完成以下两个任务：
    #
    # 　提取页面中的数据（使用XPath或CSS选择器）。
    #
    # 　提取页面中的链接，并产生对链接页面的下载请求。
    def parse(self, response):
        # 提取数据
        # 每一本书的信息在<article class="product_pod">中，我们使用
        # css()方法找到所有这样的article 元素，并依次迭代
        header = response.css('header.article-header')
        if (len(header) == 0):
            return

        bookinfo = response.css('div.bookinfo')

        bookinfos = bookinfo.xpath('./ul/li')

        # name
        nameInfo = bookinfos[0].extract()
        name = nameInfo[nameInfo.find('/strong>') + 8:nameInfo.find('</li>')]

        authorInfo = bookinfos[1].extract()
        author = authorInfo[authorInfo.find('/strong>') + 8:authorInfo.find('</li>')]

        ISBNInfo = bookinfos[6].extract()
        isbn = ISBNInfo[ISBNInfo.find('/strong>') + 8:ISBNInfo.find('</li>')]

        download_html = response.css('div.e-secret').xpath('./b').extract_first()

        urls, passwds = self.extract_download_url(download_html)

        #  页面显示的下载链接

        try:
            page_dl = response.css('table.dltable').xpath('./tbody/tr')[2].xpath('td/a')
            for pd in page_dl:
                urls.append(self.extract_url(pd.xpath('@href').extract_first()))
                passwds.append('')
        except:
            print("no page dl info")
        # max_length = min(len(urls), len(passwds))
        # urls = urls[:max_length]
        # passwds = passwds[:max_length]

        yield {
            'name': name,
            'author': author,
            'isbn': isbn,
            'urls': urls,
            'passwds': passwds
        }

    def extract_download_url(self, html):
        mys = re.split('<a|</a>|<br>', html)
        urls = []
        passwd = []
        for str in mys:
            print('>', str)

            if (str.find('url') >= 0):
                url1 = self.extract_url(str)
                urls.append(url1)
            if (str.find('密码') >= 0):
                end = str.find('</b>') if (str.find('</b>') >= 0) else len(str)
                passwd.append(str[str.index("密码") + 3:end])

        if (len(urls) > len(passwd)):
            passwd.append('')
        if (len(passwd) > len(urls)):
            urls.append('')
        return urls, passwd

    def extract_url(self, str):
        url_idx = str.index("url")
        str = str[url_idx + 4:]
        url1 = str[:str.find('"') if str.find('"') >= 0 else len(str)]
        return url1
