#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: requests入门
"""
import requests
import re
from io import StringIO
import json


def quick():
    # 常见的请求协议
    # r = requests.get('https://api.github.com/events')
    # r = requests.get("http://httpbin.org/get")
    # r = requests.put("http://httpbin.org/put")
    # r = requests.delete("http://httpbin.org/delete")
    # r = requests.head("http://httpbin.org/get")
    # r = requests.options("http://httpbin.org/get")

    # URL传递参数
    # payload = {'key1': 'value1', 'key2': 'value2'}
    # r = requests.get("http://httpbin.org/get", params=payload)
    # print(r.url)

    # 读取返回结果
    # r = requests.get('https://api.github.com/events')
    # 打印默认的编码方式
    # print(r.encoding)
    # 改变r.encoding
    # r.encoding = 'utf-8'
    # print(r.text)

    # 读取HTML/XML格式的网页
    # r = requests.get('http://www.baidu.com/')
    # print(re.findall('content="text/html;charset=.*"', 'content="text/html;charset=utf-8"'))
    # 如果只是搜索第一个出现的，就使用search就行了，不需要用findall
    # print(re.search('content="text/html;charset=.*?"', r.content.decode('utf-8')).group(0))
    # print(r.encoding)
    # print(r.text)

    # 从返回值的二进制数据中直接创建一个图片
    # i = Image.open(StringIO(r.content))

    # JSON返回值
    # r = requests.get('https://api.github.com/events')
    # print([(type(a), a) for a in (r.json(),)])
    # print(*((type(a), a) for a in ([1, 2],)))

    # # 直接返回原始的内容
    # r = requests.get('http://requests.readthedocs.org/en/'
    #                  'latest/_static/requests-sidebar.png', stream=True)
    # # print(r.raw)
    # # print(r.raw.read(10))
    # # 然后使用字节流下载对应的内容，注意啊，运行下面这个要先注释掉上面的r.raw.read(10)
    # chunk_size = 1024
    # with open('downloads.png', 'wb') as fd:
    #     for chunk in r.iter_content(chunk_size):
    #         fd.write(chunk)

    # 自定义Header
    # url = 'https://api.github.com/some/endpoint'
    # payload = {'some': 'data'}
    # headers = {'content-type': 'application/json'}
    # r = requests.post(url, data=json.dumps(payload), headers=headers)

    # 高级的POST请求示例，POST常见的四种请求内容格式
    # 1. application/x-www-form-urlencoded
    # 2. multipart/form-data
    # 3. application/json
    # 4. text/xml

    # 如果传入一个字典形式的参数，那么默认就是第一种请求格式x-www-form-urlencoded
    # payload = {'key1': 'value1', 'key2': 'value2'}
    # r = requests.post("http://httpbin.org/post", data=payload)
    # print(r.text)
    # # JSON请求，直接提供一个字符串给data，application/json格式
    # url = 'https://api.github.com/some/endpoint'
    # payload = {'some': 'data'}
    # r = requests.post(url, data=json.dumps(payload))

    # POST一个文件，multipart/form-data请求格式
    # url = 'http://httpbin.org/post'
    # 可以设置文件名，content_type 和 headers
    # files = {'file': ('report.xlsx', open('report.xlsx', 'rb')
    # , 'application/vnd.ms-excel', {'Expires': '0'})}
    # r = requests.post(url, files=files)
    # print(r.text)
    # 如果你还想将字符串作为文件POST提交，可以这样
    # files = {'file': ('report.csv', 'some,data,to,send\nanother,row,to,send\n')}
    # r = requests.post(url, files=files)
    # print(r.text)

    # 响应status_code
    # r = requests.get('http://httpbin.org/get')
    # print(r.status_code)
    # print(r.status_code == requests.codes.ok)
    # bad_r = requests.get('http://httpbin.org/status/404')
    # print(bad_r.status_code)
    # 如果不是2XX返回值，抛出异常
    # bad_r.raise_for_status()

    # 响应Headers
    # print(r.headers)
    # {
    #     'content-encoding': 'gzip',
    #     'transfer-encoding': 'chunked',
    #     'connection': 'close',
    #     'server': 'nginx/1.0.4',
    #     'x-runtime': '148ms',
    #     'etag': '"e1ca502697e5c9317743dc078f67693f"',
    #     'content-type': 'application/json'
    # }
    # print(r.headers['Content-Type'])
    # print(r.headers.get('content-type'))

    # # Cookies，如果HTTP响应中含有Cookies，可以很容易的访问
    # url = 'http://example.com/some/cookie/setting/url'
    # r = requests.get(url)
    # print(r.cookies['example_cookie_name'])
    # # 同时，使用cookies参数，也能发送带有cookies的请求
    # url = 'http://httpbin.org/cookies'
    # cookies = dict(cookies_are='working')
    # r = requests.get(url, cookies=cookies)
    # print(r.text)

    # # 重定向和历史记录, 只对HEAD无效
    # r = requests.get('http://github.com')
    # print(r.url)
    # print(r.status_code)
    # print(r.history)
    # # 禁止重定向
    # r = requests.get('http://github.com', allow_redirects=False)
    # print(r.status_code)
    # print(r.history)
    # # 当使用HEAD的时候，也可以激活重定向
    # r = requests.head('http://github.com', allow_redirects=True)
    # print(r.url)
    # print(r.history)

    # 超时设置
    # requests.get('http://github.com', timeout=0.001)

    # 错误和异常
    # 出现网络错误，如DNS错误，拒绝连接等，抛出ConnectionError异常
    # 非法的响应，抛出 HTTPError异常
    # 超时，抛出Timeout 异常
    # 重定向次数超过配置的最大数，抛出TooManyRedirects异常
    # 所有异常的均集成自requests.exceptions.RequestException.
    pass


if __name__ == '__main__':
    quick()

