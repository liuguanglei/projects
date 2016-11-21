# /usr/bin/env python
# _*_coding:utf-8_*_
__author__ = 'Eagle'
# version:1.0

import urllib
import urllib2
import os  # read system
import cookielib  # cookie lib
import time  # time module
import sys
import re
import math
import random
import requests
import json
from urllib import urlencode, unquote, quote

uuid = ''  # 定义微信登陆请求中tip值
imagesPath = os.getcwd() + '/weixin.jpg'  # 定义二维码图片路径，os.getcwd()获取当前路径

# 用于登录的全局参数
g_value = {}
# 联系人
g_contacts = []

g_myself = {}

# urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.LWPCookieJar(filename='cookies')))
agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'
# agent = 'Mozilla/5.0 (Windows NT 5.1; rv:33.0) Gecko/20100101 Firefox/33.0'

headers = {
    'User-Agent': agent
}

# 使用登录cookie信息
session = requests.session()
# session.cookies = cookielib.LWPCookieJar(filename='cookies')
session.cookies = cookielib.CookieJar()
# try:
#     session.cookies.load(ignore_discard=True)
# except:
#     print("Cookie 未能加载")


def getUUID():  # get UUID
    global uuid  # 引入全局变量uuid
    url = 'https://login.weixin.qq.com/jslogin'  # 登陆请求界面的url
    values = {
        'appid': 'wx782c26e4c19acffb',
        'redirect_uri': 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage',
        'fun': 'new',
        'lang': 'zh_CN',
        '_': int(time.time())  # 时间戳
    }
    # 用urllib2中的Request模块（有三个参数，url，data，）
    # 用urllib的urlencode()方法进行编码转换，转换后才能被网页识别
    # request = urllib2.Request(url=url, data=urllib.urlencode(values))
    # response = urlOpener.open(url, data=urllib.urlencode(values))
    response = session.post(url, data=values, headers=headers)
    # response = urllib2.urlopen(request)  # 打开实时请求request
    # data = response.read()  # 读出response的值
    data = response.content  # 读出response的值

    print data
    # 用正则表达式获取网页返回的实时值,\d为int类型，\S为非空白字符
    regx = r'window.QRLogin.code = (\d+); window.QRLogin.uuid = "(\S+?)"'
    pm = re.search(regx, data)
    code = pm.group(1)
    uuid = pm.group(2)
    g_value['uuid'] = uuid
    print code, uuid

    if code == '200':
        return True
    return False


def show2DimensionCode():
    global tip  # 引入全局变量tip

    url = 'https://login.weixin.qq.com/qrcode/' + uuid
    values = {
        't': 'webwx',
        '_': int(time.time())
    }

    # request = urllib2.Request(url=url, data=urllib.urlencode(values))
    # response = urllib2.urlopen(request)
    # response = urlOpener.open(url, data=urllib.urlencode(values))
    response = session.post(url, data=values, headers=headers)
    tip = 1

    f = open(imagesPath, 'wb')  # 以二进制（b）打开二维码图片
    # f.write(response.read())  # 将response获取的值写入img文件中
    f.write(response.content)
    f.close()
    time.sleep(1)  # 延时1秒
    os.system('call %s' % imagesPath)  # 打开图片

    # windows中DOS命令中不支持utf-8，这里用u和encode防止乱码
    print u'请使用手机微信扫描二维码登录'.encode('GBK')


def isLoginSucess():
    # 获取微信登陆请求地址,读取返回值
    url = 'https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login?tip=%s&uuid=%s&_=%s' % (tip, uuid, int(time.time()))
    # request = urllib2.Request(url=url)
    # response = urllib2.urlopen(request)
    # response = urlOpener.open(url)
    response = session.get(url, headers=headers)
    # data = response.read()
    data = response.content
    print data
    # data值为window.code=408，登陆失败;为window.code=201，登陆成功
    # 利用正则表达式获取登陆状态码
    regx = r'window.code=(\d+)'
    pm = re.search(regx, data)
    code = pm.group(1)
    # 判断登陆状态
    if code == '201':
        print'Scan QR code successfully!'
    elif code == '200':
        ticket = data.split("ticket=")[1].split('&')[0]
        scan = data.split("scan=")[1]
        g_value['ticket'] = ticket
        g_value['scan'] = scan
        print'Logining...'
    elif code == '408':
        print'Login Timeout!'

    return code


def get_login_param():
    ticket = g_value['ticket']
    uuid = g_value['uuid']
    scan = g_value['scan']

    url = "https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxnewloginpage?" \
          "ticket=%s&" \
          "uuid=%s&lang=zh_CN&scan=%s&fun=new&version=v2" % (ticket, uuid, scan)

    # request = urllib2.Request(url=url)
    # response = urlOpener.open(url)

    response = session.get(url, headers=headers)
    # response = urllib2.urlopen(request)
    data = response.content
    g_value['skey'] = data.split("<skey>")[1].split("</skey>")[0]
    g_value['sid'] = data.split("<wxsid>")[1].split("</wxsid>")[0]
    g_value['uin'] = data.split("<wxuin>")[1].split("</wxuin>")[0]
    # g_value['pass_ticket'] = unquote(data.split("<pass_ticket>")[1].split("</pass_ticket>")[0])
    g_value['pass_ticket'] = data.split("<pass_ticket>")[1].split("</pass_ticket>")[0]
    print data


def getDeviceID():
    g_value['DeviceID'] = "e" + "".join([str(random.choice(range(10))) for i in range(15)])


def send_message(name=None, msg='hello!'):
    url = 'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxsendmsg?lang=zh_CN'

    nickName = None
    for member in g_contacts:
        if name == member['NickName']:
            nickName = member['UserName']
            break

    clientMsgId = str(int(time.time() * 1000)) + \
                  str(random.random())[:5].replace('.', '')
    post_content = {
        "BaseRequest":
            {
                "Uin": g_value['uin'],
                "Sid": g_value['sid'],
                "Skey": g_value['skey'],
                "DeviceID": g_value['DeviceID']
            },
        "Msg":
            {
                "Type": 1,
                "Content": msg,
                "FromUserName": g_myself['User']['UserName'],
                # "ToUserName": "filehelper",
                "ToUserName": nickName,
                "LocalID": clientMsgId,
                "ClientMsgId": clientMsgId
            }
    }

    response = session.post(url, data=json.dumps(post_content), headers=headers)
    data = response.content
    print data

def wx_init():
    # _r = raw_input("_r")
    # _r = get_r()
    _r = int(time.time())

    # pass_ticket里面包含%2f %2b等url编码
    # url = "https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r=%s&pass_ticket=%s" % (~int(time.time()), quote(g_value['pass_ticket']))
    # url = "https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r=%s&lang=zh_CN&pass_ticket=%s" % (
    #     _r, g_value['pass_ticket'])

    url = "https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxinit?pass_ticket=%s&skey=%s&r=%s" % (
        g_value['pass_ticket'], g_value['skey'], _r)

    values = {
        'BaseRequest': {
            'Uin': int(g_value['uin']),
            'Sid': g_value['sid'],
            'Skey': g_value['skey'],
            'DeviceID': g_value['DeviceID']
        }
    }

    agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.109 Safari/537.36'
    headers = {
        'User-Agent': agent,
        'ContentType': 'application/json;charset=UTF-8'

    }
    response = session.post(url, data=json.dumps(values), headers=headers)
    data = response.content

    # request = urllib2.Request(url=url, data=json.dumps(values))
    # request.add_header('ContentType', 'application/json; charset=UTF-8')

    # urlOpener = urllib2.build_opener(urllib2.HTTPCookieProcessor(session.cookies))
    # response = urlOpener.open(request)
    # data = response.read()
    data = json.loads(data)
    g_myself['SyncKey'] = data['SyncKey']
    g_myself['User'] = data['User']

    print data


def get_connect():
    url = 'https://wx.qq.com/cgi-bin/mmwebwx-bin' + '/webwxgetcontact?pass_ticket=%s&skey=%s&r=%s' % (
        g_value['pass_ticket'], g_value['skey'], int(time.time()))

    response = session.post(url, data={}, headers=headers)
    # response = urllib2.urlopen(request)
    data = response.content
    data = json.loads(data)
    global g_contacts
    g_contacts = data['MemberList']
    print data


# 入口函数
def main():
    # 获取当前cookie
    # cj = cookielib.CookieJar()
    # cookie = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    # urllib2.install_opener(cookie)

    # 判断是否成功获取uuid
    if getUUID() == False:
        print'Get uuid unsuccessfully!'
        return None

    show2DimensionCode()
    time.sleep(1)

    while isLoginSucess() != '200':
        pass

    # 判断登陆成功，删除二维码
    # os.remove(imagesPath)
    print'Login successfully!'


def get_r():
    # from ctypes import *
    # print c_int(10)
    # print ~int(10)
    # print  int('00001010', 2)
    # print  ~int('00001010', 2)
    # print  int('11110101', 2)
    # print (int('10000000011001101000011001010100', 2)+0b1)
    # print ~int('10000000011001101000011001010100', 2)
    # print  int('101111111100110010111100110101011', 2)
    # print bin(10)
    # 1479622952532 : 2140764587
    ori_shi = 1479622952532

    print bin(ori_shi)
    r = ~int(bin(ori_shi)[-32:], 2)

    return ~int(bin(int(time.time() * 1000))[-32:], 2)


if __name__ == '__main__':
    # get_r()
    getDeviceID()
    print'Welcome to use weixin personnal version'
    print'Please click Enter key to continue......'
    main()
    get_login_param()
    wx_init()
    get_connect()
    for i in range(10):
        send_message(u'刘颖')
