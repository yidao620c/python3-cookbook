#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: 从java源代码中提取国际化的消息
    Desc : 
"""
import re
import os

def i18n_extract(top_dir):
    i18n_chinese = dict()  # 中文国际化消息
    i18n_english = dict()  # 英文国际化消息
    for path, dirs, files in os.walk(top_dir):
        for each_file in files:
            if each_file.endswith('.java'):
                full_name = os.path.join(path, each_file)
                print('开始处理:%s' % full_name)
                f = open(full_name, mode='r', encoding='utf-8')
                datas = f.readlines()
                f.close()
                anno = '@MetricField'
                patt_type = re.compile(r'^@MetricClass\(type\s*=\s*"(.+)"\)')
                patt1 = re.compile(r'^@MetricField\(.*key = "(\w+)".*\)')
                patt2 = re.compile(r'^\*\s*(\S+)')
                patt3 = re.compile(r'.*?(\w+);$')
                pre_type = ''
                for tline in datas:
                    tline = tline.strip()
                    if re.match(patt_type, tline):
                        pre_type = re.match(patt_type, tline).group(1) + '_'
                        pre_type = pre_type.replace('-', '_')
                        break
                check = set()
                for idx, line in enumerate(datas):
                    simple_line = line.strip()
                    if anno in simple_line:
                        comment_line = datas[idx - 2].strip()
                        comment = re.match(patt2, comment_line).group(1)
                        if re.match(patt1, simple_line):
                            key = re.match(patt1, simple_line).group(1)
                            i18n_chinese[pre_type + key] = comment
                            i18n_english[pre_type + key] = key.replace('_', ' ')
                            # result.append('%s=%s' % (key, comment))
                            if key in check:
                                print('------------ERROR--------', key, full_name)
                                exit(-1)
                            else:
                                check.add(key)
                        else:
                            field_line = datas[idx + 1].strip()
                            filed_name = re.match(patt3, field_line).group(1)
                            i18n_chinese[pre_type + filed_name] = comment
                            i18n_english[pre_type + filed_name] = filed_name.replace('_', ' ')
                            # result.append('%s=%s' % (filed_name, comment))
                            if filed_name in check:
                                print('------------ERROR--------', filed_name, full_name)
                                exit(-1)
                            else:
                                check.add(filed_name)
    print('split'.center(100, '*'))
    i18n_chinese = sorted(i18n_chinese.items(), key=lambda ee: ee[0])
    i18n_english = sorted(i18n_english.items(), key=lambda ee: ee[0])
    return i18n_chinese, i18n_english


if __name__ == '__main__':
    i18n_chinese, i18n_english = i18n_extract(
        top_dir = r'D:\work\projects\trunck\cloudfoundry-client-lib\src\main'
                  r'\java\org\cloudfoundry\client\lib\monitor\templates')
    for k, v in i18n_chinese:
        print("%s=%s" % (k, v))
    print('split'.center(100, '*'))
    for k, v in i18n_english:
        print("%s=%s" % (k, v))