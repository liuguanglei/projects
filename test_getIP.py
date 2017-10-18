#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import traceback
import chardet
import socket
import struct
import datetime

from BeautifulSoup import BeautifulSoup
from bs4 import UnicodeDammit

def elapse(func):
    def deco(*args, **kwargs):
        starttime = datetime.datetime.now()
        func(*args, **kwargs)
        endtime = datetime.datetime.now()
        print "elapse time: " + str((endtime - starttime).seconds) + " seconds"

    return deco

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

        # import urllib2
        # headers = {'Connection': 'keep-alive',
        #            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        #            'X-Requested-With': 'XMLHttpRequest',
        #            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36',
        #            'Accept-Encoding': 'gzip, deflate',
        #            'Accept-Language': 'en-GB,en;q=0.8,zh-CN;q=0.6,zh;q=0.4'
        #            }
        # request = urllib2.Request(url, headers=headers)
        # response = urllib2.urlopen(request)
        # html = response.read()

        dammit = chardet.detect(html)["encoding"]
        if dammit.lower() != "UTF-8".lower():
            target = get_info_from_html(html)
            # print target
            # with open("c:/ttt.txt", "w") as f:
            #     f.write(target.decode())
        else:
            soup = BeautifulSoup(html, fromEncoding="ISO-8859-1")
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


import re

import threading


def get_info_from_html(html):
    pattern = re.compile(r'<div class="well">.*?</div>')
    match = pattern.search(html)
    if match:
        tmp = match.group()
        p1 = re.compile(r'<p>.*?</p>')
        ll = p1.findall(tmp)
        target = ""
        for index, l in enumerate(ll):
            t = l.replace('<p>', '').replace('</p>', '').replace('<code>', '').replace('</code>', '')
            if index == 0:
                target += t.split("：")[1].strip()
            if index == 1:
                t = t = t.decode("utf-8").encode("utf-8")
                target += "," + t.split("：")[1].strip()  # .decode().encode("utf8")
                print chardet.detect(target)
            if index == 2:
                t = t.decode("ISO-8859-1").encode("utf-8")
                ll = t.split(":")[1].strip().split(",")
                target += "," + " ".join([s.split()[0] for s in ll])
            if index == 3:
                target += "," + t.strip()
        return target
    else:
        return ""


lock10 = threading.RLock()


def write_proxy_txt(proxy_ip):
    path = path_root + "/proxy.txt"
    lock10.acquire()
    with open(path, "a") as f:
        f.write(proxy_ip)
    lock10.release()


def is_proxy_available(ip, port):
    try:
        proxy = {"http": "http://{ip}:{port}".format(ip=ip, port=port)}
        url = "http://ip.cn/index.php?ip=" + ip
        res = requests.get(url, proxies=proxy)
        html = res.content
        soup = BeautifulSoup(html)
        result_ll = soup.findAll("div", {"class": "well"})
        if res.status_code == 200 and len(result_ll) != 0:
            print "normal proxy ip:{ip}".format(ip=ip)
            write_proxy_txt(ip + '\t' + port + '\n')
        elif len(result_ll) == 0:
            print "unavailable proxy ip:{ip}".format(ip=ip)
        else:
            print "exception code proxy ip:{ip}".format(ip=ip)
    except Exception, e:
        print "exception proxy ip:{ip}".format(ip=ip)


from threadpool import ThreadPool
from threadpool import makeRequests

path_root = "c:/ip_info"

@elapse
def filter_proxy():
    path = path_root + "/proxy_ori.txt"
    lines = []
    if os.path.exists(path_root + "/proxy.txt"):
        os.remove(path_root + "/proxy.txt")

    ss = set()
    with open(path, "r") as f:
        lines = f.readlines()
        ll = []
        for line in lines:
            if line.find(":") > 0:
                ip = line.split(":")[0]
                port = line.split(":")[1].split()[0]
            elif len(line.split()) != 2:
                continue
            else:
                ip = line.split()[0]
                port = line.split()[1]
            if ip in ss:
                continue
            else:
                ss.add(ip)
            ll.append((ip, port))
        print "proxy num is:" + str(len(ll))

        pool = ThreadPool(200)
        requests_pool = makeRequests(is_proxy_available, [([l[0], l[1]], None) for l in ll])
        [pool.putRequest(req) for req in requests_pool]
        pool.wait()


if __name__ == '__main__':
    # str = u'<div id="result"><div class="well"><p>您查询的 IP：<code>47.71.10.0</code></p><p>所在地理位置：<code>德国 </code></p><p>GeoIP: V�hl, Hessen, Germany</p><p>Vodafone D2 GmbH</p></div></div></div>sss</div>'
    # print get_info_from_html(str)
    ip = "47.71.10.0"
    # ip = "111.198.57.237"
    # dammit = UnicodeDammit(ip)
    # print dammit.original_encoding
    # tmp = ip.decode(dammit.original_encoding)
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

    # proxy = "http://111.13.7.119:80"
    # get_address(ip, proxy)
    # time.sleep(10)
    filter_proxy()
    # print [1, 2, 3] * 5
