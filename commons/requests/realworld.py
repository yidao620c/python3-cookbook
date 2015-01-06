#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 实战演练
"""
import requests
import re
from io import StringIO
import json
from requests import Request, Session
from contextlib import closing
from requests.auth import AuthBase
from requests.auth import HTTPBasicAuth
from requests.auth import HTTPDigestAuth
import xml.etree.ElementTree as ET


def xpath_demo():
    """xpath解析，或者使用lxml库"""
    xml = """..."""
    doc = ET.fromstring(xml)
    doc.findall("//rank")


def whu_bbs():
    """登录BBS系统，查看一篇文章，试着去回复一下！"""
    url = 'http://bbs.whu.edu.cn/bbslogin.php'
    payload = {
        'id': 'yidaojiba',
        'passwd': '620817',
        'webtype': 'wforum'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'
                      ' AppleWebKit/537.36 (KHTML, like Gecko)'
                      ' Chrome/38.0.2125.101 Safari/537.36'
    }
    with requests.Session() as s:
        r = s.post(url, data=payload, headers=headers)
        print(r.headers)
        # An authorised request.
        r = s.get('http://bbs.whu.edu.cn/wForum/disparticle.php'
                  '?boardName=Badminton&ID=1103391298&pos=14')
        print(r.encoding)
        r.encoding = 'gb2312'
        print(r.text)

if __name__ == '__main__':
    whu_bbs()


