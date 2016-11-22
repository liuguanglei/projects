#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests

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


if __name__ == '__main__':
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
