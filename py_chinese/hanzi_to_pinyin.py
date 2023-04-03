#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# Created on 2023-04-03
import configparser
import pymysql.cursors
from xpinyin import Pinyin

pinyinConverter = Pinyin()
dbConfig = configparser.ConfigParser()
dbConfig.read('./app.ini')

db = pymysql.connect(host=dbConfig.get('db', 'host'),
                     user=dbConfig.get('db', 'user'),
                     passwd=dbConfig.get('db', 'password'),
                     db=dbConfig.get('db', 'schema'),
                     use_unicode=dbConfig.getboolean('db', 'use_unicode'),
                     charset=dbConfig.get('db', 'charset'))


def getNeedToUpdateRows():
    # 使用字典游标遍历
    with pymysql.cursors.DictCursor(db) as cur:
        querySql = "SELECT * FROM sys_user WHERE dept_id = 101 "
        cur.execute(querySql)
        rows = cur.fetchall()
        return rows


def update_rows():
    rows = getNeedToUpdateRows()
    for row in rows:
        row_dict = {key: val for key, val in row.items() if key in [
            'user_id', 'user_name']}
        user_no_pinyin = pinyinConverter.get_pinyin(row_dict['user_name'], '')
        update_params = (user_no_pinyin, row_dict['user_id'])
        with db.cursor() as cursor:
            # Update a record
            sql = "UPDATE sys_user SET user_no = %s WHERE user_id = %s"
            print(sql % update_params)
            cursor.execute(sql, update_params)

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        db.commit()


if __name__ == "__main__":
    try:
        update_rows()
    except Exception as e:
        print('Handling run-time error:', e)
        print(e.args)
