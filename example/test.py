import scrapy

import re
import csv

def error(response):
    print('error...')


def parse(response):
    print('parse...')
    books = response.css('div.card-item')
    for book in books:
        print(book)


request = scrapy.Request('https://sobooks.cc/page/1', dont_filter=True, callback=parse, errback=error)
request = scrapy.Request('https://sobooks.cc/page/1', encoding='utf8')

string = '''
<b style="font-size:16px; color:#F00;">城通网盘：<a href="https://sobooks.cc/go.html?url=https://url66.ctfile.com/d/14804066-46740927-03ab7c" rel="nofollow">日本及其历史枷锁</a> 密码:666888<br>蓝奏云盘：<a href="https://sobooks.cc/go.html?url=https://sobooks.lanzouo.com/b03ohqsla" rel="nofollow">日本及其历史枷锁</a> 密码:4fn6<br>备份云盘：<a href="https://sobooks.cc/go.html?url=https://sobooks.cloud/2022/01/19393.epub" rel="nofollow">日本及其历史枷锁</a></b>
'''

# url_idx = string.index("url")
# print(url_idx)
# string = string[url_idx + 4:]
#
# url1 = string[:string.index('"')]
# print(url1)
#
# string = string[url_idx + 4:]

def extract_download_url(string):
    mys = re.split('<a|</a>|<br>', string)
    urls = []
    passwd = []
    for str in mys:
        print('>', str)

        if (str.find('url') >= 0):
            url_idx = str.index("url")
            str = str[url_idx + 4:]
            url1 = str[:str.index('"')]
            urls.append(url1)
        if (str.find('密码') >= 0):
            passwd.append(str[str.index("密码") + 3:])
    return urls, passwd


urls, passwd = extract_download_url(string)

print(urls)
print(passwd)


# open file for reading
with open('books2.csv') as csvDataFile:

    # read file as csv file
    csvReader = csv.reader(csvDataFile)

    # for every row, print the row
    for row in csvReader:
        print(row[3])
