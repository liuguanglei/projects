#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
import Queue
import traceback
import thread
import os

import threading
from BeautifulSoup import BeautifulSoup
from threadpool import ThreadPool
from threadpool import makeRequests

# proxy_taken = []
proxy_free = []


def gen_thread_lock():
    while True:
        yield threading.Lock()


gen_lock = gen_thread_lock()


def get_thread_lock():
    return gen_lock.next()


def init_proxy():
    with open("c:/ip_info/proxy.txt", "r") as f:
        lines = f.readlines()
        for l in lines:
            if len(l.split()) == 2:
                proxy_free.append("http://{ip}:{port}".format(ip=l.split()[0], port=l.split()[1]))


lock3 = get_thread_lock()


def get_proxy():
    while True:
        lock3.acquire()
        if proxy_free:
            proxy = proxy_free.pop()
            lock3.release()
            return proxy
        else:
            time.sleep(1)


# 用完代理后恢复到可用代理列表中
def back_proxy(proxy):
    if proxy:
        proxy_free.append(proxy)


def send_thread_pool(ips=None):
    size = 100
    pool = ThreadPool(size)
    requests_pool = makeRequests(get_address, [([ip], None) for ip in ips])
    [pool.putRequest(req) for req in requests_pool]
    pool.wait()


lock4 = get_thread_lock()


def error_handle(ip, proxy):
    path = "c:/ip_info/ip_error.txt"
    lock4.acquire()
    with open(path, "a") as f:
        f.write(ip + "\n")
    lock4.release()


lock = get_thread_lock()


def write_file(content, path=None):
    if path is None:
        path = "c:/ip_info/ip_info.txt"
    lock.acquire()
    with open(path, 'a') as f:
        f.write(content.encode("utf8") + "\n")
    lock.release()


def write_thread_pool():
    ll = [str(i) for i in xrange(1000)]
    size = 100
    pool = ThreadPool(size)
    requests_pool = makeRequests(write_file, [([l], None) for l in ll])
    [pool.putRequest(req) for req in requests_pool]
    pool.wait()


lock1 = get_thread_lock()


def add_ip_to_current_req_file(ip):
    path = "c:/ip_info/current_req.txt"
    lock1.acquire()
    with open(path, 'a') as f:
        f.write(ip + "\n")
    lock1.release()


lock5 = get_thread_lock()


def remove_ip_from_current_req_file(ip):
    path = "c:/ip_info/current_req.txt"
    lock5.acquire()
    lines = []
    with open(path, 'r') as f:
        lines = f.readlines()
        del_index = None
        for index, line in enumerate(lines):
            if ip == line.split()[0]:
                del_index = index
        if del_index is not None:
            del lines[del_index]
    with open(path, 'w') as f:
        f.writelines(lines)
    lock5.release()


def get_address(ip=None, proxy=None):
    try:
        if ip is None:
            ip = get_ip_d()
        add_ip_to_current_req_file(ip)
        url = "http://ip.cn/index.php?ip=" + ip
        if proxy is None:
            proxy = get_proxy()
        res = requests.get(url, proxies={"http": proxy})
        if res.status_code != 200:
            error_handle(ip, proxy)
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
        print traceback.format_exc()
        error_handle(ip, proxy)
    finally:
        remove_ip_from_current_req_file(ip)
        back_proxy(proxy)


def get_ip_run():
    while True:
        get_address()


lock2 = get_thread_lock()


def gen_ip_d_segment(num=None):
    path = "c:/ip_info/ip_last_flag.txt"
    _a, _b, _c = None, None, None
    if os.path.exists(path):
        with open(path, "r") as f:
            last_ip = f.read()
            _a = int(last_ip.split(",")[0])
            _b = int(last_ip.split(",")[1])
            _c = int(last_ip.split(",")[2])
    lock2.acquire()
    count = 1000
    if num:
        count = num
    for a in range(0, 255):
        if a == 10 or a == 127 or a == 0:
            continue
        for b in range(0, 255):
            if _b:
                if b < _b:
                    continue
                else:
                    _b = None
            # 运营商级路由
            if a == 100 and b >= 64 and b <= 127:
                continue
            if a == 192 and b == 168:
                continue
            if a == 172 and b >= 16 and b <= 31:
                continue

            for c in range(0, 255):
                if _c:
                    if c <= _c:
                        continue
                    else:
                        _c = None
                tmp = [str(a), str(b), str(c)]
                if num:
                    count -= 1
                    if count >= 0:
                        with open(path, 'w') as f:
                            f.write(",".join(tmp))
                        yield ".".join(tmp + [str(0)])
                    else:
                        return
                else:
                    with open(path, 'w') as f:
                        f.write(",".join(tmp))
                    yield ".".join(tmp + [str(0)])
    lock2.release()


gen_ip = gen_ip_d_segment()

lock11 = get_thread_lock()


def get_ip_d():
    lock11.acquire()
    ip = gen_ip.next()
    lock11.release()
    return ip


lock10 = get_thread_lock()


def write_proxy_txt(proxy_ip):
    path = "c:/ip_info/proxy.txt"
    lock10.acquire()
    with open(path, "a") as f:
        f.write(proxy_ip)
    lock10.release()


def is_proxy_available(ip, port):
    try:
        proxy = {"http": "http://{ip}:{port}".format(ip=ip, port=port)}
        url = "http://ip.cn/index.php?ip=" + ip
        res = requests.get(url, proxies=proxy)
        if res.status_code == 200:
            print "normal proxy ip:{ip}".format(ip=ip)
            write_proxy_txt(ip + '\t' + port + '\n')
        else:
            print "exception code proxy ip:{ip}".format(ip=ip)
    except Exception, e:
        print "exception proxy ip:{ip}".format(ip=ip)


def filter_proxy():
    path = "c:/ip_info/proxy_ori.txt"
    lines = []

    ss = set()
    with open(path, "r") as f:
        lines = f.readlines()
        ll = []
        for line in lines:
            if len(line.split()) != 2:
                continue
            ip = line.split()[0]
            if ip in ss:
                continue
            else:
                ss.add(ip)

            port = line.split()[1]
            ll.append((ip, port))

        pool = ThreadPool(50)
        requests_pool = makeRequests(is_proxy_available, [([l[0], l[1]], None) for l in ll])
        [pool.putRequest(req) for req in requests_pool]
        pool.wait()


if __name__ == '__main__':
    # ips = ["182.127.255.251"] * 300
    # init_proxy()
    #
    # for i in range(10):
    #     get_address("182.127.255.251")
    # send_thread_pool(ips)
    # write_thread_pool()
    # ip_iter = gen_ip_d_segment(100)
    # for i in ip_iter:
    #     write_file(i, path="c:/ip_info/ip_d.txt")
    # print get_ip_d()
    # print get_ip_d()
    # print get_ip_d()
    # print get_ip_d()

    # filter_proxy()
    init_proxy()
    thread_num = 100
    for i in range(thread_num):
        obj = threading.Thread(target=get_ip_run).start()
