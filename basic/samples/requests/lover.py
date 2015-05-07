#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 每天一句情话
"""
import requests
import re
from io import StringIO
import json
import xml.etree.ElementTree as ET


def extract_content(xml):
    """xpath解析，或者使用lxml库"""
    doc = ET.fromstring(xml)
    tt= doc.findall("//div[@class='articleText']")
    print(tt)


def lover_sentences_01():
    """获取情话网的情话列表！"""
    urls = ['http://www.siandian.com/qinghua/510.html',
            'http://www.siandian.com/qinghua/510_2.html',
            'http://www.siandian.com/qinghua/1608.html']
    for url in urls:
        # 读取返回结果
        r = requests.get(url)
        # 改变r.encoding
        encoding = re.search('content="text/html;\s*charset=(.*?)"', r.text).group(1)
        r.encoding = encoding
        finds = re.finditer(r'<p>\s*(((?!</).)+)\s*</p>', r.text)
        for f in finds:
            print(f.group(1))


if __name__ == '__main__':
    lover_sentences_01()
