#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 认证
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
from requests.auth import HTTPDigestAuth
from requests_oauthlib import OAuth2


def auth():
    # Basic Authentication
    requests.get('https://api.github.com/user', auth=HTTPBasicAuth('user', 'pass'))
    requests.get('https://api.github.com/user', auth=('user', 'pass'))

    # Digest Authentication
    url = 'http://httpbin.org/digest-auth/auth/user/pass'
    requests.get(url, auth=HTTPDigestAuth('user', 'pass'))

    # OAuth2 Authentication，先安装requests-oauthlib
    url = 'https://api.twitter.com/1.1/account/verify_credentials.json'
    auth = OAuth2('YOUR_APP_KEY', 'YOUR_APP_SECRET', 'USER_OAUTH_TOKEN')
    requests.get(url, auth=auth)



    pass

if __name__ == '__main__':
    auth()



