#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json

from threadpool import makeRequests
from threadpool import ThreadPool
from BeautifulSoup import BeautifulSoup


def get_address(ip):
    url = "http://ip.cn/index.php?ip=" + ip
    re = requests.get(url)
    html = re.content
    soup = BeautifulSoup(html)
    print soup.findAll('code')
    # target = soup.findAll('code')[1].text
    # print target


ip_addr = {}


def get_address1(ip):
    if ip_addr.has_key(ip):
        return

    global ip_addr
    url = "http://ip.cn/index.php?ip=" + ip
    re = requests.get(url)
    html = re.content
    soup = BeautifulSoup(html)
    addr = soup.findAll('code')[1].text
    print ip, addr

    ip_addr[ip] = addr


def get_ip_from_json():
    path = "c:\\temp\\111111.json"
    json_str = ""
    with open(path, "rb") as f:
        json_str = f.read()

    ips = []

    objs = json.loads(json_str)
    for obj in objs:
        ip = obj["_source"]["layers"]["ip"]["ip.src"]
        if ip not in ips:
            ips.append(ip)

    ips = ["201.247.40.134"]

    size = 3
    pool = ThreadPool(size)
    reqs = makeRequests(get_address1, [([ip], None) for ip in ips])
    [pool.putRequest(req) for req in reqs]
    pool.wait()

    # to file
    path = "c:\\temp\\ip_address.txt"
    global ip_addr
    # str_out = ""
    # for (k, v) in ip_addr.items():
    #     str_out += k + "       :        " + v.encode('utf-8')+r"\r\n"

    str_out = json.dumps(ip_addr, ensure_ascii=False)
    print str_out
    with open(path, "wb") as f:
        f.write(str_out.encode("utf-8"))


def get_ip_muti_thread():
    ip_list = []
    for i in range(1, 255):
        ip = str(i) + '.22.22.22'
        ip_list.append(ip)
        # get_address(ip)

    # TODO size设置过多会导致一些结果为空
    size = 4
    pool = ThreadPool(size)
    reqs = makeRequests(get_address, [([ip], None) for ip in ip_list])
    [pool.putRequest(req) for req in reqs]
    pool.wait()


if __name__ == '__main__':
    # get_ip_from_json()
    ip = "202.101.201.101"
    get_address(ip)
