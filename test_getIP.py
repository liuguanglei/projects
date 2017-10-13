#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import traceback
import chardet

from BeautifulSoup import BeautifulSoup
# from bs4 import UnicodeDammit

def get_address(ip=None, proxy=None):
    try:
        url = "http://ip.cn/index.php?ip=" + ip
        # print "begin request d ip:{ip},proxy:{proxy}".format(ip=ip, proxy=proxy)
        res = requests.get(url, proxies={"http": proxy})
        if res.status_code != 200:
            return
        html = res.content
        soup = BeautifulSoup(html)
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
        print
    except IndexError, e:
        print traceback.format_exc()
    except Exception, e:
        print traceback.format_exc()
    finally:
        pass


if __name__ == '__main__':
    ip = "1.34.209.0"
    proxy = "http://183.2.208.35:80"
    get_address(ip, proxy)
