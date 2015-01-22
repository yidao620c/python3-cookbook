#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: sample
Desc : 
"""
import examples.zupload as zupload
import logging.config
import commons.util as cutil
import tempfile
# logging.basicConfig(level=logging.DEBUG, filename=tempfile.TemporaryFile().name)
logging.basicConfig(level=logging.INFO,
                    filename=cutil.userhome_file('ztool.log'),
                    format='%(asctime)s %(message)s')
# 采用配置文件
# logging.config.fileConfig(cutil.resource_path("resources/logging.conf"))

if __name__ == '__main__':
    zupload.main()
