#!/usr/bin/env python
# -*- coding:utf-8 -*-

import random
import traceback
from db_helper import getConnection, executeSql


def insert_data_to_db():
    increase = 100
    two = {11: "北京", 12: "天津", 13: "河北", 14: "山西", 15: "内蒙古", 21: "辽宁", 22: "吉林", 23: "黑龙江 ", 31: "上海", 32: "江苏",
           33: "浙江",
           34: "安徽", 35: "福建", 36: "江西", 37: "山东", 41: "河南", 42: "湖北 ", 43: "湖南", 44: "广东", 45: "广西", 46: "海南",
           50: "重庆",
           51: "四川", 52: "贵州", 53: "云南", 54: "西藏 ", 61: "陕西", 62: "甘肃", 63: "青海", 64: "宁夏", 65: "新疆", 71: "台湾",
           81: "香港",
           82: "澳门", 91: "国外 "}

    tow_list = two.keys()
    tow_value_list = two.values()
    last_list = [str(i) for i in range(0 - 9)] + ['x']

    conn = getConnection()
    cursor = conn.cursor()

    for i in xrange(1000000):
        _id = increase
        sfzh = str(random.choice(tow_list)) + str(random.randint(100000000000000, 999999999999999)) + random.choice(
            last_list)
        xm = str(random.randint(10, 20000))
        xb = random.choice(["男", "女"])
        nl = str(random.randint(1, 150))
        hyzk = random.choice(["已婚", "未婚", "未知"])
        xl = random.choice(["小学", "初中", "高中", "专科", "大学及以上", "未知"])
        xzz = random.choice(tow_value_list)
        jcxx = random.random() * 100
        shxx = random.random() * 100
        cxxw = random.random() * 100
        swxw = random.random() * 100
        zsxw = random.random() * 100
        fs = random.random() * 100
        y = random.choice([1] * 1 + [0] * 9)
        isck = random.choice([1] * 7 + [0] * 3)

        sql = "INSERT INTO `result` VALUES ('{_id}', '{sfzh}', '{xm}', '{xb}', '{nl}', '{hyzk}', '{xl}', " \
              "'{xzz}', '{jcxx}', '{shxx}', '{cxxw}', '{swxw}', '{zsxw}', '{fs}', '{y}', '{isck}')" \
            .format(_id=_id, sfzh=sfzh, xm=xm, xb=xb, nl=nl, hyzk=hyzk, xl=xl, xzz=xzz, jcxx=jcxx,
                    shxx=shxx, cxxw=cxxw, swxw=swxw, zsxw=zsxw, fs=fs, y=y, isck=isck)
        cursor.execute(sql)

        increase += 1
        if increase % 1000 == 0:
            print increase
    conn.commit()
    conn.close()


if __name__ == '__main__':
    insert_data_to_db()
