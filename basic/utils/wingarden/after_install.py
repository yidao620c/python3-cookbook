#!/usr/bin/env python
# -*- encoding: utf-8 -*-
"""
Topic: sample
Desc : 
"""
import psycopg2
import sys

def clear_static_routes(host, port, user, passwd):
    # --------------开始操作数据库了----------------------
    con = None
    try:
        con = psycopg2.connect(database='cloud_controller', user=user,
                               password=passwd, host=host, port=port)
        cur = con.cursor()
        cur.execute('delete from static_routes')
        con.commit()

    except psycopg2.DatabaseError as e:
        if con:
            con.rollback()
        print('Error is %s' % e)
    finally:
        if con:
            con.close()

def update_redirect_url(host, port, user, passwd, domain_name):
    # --------------开始操作数据库了----------------------
    con = None
    try:
        con = psycopg2.connect(database='uaa', user=user,
                               password=passwd, host=host, port=port)
        cur = con.cursor()
        cur.execute("update oauth_client_details set"
                    " web_server_redirect_uri='http://uaa.cloudfoundry.com/redirect/vmc,"
                    "https://uaa.cloudfoundry.com/redirect/vmc,"
                    "http://uaa.%s/redirect/vmc,https://uaa.%s/redirect/vmc'"
                    " where client_id in ('simple', 'vmc')" % (domain_name, domain_name))
        con.commit()

    except psycopg2.DatabaseError as e:
        if con:
            con.rollback()
        print('Error is %s' % e)
    finally:
        if con:
            con.close()

if __name__ == '__main__':
    if len(sys.argv) != 6:
        print('usage: python after_install.py host port user passwd domain')
        exit(1)
    clear_static_routes(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    update_redirect_url(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])
