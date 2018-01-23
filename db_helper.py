#!/usr/bin/env python
# -*- coding:utf-8 -*-

'''
Created on 2018年01月19日

@author: liuganglei
'''

import traceback
import logging
import sqlite3
# import MySQLdb
# import pymysql
import mysql.connector

logger = logging.getLogger("page")


def getConnection():
    try:

        conn = mysql.connector.connect(
            host='192.168.10.201',
            user="scorpion",
            port=3306,
            passwd="CM$ecThreat#2015",
            database="xdrygk",
            charset="utf8")
        return conn
    except Exception, e:
        logger.error(traceback.format_exc())


# def getConnection():
#     try:
#         conn = sqlite3.connect(r"C:\lgl\py_wk\drug_special\test.db")
#         return conn
#     except Exception, e:
#         logger.error(traceback.format_exc())


# def getConnection():
#     try:
#         conn = pymysql.connect(
#             host='192.168.10.201',
#             port=3306,
#             user='scorpion',
#             password='CM$ecThreat#2015',
#             db='xdrygk',
#             charset='utf8'
#         )
#         return conn
#     except Exception, e:
#         logger.error(traceback.format_exc())
#
#
# def getConnection():
#     try:
#         conn = MySQLdb.connect(
#             host="192.168.10.201",
#             port=3306,
#             user="scorpion",
#             passwd="CM$ecThreat#2015",
#             db="xdrygk",
#             charset="utf8"
#         )
#         return conn
#     except Exception, e:
#         logger.error(traceback.format_exc())

def executeSqlOri(cursor, sql):
    re = cursor.execute(sql)
    return re


def executeSql(sql):
    try:
        connection = getConnection()
        cursor = connection.cursor()
        re = cursor.execute(sql)  # update返回更新的列数，select返回查到的结果个数，delete返回删除的个数，insert返回增加的个数
        return re
    except Exception, e:
        logging.error(traceback.format_exc())
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def dictfetchall(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
        ]


def fetchallJson(sql):
    try:
        connection = getConnection()
        cursor = connection.cursor()
        cursor.execute(sql)
        re = dictfetchall(cursor)
        return re
    except Exception, e:
        logging.error(traceback.format_exc())
        return []
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def fetchoneJson(sql):
    try:
        connection = getConnection()
        cursor = connection.cursor()
        cursor.execute(sql)
        re = dictfetchall(cursor)
        if re:
            re = re[0]
        return re
    except Exception, e:
        logging.error(traceback.format_exc())
        return None
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


if __name__ == "__main__":
    print getConnection()
