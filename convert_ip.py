import MySQLdb
import time
import os
import socket
import struct
import traceback
import datetime

from _mysql_exceptions import IntegrityError
from MySQLdb import escape_string


def elapse(func):
    def deco(*args, **kwargs):
        starttime = datetime.datetime.now()
        func(*args, **kwargs)
        endtime = datetime.datetime.now()
        print "elapse time: " + str((endtime - starttime).seconds) + " seconds"

    return deco


DB = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'scorpion',
    'passwd': 'CM$ecThreat#2015',
    'db': 'kb',
    'charset': 'utf8',
}


def getMySQLConnection():
    conn = MySQLdb.connect(
        host=DB['host'],
        port=DB['port'],
        user=DB['user'],
        passwd=DB['passwd'],
        db=DB['db'],
        charset=DB['charset']
    )
    return conn


def convert_int2Ip(int_ip):
    return socket.inet_ntoa(struct.pack('!L', int_ip))


def convert_ip2Int(ip):
    return socket.ntohl(struct.unpack("I", socket.inet_aton(str(ip)))[0])


def get_add_to_table_sql(line):
    arr = line.split(",")
    ip_start_str = arr[0]
    ip_start = convert_ip2Int(arr[0])
    ip_end = ip_start + 255
    ip_end_str = convert_int2Ip(ip_end)
    country = escape_string(arr[1])
    msg = ""
    msg1 = ""
    if len(arr) == 3:
        msg = escape_string(arr[2])
    elif len(arr) == 4:
        msg = escape_string(arr[2])
        msg1 = escape_string(arr[3])

    sql = "INSERT INTO `kb_ip_address_all` " \
          "VALUES ('{ip_start}', '{ip_end}', '0', '{country}', '', '', '0', '0', '{msg}', '', '', '{ip_start_str}', '{ip_end_str}','{msg1}');".format(
        ip_start=ip_start, ip_end=ip_end, country=country, msg=msg, ip_start_str=ip_start_str, ip_end_str=ip_end_str,
        msg1=msg1)

    return sql


@elapse
def add_to_table():
    path = "c:/ip_info/result/ip_info_"
    for i in range(2, 50):
        path_ = path + str(i) + ".txt"
        conn = getMySQLConnection()
        cur = conn.cursor()
        with open(path_, "r") as f:
            lines = f.readlines()
            for line in lines:
                sql = get_add_to_table_sql(line.strip())
                try:
                    cur.execute(sql)
                except IntegrityError, e:
                    print "IntegrityError sql:" + sql
                except Exception:
                    print traceback.format_exc()
        cur.close()
        conn.commit()
        conn.close()


if __name__ == '__main__':
    # print MySQLdb.escape_string("Seoul Seoul-t'ukpyolsi Korea Republic".encode('utf-8'))
    add_to_table()
