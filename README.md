# scrapy_tutorial
scrapy_tutorial，爬虫测试类

# 软件版本
- python 3.5+
- scrapy
- dependency/Win64OpenSSL_Light-1_0_2m.exe

# 安装
Anaconda 安装方式
```
>conda install -c conda-forge scrapy
```

安装 dependency/Win64OpenSSL_Light-1_0_2m.exe ，使用默认安装目录即可。安装后把C:\OpenSSL-Win64\bin配置都path环境变量中。

# 使用
tutorial/spiders目录下是自定义的爬虫文件

如：tutorial/spiders/tt_spider.py，运行方式如下

```
>scrapy crawl tt
```

# 参考
- [Scrapy 1.4 documentation](https://docs.scrapy.org/en/latest/index.html)
- [Scrapy 0.24 文档](http://scrapy-chs.readthedocs.io/zh_CN/0.24/index.html)
