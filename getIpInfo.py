#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
import Queue
import traceback
import thread

lock = thread.allocate_lock()

from BeautifulSoup import BeautifulSoup
from threadpool import ThreadPool
from threadpool import makeRequests

# proxy_taken = []
proxy_free = []


def init_proxy():
    global proxy_free
    with open("c:/ip_info/proxy.txt", "r") as f:
        lines = f.readlines()
        for l in lines:
            proxy_free.append("http://{ip}:{port}".format(ip=l.split()[0], port=l.split()[1]))
            print proxy_free


def get_proxy():
    global proxy_free
    while True:
        if proxy_free:
            proxy = proxy_free.pop()
            return proxy
        else:
            time.sleep(1)


def back_proxy(proxy):
    global proxy_free
    proxy_free.append(proxy)


def send_thread_pool(ips=None):
    size = 100
    pool = ThreadPool(size)
    requests_pool = makeRequests(_get_address, [([ip], None) for ip in ips])
    [pool.putRequest(req) for req in requests_pool]
    pool.wait()


def error_handle(ip):
    print "error_handle"


def write_file(content, path=None):
    if path is None:
        path = "c:/ip_info/ip_info.txt"
    global lock
    lock.acquire()
    with open(path, 'a') as f:
        f.write(content + "\n")
    lock.release()


def write_thread_pool():
    ll = [str(i) for i in range(10000)]
    size = 100
    pool = ThreadPool(size)
    requests_pool = makeRequests(write_file, [([l], None) for l in ll])
    [pool.putRequest(req) for req in requests_pool]
    pool.wait()


def _get_address(ip, proxies=None):
    try:
        url = "http://ip.cn/index.php?ip=" + ip
        if proxies:
            res = requests.get(url, proxies=proxies)
        else:
            res = requests.get(url, proxies=get_proxy())
        if res.status_code != 200:
            error_handle(ip)
            return
        html = res.content
        soup = BeautifulSoup(html)
        target = soup.findAll('code')[1].text
        target1 = soup.findAll("div", {"class": "well"})[0]
        for index, c in enumerate(target1):
            if c.text.find("GeoIP") > -1:
                ll = c.text.split(":")[1].split(",")
                target = target + "," + " ".join([s.split()[0] for s in ll])
                continue
            if index == 3:
                target = target + "," + c.text
        target = ip + "," + target
        write_file(target)
        # print target
    except Exception, e:
        error_handle(ip)
        # print traceback.format_exc(e)


def gen_ip_d_segment():
    for a in range(255):
        if a == 10 or a == 127 or a == 0:
            continue
        for b in range(255):
            # 运营商级路由
            if a == 100 and b >= 64 and b <= 127:
                continue
            if a == 192 and b == 168:
                continue
            if a == 172 and b >= 16 and b <= 31:
                continue
            for c in range(255):
                yield ".".join([str(a), str(b), str(c), str(0)])


if __name__ == '__main__':
    ips = ["182.127.255.251"] * 300
    init_proxy()
    #
    # for i in range(10):
    #     _get_address("182.127.255.251")
    # send_thread_pool(ips)
    # write_thread_pool()
    # ip_iter = gen_ip_d_segment()
    # ips = []
    # for i in range(100000):
    #     # ips.append(ip_iter.next())
    #     # print len(ips)
    #     write_file(ip_iter.next(), path="c:/tmp/ip_d.txt")
