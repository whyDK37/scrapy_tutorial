from scrapy.selector import Selector
from scrapy.http import HtmlResponse

text = '''
      <html>
         <body>
              <h1>Hello World</h1>
              <h1>Hello Scrapy</h1>
              <b>Hello python</b>
              <ul>
                  <li>C++</li>
                  <li>Java</li>
                  <li>Python</li>
              </ul>
         </body>
      </html>
      '''

selector = Selector(text=text)

response = HtmlResponse(url='https://sobooks.cc/page/1', body=text, encoding='utf8')
selector = Selector(response=response)
selector_list = selector.xpath('//h1')
print(selector_list.extract())
for sel in selector_list:
    print(sel)

selector = response.selector
print(selector.extract())
print(response.xpath('.//h1/text()').extract())

print('------------------------')
body = '''
      <html>
         <head>
              <base href='http://example.com/' />
              <title>Example website</title>
         </head>
         <body>
              <div id='images'>
                  <a href='image1.html'>Name: Image 1 <br/><img src='image1.jpg' /></a>
                  <a href='image2.html'>Name: Image 2 <br/><img src='image2.jpg' /></a>
                  <a href='image3.html'>Name: Image 3 <br/><img src='image3.jpg' /></a>
                  <a href='image4.html'>Name: Image 4 <br/><img src='image4.jpg' /></a>
                  <a href='image5.html'>Name: Image 5 <br/><img src='image5.jpg' /></a>
              </div>
         </body>
      </html>
      '''
response = HtmlResponse(url='http://www.example.com', body=body, encoding='utf8')
# 跟路径
response.xpath('/html')
# 选中所有a的文本
sel = response.xpath('//a/text()')
print(sel)
