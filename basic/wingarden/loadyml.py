#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: sample
Desc : yaml文件解析
"""
import yaml
import os.path as op
import sys

def main(key):
    # 相对于当前脚本文件的路径op.split(op.realpath(__file__))[0]
    with open(op.join(op.split(op.realpath(__file__))[0], 'ip_config.yml'),
              encoding='utf-8') as f:
        configs = yaml.load(f)
    ip_value = configs[key]
    if type(ip_value) is str:
        print(configs[key])
    else:
        for ip in configs[key]:
            print(ip, end=' ')

if __name__ == '__main__':
    main(sys.argv[1])

