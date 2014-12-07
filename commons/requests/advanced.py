#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 高级主题
"""
import requests
import re
from PIL import Image
from io import StringIO
import json
from requests import Request, Session
from contextlib import closing
from requests.auth import AuthBase
from requests.auth import HTTPBasicAuth


def advanced():
    # # Session对象
    # with requests.Session() as s:
    #     s.get('http://httpbin.org/cookies/set/sessioncookie/123456789')
    #     r = s.get("http://httpbin.org/cookies")
    #     print(r.text) # '{"cookies": {"sessioncookie": "123456789"}}'
    #     s = requests.Session()
    #     s.auth = ('user', 'pass')
    #     s.headers.update({'x-test': 'true'})
    #     # both 'x-test' and 'x-test2' are sent
    #     s.get('http://httpbin.org/headers', headers={'x-test2': 'true'})
    #     # session中的值可以被方法中的覆盖，如果想移除某个参数，可以在方法中设置其值为None即可

    # # Request和Response对象
    # r = requests.get('http://en.wikipedia.org/wiki/Monty_Python')
    # # 访问服务器返回来的headers
    # print(r.headers)
    # # 访问我们发送给服务器的headers
    # print(r.request.headers)

    # # Prepared Requests，你想在发送给服务器之前对body或header加工处理的话
    # s = Session()
    # req = Request('GET', url,
    # data=data,
    #     headers=header
    # )
    # prepped = s.prepare_request(req)
    # # do something with prepped.body
    # # do something with prepped.headers
    # resp = s.send(prepped,
    #     stream=stream,
    #     verify=verify,
    #     proxies=proxies,
    #     cert=cert,
    #     timeout=timeout
    # )
    # print(resp.status_code)

    # # SSL证书认证，verify缺省为True
    # requests.get('https://kennethreitz.com', verify=True)
    # requests.get('https://github.com', verify=True)
    # requests.get('https://kennethreitz.com', cert=('/path/server.crt', '/path/key'))

    # # Body内容流
    # # 默认情况下，当你构造一个request的时候，response的body会自动下载，可以使用stream延迟下载
    # tarball_url = 'https://github.com/kennethreitz/requests/tarball/master'
    # r = requests.get(tarball_url, stream=True)  # 这时候只有响应的headers被下载，连接仍然未断开
    # if int(r.headers['content-length']) < TOO_LONG:
    #     content = r.content
    # # 接下来还能使用 Response.iter_content and Response.iter_lines来迭代读取数据
    # # 或者是urllib3.HTTPResponse at Response.raw.获取为解码的元素字节数据
    # # 更好的方法是下面的这样：
    # with closing(requests.get('http://httpbin.org/get', stream=True)) as r:
    #     if int(r.headers['content-length']) < TOO_LONG:
    #         content = r.content

    # # 流式上传模式，上传大文件不需要先将其读到内存中去
    # with open('massive-body', 'rb') as f:
    #     requests.post('http://some.url/streamed', data=f)

    # # 多文件POST上传提交
    # # <input type=”file” name=”images” multiple=”true” required=”true”/>
    # url = 'http://httpbin.org/post'
    # multiple_files = [('images', ('foo.png', open('foo.png', 'rb'), 'image/png')),
    #                   ('images', ('bar.png', open('bar.png', 'rb'), 'image/png'))]
    # r = requests.post(url, files=multiple_files)
    # print(r.text)
    #

    # # 自定义认证
    # requests.get('http://pizzabin.org/admin', auth=PizzaAuth('kenneth'))

    # # 流式请求
    # r = requests.get('http://httpbin.org/stream/20', stream=True)
    # for line in r.iter_lines():
    #     # filter out keep-alive new lines
    #     if line:
    #         print(json.loads(line.decode('utf-8')))

    # # 代理
    # proxies = {
    #   "http": "http://10.10.1.10:3128",
    #   "https": "http://10.10.1.10:1080",
    # }
    # 带基本认证的代理
    # proxies = {
    #     "http": "http://user:pass@10.10.1.10:3128/",
    # }
    # requests.get("http://example.org", proxies=proxies)

    # # Github提交示例
    # body = json.dumps({"body": "Sounds great! I'll get right on it!"})
    # url = "https://api.github.com/repos/kennethreitz/requests/issues/482/comments"
    # auth = HTTPBasicAuth('fake@example.com', 'not_a_real_password')
    # r = requests.post(url=url, data=body, auth=auth)
    # print(r.status_code)
    # content = r.json().decode('utf-8')
    # print(content['body'])

    # # Link Headers
    # url = 'https://api.github.com/users/kennethreitz/repos?page=1&per_page=10'
    # r = requests.head(url=url)
    # print(r.headers['link'])
    # print(r.links["next"])
    # print(r.links["last"])

    # # 超时，第一个是连接服务器的超时时间，第二个是下载超时时间。
    # r = requests.get('https://github.com', timeout=(3.05, 27))

    pass


class PizzaAuth(AuthBase):
    """Attaches HTTP Pizza Authentication to the given Request object."""
    def __init__(self, username):
        # setup any auth-related data here
        self.username = username

    def __call__(self, r):
        # modify and return the request
        r.headers['X-Pizza'] = self.username
        return r

if __name__ == '__main__':
    advanced()
