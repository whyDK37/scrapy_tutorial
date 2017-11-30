#!/usr/bin/python
# -*- coding: UTF-8 -*-

import scrapy
import random

# "http://www.rrdnyyy.com/post/Im7X5z76QkUZb8tb",
# "http://www.rrdnyyy.com/post/7etmwzFlYc0wwlHh",
# "http://www.rrdnyyy.com/post/vyr4rmLIl8nmvZ62"


def generator_random_str():
    fstring = ""
    for num in range(16):
        if random.randint(0, 1) == 1:
            x = random.randint(1, 26)
            if random.randint(0, 1) == 1:
                x += 96
            else:
                x += 64
            fstring += (chr(x))
        else:
            x = random.randint(0, 9)
            fstring += str(x)

    return fstring

class TTSpider(scrapy.Spider):
    name = "tt"
    allowed_domains = ["rrdnyyy.com"]
    start_urls = [
        "http://www.rrdnyyy.com/post/",
        "http://www.rrdnyyy.com/post/Im7X5z76QkUZb8tb",
        "http://www.rrdnyyy.com/post/7etmwzFlYc0wwlHh",
        "http://www.rrdnyyy.com/post/unknow",
        "http://www.rrdnyyy.com/post/vyr4rmLIl8nmvZ62"
    ]

    # 优先级高于 start_urls
    def start_requests(self):
        for num in range(10, 20):
            yield scrapy.Request('http://www.rrdnyyy.com/post/' + generator_random_str(), self.parse)

    def parse(self, response):
        filename = response.url.split("/")[-2]
        self.log('----A response from %s just arrived!' % response.url)
        with open(filename, 'wb') as f:
            f.write(response.body)

    # def make_requests_from_url(url):
        # print("------------------------------"+url)
        # return url

