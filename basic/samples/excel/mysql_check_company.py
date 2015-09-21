#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: 检查企业数据哪些已经在我们数据库里面
"""
import sys
import copy

import logging
import datetime
import mysql.connector
from mysql.connector import errorcode

# 查询航信CRM表
sql_select_name = """
SELECT COUNT(*) FROM t_crm_company
WHERE cust_name='{}' OR cust_tax_name='{}';
"""

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    handlers=[logging.FileHandler('d:/logs/merge_table.log', 'a', 'utf-8')])
_log = logging.getLogger('app.' + __name__)


def _connect():
    config = {
        'user': 'root',
        'password': 'mysql',
        'host': '192.168.203.95',
        'database': 'fastloan_test',
        'raise_on_warnings': True,
    }
    cnx = None
    try:
        cnx = mysql.connector.connect(**config)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
        if cnx:
            cnx.close()
    return cnx


def check_table():
    conn_ = _connect()
    _log.info('---------------------------分割线-----------------------------')
    cursor = conn_.cursor()

    data_yes = []
    data_no = []
    for idx in [1, 2, 3]:
        data_file = r'D:\work\projects\gitprojects\python3-cookbook\basic\samples\excel\data{}.txt'.format(idx)
        data_file_y = r'D:\work\projects\gitprojects\python3-cookbook\basic\samples\excel\data{}y.txt'.format(idx)
        data_file_n = r'D:\work\projects\gitprojects\python3-cookbook\basic\samples\excel\data{}n.txt'.format(idx)
        with open(data_file, encoding='utf-8') as f:
            for tline in f:
                tline = tline.strip()
                if tline:
                    cursor.execute(sql_select_name.format(tline, tline))
                    count_num = cursor.fetchone()[0]
                    if count_num > 0:
                        data_yes.append(tline + "\n")
                    else:
                        data_no.append(tline + "\n")
        with open(data_file_y, mode='w', encoding='utf-8') as f:
            f.writelines(data_yes)
        with open(data_file_n, mode='w', encoding='utf-8') as f:
            f.writelines(data_no)
        data_yes.clear()
        data_no.clear()

    cursor.close()
    conn_.close()


if __name__ == '__main__':
    check_table()
    pass
