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


# from getIpInfo import filter_proxy

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




import re

import threading


def get_info_from_html(html):
    pattern = re.compile(r'<div class="well">.*?</div>')
    match = pattern.search(html)
    if match:
        tmp = match.group()
        p1 = re.compile(r'<p>.*?</p>')
        ll = p1.findall(tmp)
        if tmp.find("<a href=") > -1:
            del ll[2]
        target = ""
        for index, l in enumerate(ll):
            t = l.replace('<p>', '').replace('</p>', '').replace('<code>', '').replace('</code>', '')
            if index == 0:
                target += t.split("：")[1].strip()
            if index == 1:
                t = t = t.decode("utf-8").encode("utf-8")
                target += "," + t.split("：")[1].strip()  # .decode().encode("utf8")
                # print chardet.detect(target)
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


def is_proxy_available(ip, port, http_proxy="http"):
    try:
        if http_proxy == None:
            http_proxy = "http"
        proxy = {
            "{http_proxy}".format(http_proxy=http_proxy.lower()): "{http_proxy}://{ip}:{port}".format(ip=ip, port=port,
                                                                                                      http_proxy=http_proxy.lower())}
        url = "http://ip.cn/index.php?ip=" + ip
        res = requests.get(url, proxies=proxy, verify=False)
        html = res.content
        soup = BeautifulSoup(html)
        result_ll = soup.findAll("div", {"class": "well"})
        if res.status_code == 200 and len(result_ll) != 0:
            print "normal proxy ip:{ip}".format(ip=ip)
            # write_proxy_txt(ip + '\t' + port + '\n')
            write_proxy_txt(ip + '\t' + port + '\t' + http_proxy + '\n')
        elif len(result_ll) == 0:
            print "unavailable proxy ip:{ip}".format(ip=ip)
        else:
            print "exception code proxy ip:{ip}".format(ip=ip)
    except Exception, e:
        print "exception proxy ip:{ip}".format(ip=ip)


from threadpool import ThreadPool
from threadpool import makeRequests

path_root = "c:/ip_info"


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
            line = line.strip()
            http = None
            if line.find(":") > 0:
                ip = line.split(":")[0]
                port = line.split(":")[1].split()[0]
            elif len(line.split()) == 3:
                ip = line.split()[0]
                port = line.split()[1]
                http = line.split()[2]
            elif len(line.split()) == 2:
                ip = line.split()[0]
                port = line.split()[1]
            if ip in ss:
                continue
            else:
                ss.add(ip)
            ll.append((ip, port, http))
        print "proxy num is:" + str(len(ll))
        pool = ThreadPool(300)
        requests_pool = makeRequests(is_proxy_available, [([l[0], l[1], l[2]], None) for l in ll])
        [pool.putRequest(req) for req in requests_pool]
        pool.wait()
        # for l in ll:
        #     is_proxy_available(l[0], l[1], l[2])


def filter_proxy_test():
    filter_proxy()


write_file_count = 0
starttime = None

write_locak = threading.RLock()


def convert_soup_html(html):
    soup = BeautifulSoup(html)
    result_ll = soup.findAll("div", {"class": "well"})
    target = ""
    if len(result_ll) == 0:
        return
    else:
        target1 = result_ll[0]
    for index, c in enumerate(target1):
        if index == 1:
            target += c.text.split(u"：")[1]
        elif c.text.find("GeoIP") > -1:
            ll = c.text.split(":")[1].split(",")
            target = target + "," + " ".join([s.split()[0] for s in ll])
            continue
        elif index == 3 and c.text.find("GeoIP") == -1:
            target = target + "," + c.text
        elif index == 4:
            target = target + "," + c.text
    target = "" + "," + target
    target = target.encode("utf8")


def test_open_file():
    while True:
        str1 = """
        <!DOCTYPE html>
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<link href="http://s.ip-cdn.com" rel="dns-prefetch" />
<title>47.71.10.0 - IP.cn - IP 地址查询 | 地理位置 | 手机归属地</title>
<meta name="robots" content="all" />
<meta name="Keywords" content="ip,ip查询,手机ip,本机ip,外网ip,ip地址查询,手机号,归属地,47.71.10.0">
<meta name="Description" content="专业本机 IP 地址查询、手机 IP 地址、地理位置查询、IP 数据库、手机号归属地查询、电话号码黄页查询，可查广告、骚扰、快递、银行、保险、房地产、中介电话。">
<link href='http://s.ip-cdn.com/css/bootstrap.min.css' rel='stylesheet' type='text/css'>
<meta name="viewport" content="width=device-width, minimum-scale=0.5">
<meta name="format-detection" content="telephone=no">
<!--[if lt IE 8]>
<script src="http://s.ip-cdn.com/js/ie8.js"></script>
<![endif]-->
<link href='http://s.ip-cdn.com/css/main.css' rel='stylesheet' type='text/css'>
</head>
<body onLoad="document.fs.ip.focus()">
<div class="container-fluid">
	<div class="header">
		<a href="/"><img src="http://s.ip-cdn.com/img/logo.gif"></a>
	</div>

	<div class="mainbar">
		<ul class="nav nav-pills center-pills">
			<li class="active"><a href="/">IP 查询</a></li>
			<li><a href="db.php">手机、电话号码数据库</a></li>
			<li><a href="dns.html">DNS</a></li>
			<li><a href="chnroutes.html">IP 列表</a></li>
		</ul>
	</div>

	<div class="searchform">
		<form name="fs" action="index.php" method="GET" class="form-search">
			<input name="ip" type="text" placeholder="请输入要查询的域名或 IP 地址" class="span3">
			<input id="s" type="submit" class="btn btn-primary" value="查询">
		</form>
	</div>

	<div id="result"><div class="well"><p>您查询的 IP：<code>47.71.10.0</code></p><p>所在地理位置：<code>德国 </code></p><p>GeoIP: V�hl, Hessen, Germany</p><p>Vodafone D2 GmbH</p></div></div>

        <div width="100%" align="center">
		<div name="dashmain" id="dash-main-id-87884f" class="dash-main-2 87884f-9.9"></div><script type="text/javascript" charset="utf-8" src="http://www.dashangcloud.com/static/ds.js"></script>
        </div>
	<div class="footer">
		<p>©2006-2017 IP.cn <a href="http://www.miitbeian.gov.cn/" target="_blank">沪ICP备15005128号-3</a> <script src="http://s19.cnzz.com/stat.php?id=123770&web_id=123770" language="JavaScript"></script></p>
	</div>
</div>
</body>
</html>

        """
        get_info_from_html(str1)
        # convert_soup_html(str1)

        write_locak.acquire()
        global write_file_count
        path = r"C:\temp\ip_info\proxy.txt"
        with open(path, "w") as f:
            f.write("")
        with open(path, "a") as f:
            f.write("1")
        write_file_count += 1

        if write_file_count == 1000:
            endtime = datetime.datetime.now()
            print "elapse time: " + str((endtime - starttime).seconds) + " seconds"
        write_locak.release()


def test_main():
    global starttime
    starttime = datetime.datetime.now()
    # for i in range(10000):
    #     test_open_file()
    thread_num = 100
    for i in range(thread_num):
        tmp = threading.Thread(target=test_open_file)
        tmp.setDaemon(False)
        tmp.start()


if __name__ == '__main__':
    pass
    print "0,16777215,,".split(",")
    print "16777216,16777471,澳大利亚,".split(",")
    print "16777472,16778239,福建省,电信".split(",")

    # test_main()
    #     str = """
    #     <!DOCTYPE html>
    # <html>
    # <head>
    # <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    # <link href="http://s.ip-cdn.com" rel="dns-prefetch" />
    # <title>4.122.141.0 - IP.cn - IP 地址查询 | 地理位置 | 手机归属地</title>
    # <meta name="robots" content="all" />
    # <meta name="Keywords" content="ip,ip查询,手机ip,本机ip,外网ip,ip地址查询,手机号,归属地,4.122.141.0">
    # <meta name="Description" content="专业本机 IP 地址查询、手机 IP 地址、地理位置查询、IP 数据库、手机号归属地查询、电话号码黄页查询，可查广告、骚扰、快递、银行、保险、房地产、中介电话。">
    # <link href='http://s.ip-cdn.com/css/bootstrap.min.css' rel='stylesheet' type='text/css'>
    # <meta name="viewport" content="width=device-width, minimum-scale=0.5">
    # <meta name="format-detection" content="telephone=no">
    # <!--[if lt IE 8]>
    # <script src="http://s.ip-cdn.com/js/ie8.js"></script>
    # <![endif]-->
    # <link href='http://s.ip-cdn.com/css/main.css' rel='stylesheet' type='text/css'>
    # </head>
    # <body onLoad="document.fs.ip.focus()">
    # <div class="container-fluid">
    # 	<div class="header">
    # 		<a href="/"><img src="http://s.ip-cdn.com/img/logo.gif"></a>
    # 	</div>
    #
    # 	<div class="mainbar">
    # 		<ul class="nav nav-pills center-pills">
    # 			<li class="active"><a href="/">IP 查询</a></li>
    # 			<li><a href="db.php">手机、电话号码数据库</a></li>
    # 			<li><a href="dns.html">DNS</a></li>
    # 			<li><a href="chnroutes.html">IP 列表</a></li>
    # 		</ul>
    # 	</div>
    #
    # 	<div class="searchform">
    # 		<form name="fs" action="index.php" method="GET" class="form-search">
    # 			<input name="ip" type="text" placeholder="请输入要查询的域名或 IP 地址" class="span3">
    # 			<input id="s" type="submit" class="btn btn-primary" value="查询">
    # 		</form>
    # 	</div>
    #
    # 	<div id="result"><div class="well"><p>您查询的 IP：<code>4.122.141.0</code></p><p>所在地理位置：<code>美国 Level3</code></p><p>GeoIP: United States</p><p>Level 3 Communications</p></div></div>
    #
    #         <div width="100%" align="center">
    # 		<div name="dashmain" id="dash-main-id-87884f" class="dash-main-2 87884f-9.9"></div><script type="text/javascript" charset="utf-8" src="http://www.dashangcloud.com/static/ds.js"></script>
    #         </div>
    # 	<div class="footer">
    # 		<p>©2006-2017 IP.cn <a href="http://www.miitbeian.gov.cn/" target="_blank">沪ICP备15005128号-3</a> <script src="http://s19.cnzz.com/stat.php?id=123770&web_id=123770" language="JavaScript"></script></p>
    # 	</div>
    # </div>
    # </body>
    # </html>
    #
    #
    #     """
    #     xxx = "Nicaragua,estaci󮠤e servicio Comarca Aul�"
    #     print chardet.detect(xxx)
    #     i = 0
    # print get_info_from_html(str)
    # ip = "47.71.10.0"
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

    # for i in get_ip_from_file():
    #     print i

    # proxy = "http://111.13.7.119:80"
    # get_address(ip, proxy)
    # time.sleep(10)
    # filter_proxy_test()
