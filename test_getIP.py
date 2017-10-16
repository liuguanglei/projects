#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import traceback
import chardet
import socket
import struct

from BeautifulSoup import BeautifulSoup
from bs4 import UnicodeDammit


# from bs4 import UnicodeDammit

def get_address(ip=None, proxy=None):
    try:
        url = "http://ip.cn/index.php?ip=" + ip
        # print "begin request d ip:{ip},proxy:{proxy}".format(ip=ip, proxy=proxy)
        res = requests.get(url, proxies={"http": proxy})
        print res.encoding
        if res.status_code != 200:
            return
        html = res.content

        import urllib2
        response = urllib2.urlopen(url)
        html = response.read()

        with open("c://test_xxx.txt", "w") as f:
            f.write(html)
        dammit = UnicodeDammit(html)
        print dammit.original_encoding
        print chardet.detect(html)
        tmp = html.decode("UTF-8")
        tmp1 = tmp.encode("utf-8")
        soup = BeautifulSoup(html, fromEncoding=dammit.original_encoding)
        target = ""
        target1 = soup.findAll("div", {"class": "well"})[0]
        for index, c in enumerate(target1):
            if index == 1:
                # print "chardet:" + chardet.detect(c.text)
                target += c.text.split(u"：")[1]
            elif c.text.find("GeoIP") > -1:
                ll = c.text.split(":")[1].split(",")
                target = target + "," + " ".join([s.split()[0] for s in ll])
                continue
            elif index == 3 and c.text.find("GeoIP") == -1:
                target = target + "," + c.text
            elif index == 4:
                target = target + "," + c.text
        target = ip + "," + target
        print target
    except requests.exceptions.ProxyError, e:
        print traceback.format_exc()
    except IndexError, e:
        print traceback.format_exc()
    except Exception, e:
        print traceback.format_exc()
    finally:
        pass


import MySQLdb
import time
import os

DB = {
    'host': '192.168.10.201',
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


def convet_int2Ip(int_ip):
    return socket.inet_ntoa(struct.pack('!L', int_ip))


def convert_ip2Int(ip):
    return socket.ntohl(struct.unpack("I", socket.inet_aton(str(ip)))[0])


def convert_to_next_d(int_ip):
    result = ""
    tmp = int_ip + 256
    tmp1 = tmp % 256
    tmp = tmp - tmp1
    result = convet_int2Ip(tmp)
    return result


def calculate_step_ip(int_ip_start, int_ip_end):
    ll = []
    while int_ip_start < int_ip_end:
        ll.append(convert_to_next_d(int_ip_start))
        int_ip_start = int_ip_start + 256
    return ll[:-1]


def checkContinuity():
    print u'======== 开始判断地址段的连续性 ========'
    timeStart = time.time()
    resNum = 0
    conn = getMySQLConnection()
    cur = conn.cursor()
    sql = "SELECT `IP_START`, `IP_END` FROM KB_IP_ADDRESS ORDER BY IP_START,IP_END"

    path = "c:/ip_info/z_all_need_req_ip.txt"
    count = cur.execute(sql)
    print 'find %d records' % count
    if count:
        res = cur.fetchall()
        result = []
        data = None
        for index, d in enumerate(res):
            if index % 10000 == 0:
                print index

            item = {}
            item['IP_START'] = d[0]
            item['IP_END'] = d[1]
            if data and data['IP_END'] + 1 == item['IP_START']:
                pass
            else:
                if data:
                    d_tmp_list = calculate_step_ip(data['IP_END'], item['IP_START'])
                    result += d_tmp_list
                    resNum += 1
            data = item
        for index, line in enumerate(result):
            result[index] = line + "\n"
        with open(path, "w") as f:
            f.writelines(result)
    cur.close()
    conn.close()
    print '%d 条数据存在不连续性' % resNum

    timeEnd = time.time()
    print u'\n\n\n==================处理结束 耗时 %f 秒 =================\n\n\n' % (timeEnd - timeStart)


def get_ip_from_file():
    # TODO add thread lock
    path = "c:/ip_info/z_all_need_req_ip.txt"
    path1 = "c:/ip_info/ip_count_flag_from_file.txt"
    count_index_file = None
    if os.path.exists(path1) is False:
        count_index_file = None
    else:
        with open(path1, "r") as f:
            count_index_file = f.read()
    with open(path, "r") as f:
        for index, line in enumerate(f):
            if count_index_file is not None and index <= int(count_index_file):
                pass
            else:
                with open(path1, "w") as f1:
                    f1.write(str(index))
                yield line


if __name__ == '__main__':
    ip = "47.71.10.0"
    # ip = "111.198.57.237"
    dammit = UnicodeDammit(ip)
    print dammit.original_encoding
    tmp = ip.decode(dammit.original_encoding)
    # print convet_int2Ip(3756722688)
    # print convert_ip2Int("223.235.10.0")
    # print convert_ip2Int(ip)
    # print convert_ip2Int(ip)
    # print convert_to_next_d(convert_ip2Int(ip))
    # print calculate_step_ip(3756781567, 3756797440)
    # print convert_ip2Int("255.255.255.0")
    # checkContinuity()

    # for i in get_ip_from_file():
    #     print i

    proxy = "http://111.13.7.119:80"
    get_address(ip, proxy)
    time.sleep(10)
