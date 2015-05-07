#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 一个简单的日志解析工具
Desc :
日志格式如下：
* 客户端IP地址
* 客户标识：通常不可靠，可以不记录
* 认证用户名：如果无需认证也没有
* 请求接受时间：包括日期、时间、地区
* 请求内容：进一步划分为：方法、资源、请求参数、协议
* 状态码：HTTP状态码
* 返回对象大小：byte为单位
* 提交方Referrer：通常是连接到Web页面或资源的URI或URL
* 用户代理User Agent：客户端程序比如Mozilla、Chrome等
"""
import re
import inspect
from pymongo import Connection

LINE_REGEX = re.compile(r'(\d+\.\d+\.\d+\.\d+) ([^ ]*) ([^ ]*) '
                        r'\[([^\]]*)\] "([^"]*)" (\d+) ([^ ]*) '
                        r'"([^"]*)" "([^"]*)"')


class ApacheLogRecord():
    def __init__(self, *rgroups):
        self.ip, self.ident, \
        self.http_user, self.time, \
        self.request_line, self.http_response_code, \
        self.http_response_size, self.referrer, \
        self.user_agent = rgroups
        self.http_method, self.url, self.http_vers = self.request_line.split()

    def __str__(self):
        return ' '.join([self.ip, self.ident, self.time, self.request_line,
                         self.http_response_code, self.http_response_size,
                         self.referrer, self.user_agent])


class ApacheLogFile():
    def __init__(self, logfile):
        self.filename = logfile

    def my_generator(self):
        _match = LINE_REGEX.match
        print(self.filename)
        with open(self.filename, encoding='utf-8') as f:
            for line in f:
                m = _match(line)
                if m:
                    print(line)
                    try:
                        log_line = ApacheLogRecord(*m.groups())
                        yield log_line
                    except GeneratorExit:
                        pass
                    except Exception as e:
                        print('NON_COMPLIANT_FORMAT: ', line, 'Exception: ', e)


def props(ob):
    pr = {}
    for name in dir(ob):
        val = getattr(ob, name)
        if not name.startswith('__') and not inspect.ismethod(val):
            pr[name] = val
    return pr


def insert_log():
    connection = Connection('localhost', 27017)
    db = connection.mydb
    collection = db.logdata
    alf = ApacheLogFile(r'D:\work\gitproject\python3-cookbook\configs\app.log')
    for lg_line in alf.my_generator():
        collection.insert(props(lg_line))


def query_log():
    connection = Connection('localhost', 27017)
    db = connection.mydb
    collection = db.logdata
    for doc in collection.find():
        print(doc)
    connection.close()


if __name__ == '__main__':
    """"""
    query_log()
