# -*- coding: utf-8 -*-

import os
import json
import base64

if __name__ == "__main__":
    dic = {
        "sHost": "192.168.20.112:8080",
        "sensorID": "Sensor001",
        "eventID": "A027-6-01-Sensor001-20161214141513014",
        "sessionID": 0,
        "time": 1481696113,
        "timedate": "2016-12-14 14:15:13",
        "logTime": 1481696115,
        "srcIP": "1.6.1.1",
        "dstIP": "192.168.20.3",
        "srcPort": 58631,
        "dstPort": 80,
        "method": "POST",
        "uri": "/spy.php",
        "version": "HTTP/1.1",
        "host": "192.168.20.203:8080",
        "userAgent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.22 Safari/537.36",
        "referer": "http://192.168.20.203:8080/spy.php",
        "reqBodyPath": "/tmp/http/reqBody/1773/20161214/20161214-14/20161214-141513-1481696113385-135",
        "resBodyPath": "",
        "status": 0,
        "reqHeaders": [
            "Cookie=adminer_version=0; adminpass=1; admin_silicpass=f9606eb557d4e9a708cd18dc9749a42d; loginpass=571df1818893b45ad4fd9697b55b3679"
            ,
            "Accept-Language=zh-CN,zh;q=0.8"
            ,
            "Accept-Encoding=gzip, deflate"
            ,
            "Referer=http://192.168.20.203:8080/spy.php"
            ,
            "Content-Type=application/x-www-form-urlencoded"
            ,
            "User-Agent=Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.22 Safari/537.36"
            ,
            "Upgrade-Insecure-Requests=1"
            ,
            "Origin=http://192.168.20.203:8080"
            ,
            "Accept=text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"
            ,
            "Cache-Control=max-age=0"
            ,
            "Content-Length=136"
            ,
            "Connection=keep-alive"
            ,
            "Host=192.168.20.203:8080"
        ],
        "resHeaders": [],
        "ruleID": 24,
        "ruleLevel": 2,
        "ruleType": "WEBSHELL",
        "ruleName": "WEBSHELL",
        "category": "A",
        "subCategory": 27,
        "srcHostID": "",
        "srcHostDepID": "",
        "dstHostID": "",
        "dstHostDepID": "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFC",
        "srcLocation": "IN",
        "dstLocation": "",
        "killChainType": 6,
        "srcCountry": "印度",
        "dstCountry": "",
        "srcLatitude": 20,
        "srcLongitude": 77,
        "dstLatitude": 0,
        "dstLongitude": 0,
        "srcIntranet": 0,
        "dstIntranet": 1,
        "srcIsServer": 0,
        "dstIsServer": 0,
        "attackedSvr": "192.168.20.3",
        "attackSvr": "1.6.1.1"
    }
    dic_str = json.dumps(dic)

    code_str = base64.b64encode(dic_str)
    # print base64.b64decode(code_str)
    # print code_str

    # cmd_str = "python input_param1.py " + dic_str
    cmd_str = "python input_param.py -o " + code_str
    # cmd_str = cmd_str.replace(r'"',r'/#')
    # print cmd_str
    os.system(cmd_str)
    # print os.system("python input_param1.py")
