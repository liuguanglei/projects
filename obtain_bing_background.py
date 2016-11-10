#!/usr/bin/env python
# -*- coding:utf-8 -*-
# -*- author:liugl -*-
# python抓取bing主页所有背景图片

import requests
import json
import os
import re
from BeautifulSoup import BeautifulSoup
import libxml2


def get_background_info(url):
    re = requests.get(url)
    re_content = json.loads(re.content)
    url = re_content["images"][0]["url"]
    name = re_content["images"][0]["enddate"]
    download(url, name, r'c:\\temp\\photo')


def download(url, name, dest):
    re = requests.get(url)
    raw = re.content
    path = dest + os.path.sep + name + ".jpg"
    if os.path.exists(path) is False:
        with open(dest + os.path.sep + name + ".jpg", "wb") as f:
            f.write(raw)


def rename(str):
    replace_str = "$"
    pattern = re.compile('[/\\\\:*?<>|"]')
    m = pattern.search(str)
    if m is not None:
        return str.replace(m.group(), replace_str)
    else:
        return str


def get_background():
    for i in range(17):
        root_url = "http://www.bing.com/HPImageArchive.aspx?format=js&idx=" + str(i) + "&n=1&mkt=zh-cn"
        get_background_info(root_url)


def get_one_month_background(year, month):
    print 'get image %s %s' % (year, month)
    url = "http://www.istartedsomething.com/bingimages/?m=" + str(month) + "&y=" + str(year)
    res = requests.get(url)
    soup = BeautifulSoup(res.content)
    target = soup.find('table').findAllNext(attrs={'href': re.compile(r"-cn")})
    for t in target:
        title = t.get('title')
        date = t.get('href')[1:]
        url = t.img.get('data-original')
        real_url = 'http://www.istartedsomething.com/bingimages/cache/' + url.split('=')[1][:-2]

        file_name = date + "_" + rename(title)
        # if title.find(u"(©") != -1:
        #     file_name = date + "_" + title.split(u'(©')[0]
        # if title.find(u"--") != -1
        #     file_name = date + "_" + title.split(u'--')[0]
        dest = r'c:\\temp\\photo'
        download(real_url, file_name, dest)


def get_background_new():
    for y in range(2009, 2017):
        for m in range(1, 13):
            if y <= 2009 and m <= 6:
                continue
            get_one_month_background(y, m)


if __name__ == '__main__':
    # get_background()
    # get_background_new()
    get_one_month_background(2010, 2)
