#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
    Topic: mango的组件监控需求，从Java源代码中获取组件类型，然后每次插入两行数据
    Desc : 通过这个脚本熟悉下python对pgsql数据库的操作
"""
import re
import os
import sys
import psycopg2

def init_data(top_dir):
    """
    top_dir: 存放组件模型的目录
    """
    all_types = set()  # 所有组件类型
    for path, dirs, files in os.walk(top_dir):
        for each_file in files:
            if each_file.endswith('.java'):
                full_name = os.path.join(path, each_file)
                print('开始处理:%s' % full_name)
                patt_type = re.compile(r'^@MetricClass\(type\s*=\s*"(.+)"\)')
                with open(full_name, mode='r', encoding='utf-8') as f:
                    for tline in f:
                        tline = tline.strip()
                        if re.match(patt_type, tline):
                            all_types.add(re.match(patt_type, tline).group(1))
                            break
    print('split'.center(100, '*'))

    #--------------开始操作数据库了----------------------
    con = None
    try:
        con = psycopg2.connect(database='mango15', user='postgres',
                               password='postgres', host='10.0.0.175', port=5432)
        cur = con.cursor()
        cur.execute("delete from metric_domain where mkey in ('cpu', 'mem')")
        my_datas = []
        key_indx = 30
        for each_type in all_types:
            my_datas.append((key_indx, each_type, 'cpu', 'cpu', 0.9))
            my_datas.append((key_indx + 1, each_type, 'mem', 'mem', 1024000))
            key_indx += 2
        insert_sql = "insert into metric_domain values (%s, %s, %s, %s, %s)"
        cur.executemany(insert_sql, my_datas)
        con.commit()

    except psycopg2.DatabaseError as e:
        if con:
            con.rollback()
        print('Error is %s' % e)
    finally:
        if con:
            con.close()


if __name__ == '__main__':
    init_data(top_dir=r'D:\work\projects\trunck\cloudfoundry-client-lib\src\main'
                      r'\java\org\cloudfoundry\client\lib\monitor\templates')