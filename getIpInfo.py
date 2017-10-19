#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import time
import Queue
import traceback
import thread
import os
import socket
import struct
import re
import chardet

import threading
from BeautifulSoup import BeautifulSoup
from threadpool import ThreadPool
from threadpool import makeRequests

# proxy_taken = []
proxy_free = []
path_root = "c:/ip_info"


def gen_thread_lock():
    while True:
        yield threading.RLock()


gen_lock = gen_thread_lock()


def get_thread_lock():
    return gen_lock.next()


def init_proxy():
    global proxy_free
    path = path_root + "/proxy.txt"
    with open(path, "r") as f:
        lines = f.readlines()
        for l in lines:
            if len(l.split()) == 2:
                proxy_free.append("http://{ip}:{port}".format(ip=l.split()[0], port=l.split()[1]))
    proxy_free = proxy_free * 6


lock3 = get_thread_lock()


def get_proxy():
    lock3.acquire()
    while True:
        if proxy_free:
            proxy = proxy_free.pop()
            lock3.release()
            return proxy
        else:
            print "---------------------------proxy_free num:" + str(len(proxy_free))
            print "--------------------------- reinit proxy"
            init_proxy()


# 用完代理后恢复到可用代理列表中
def back_proxy(proxy):
    if proxy:
        lock3.acquire()
        proxy_free.append(proxy)
        lock3.release()


def remove_proxy(proxy):
    path = path_root + "/proxy.txt"

    proxy_ip = proxy.split(r"//")[1].split(":")[0]
    ll_index = []
    lines = []
    lock3.acquire()
    with open(path, "r") as f:
        lines = f.readlines()
        for index, line in enumerate(lines):
            if line.find(proxy_ip) > -1:
                ll_index.append(index)
    for l in ll_index:
        del lines[l]
    with open(path, "w") as f:
        f.writelines(lines)
    print "---------------------------remove proxy: {proxy}".format(proxy=proxy)
    lock3.release()


def send_thread_pool(ips=None):
    size = 100
    pool = ThreadPool(size)
    requests_pool = makeRequests(get_address, [([ip], None) for ip in ips])
    [pool.putRequest(req) for req in requests_pool]
    pool.wait()


lock4 = get_thread_lock()


def error_handle(ip, proxy):
    path = path_root + "/ip_error.txt"
    lock4.acquire()
    with open(path, "a") as f:
        f.write(ip + "\n")
    lock4.release()


lock = get_thread_lock()

global_count = 0
global_file_count = 0
global_total = 0
NEW_IP_INFO_COUNT = 100000


def write_file(content, path=None):
    global global_count
    global global_file_count
    global global_total
    lock.acquire()
    global_count += 1
    global_total += 1
    if global_count >= NEW_IP_INFO_COUNT:
        if path is None:
            path = path_root + "/result/ip_info_{count}.txt".format(count=str(global_file_count))
        global_count = 0
        global_file_count += 1
    else:
        # 每隔多少条数据输出一次这次的总数
        if global_count % 1000 == 0:
            print "have request data total: {total},free proxy number:{num}".format(
                total=str(global_total), num=str(len(proxy_free)))
        if path is None:
            path = path_root + "/result/ip_info_{count}.txt".format(count=str(global_file_count))
    with open(path, 'a') as f:
        f.write(content + "\n")

    path_1 = path_root + "/ip_count_flag.txt"
    with open(path_1, "w") as f:
        count_str = ",".join([str(global_total), str(global_file_count), str(global_count)])
        f.write(count_str)
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
    path = path_root + "/current_req.txt"
    lock1.acquire()
    with open(path, 'a') as f:
        f.write(ip + "\n")
    lock1.release()


def remove_ip_from_current_req_file(ip):
    path = path_root + "/current_req.txt"
    lock1.acquire()
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
    lock1.release()


def get_address(ip=None, proxy=None):
    try:
        if ip is None:
            ip = get_ip_d()
        add_ip_to_current_req_file(ip)
        url = "http://ip.cn/index.php?ip=" + ip
        if proxy is None:
            proxy = get_proxy()
        # print "begin request d ip:{ip},proxy:{proxy}".format(ip=ip, proxy=proxy)
        res = requests.get(url, proxies={"http": proxy})

        if res.status_code != 200:
            error_handle(ip, proxy)
            return
        html = res.content
        target = ""
        # dammit = chardet.detect(html)["encoding"]
        if True:
            # 这种方式解析速度更快
            # 针对乱码的情况，通过正则解析
            target = get_info_from_html(html)
            if target == "":
                # 解析错误的情况
                error_handle(ip, proxy)
                remove_proxy(proxy)
                return
        else:
            soup = BeautifulSoup(html)
            result_ll = soup.findAll("div", {"class": "well"})
            if len(result_ll) == 0:
                # 比较有可能是代理被封的情况,因此把代理移除
                error_handle(ip, proxy)
                remove_proxy(proxy)
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
            target = ip + "," + target
            target = target.encode("utf8")
        write_file(target)
        back_proxy(proxy)
        # print target
    except requests.exceptions.ProxyError, e:
        print "ProxyError d ip:{ip},proxy:{proxy},current free proxy num:{count}".format(ip=ip, proxy=proxy,
                                                                                         count=len(proxy_free))
        error_handle(ip, proxy)
    except IndexError, e:
        print "IndexError d ip:{ip},proxy:{proxy}".format(ip=ip, proxy=proxy)
        error_handle(ip, proxy)
        back_proxy(proxy)
    except Exception, e:
        print traceback.format_exc()
        error_handle(ip, proxy)
        back_proxy(proxy)
    finally:
        remove_ip_from_current_req_file(ip)


def get_ip_run():
    while True:
        get_address()


lock2 = get_thread_lock()


def gen_ip_d_segment(num=None):
    path = path_root + "/ip_last_flag.txt"
    _a, _b, _c = 0, None, None
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
    for a in range(_a, 255):
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
                target += "," + t.split("：")[1].strip()
                # print chardet.detect(target)
            if index == 2:
                t = t.decode("ISO-8859-1").encode("utf-8")
                ll = t.split(":")[1].strip().split(",")
                target += "," + " ".join([s.split()[0] for s in ll])
            if index == 3:
                target += "," + t.strip()
        return target
    else:
        print "get_info_from_html return empyt string"
        return ""


def main():
    path = path_root + "/result"
    if os.path.exists(path) is False:
        os.makedirs(path)
    path_1 = path_root + "/ip_count_flag.txt"
    if os.path.exists(path_1):
        with open(path_1, "r") as f:
            ll = f.read().split(",")
            global global_count, global_file_count, global_total
            global_total, global_file_count, global_count = int(ll[0]), int(ll[1]), int(ll[2])

    init_proxy()
    thread_num = 200
    for i in range(thread_num):
        threading.Thread(target=get_ip_run).start()


if __name__ == '__main__':
    # ips = ["182.127.255.251"] * 300
    # init_proxy()

    # for i in range(10):
    # get_address("1.4.175.0", "'http://62.80.182.42:53281'")
    # send_thread_pool(ips)
    # write_thread_pool()
    # ip_iter = gen_ip_d_segment(100)
    # for i in ip_iter:
    #     write_file(i, path=path_root + "/ip_d.txt")
    # print get_ip_d()
    # print get_ip_d()
    # print get_ip_d()
    # print get_ip_d()

    # remove_proxy("http://118.76.255.52:80")
    # filter_proxy()
    main()
