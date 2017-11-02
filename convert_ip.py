#!/usr/bin/env python
# -*- coding: utf-8 -*-

import MySQLdb
import time
import os
import socket
import struct
import traceback
import datetime
import copy

from _mysql_exceptions import IntegrityError
from MySQLdb import escape_string


def elapse(func):
    def deco(*args, **kwargs):
        starttime = datetime.datetime.now()
        func(*args, **kwargs)
        endtime = datetime.datetime.now()
        print "elapse time: " + str((endtime - starttime).seconds) + " seconds"

    return deco


DB = {
    # 'host': '127.0.0.1',
    'host': '192.168.10.201',
    'port': 3306,
    'user': 'scorpion',
    'passwd': 'CM$ecThreat#2015',
    'db': 'kb',
    'charset': 'utf8',
}


def getMySQLConnection():
    conn = MySQLdb.connect(
        host=DB['host'],
        port=DB['port'],
        user=DB['user'],
        passwd=DB['passwd'],
        db=DB['db'],
        charset=DB['charset']
    )
    return conn


def convert_int2Ip(int_ip):
    return socket.inet_ntoa(struct.pack('!L', int_ip))


def convert_ip2Int(ip):
    return socket.ntohl(struct.unpack("I", socket.inet_aton(str(ip)))[0])


def get_add_to_table_sql(line):
    arr = line.split(",")
    ip_start_str = arr[0]
    ip_start = convert_ip2Int(arr[0])
    ip_end = ip_start + 255
    ip_end_str = convert_int2Ip(ip_end)
    country = escape_string(arr[1])
    msg = ""
    msg1 = ""

    if line.find("GeoIP:") > -1:
        del arr[2]
        if arr[2].find("GeoIP:") > -1:
            arr[2] = arr[2].split("GeoIP:")[1]
        msg = " ".join([l.strip() for l in arr[2:]])
    elif len(arr) == 3:
        msg = arr[2]
    elif len(arr) == 4:
        msg = arr[2]
        msg1 = arr[3]
    msg = escape_string(msg.decode("iso-8859-1").encode("utf8"))
    msg1 = escape_string(msg1.decode("iso-8859-1").encode("utf8"))
    sql = "INSERT INTO `kb_ip_address_all` " \
          "VALUES ('{ip_start}', '{ip_end}', '0', '{country}', '', '', '0', '0', '{msg}', '', '', '{ip_start_str}', '{ip_end_str}','{msg1}');".format(
        ip_start=ip_start, ip_end=ip_end, country=country, msg=msg, ip_start_str=ip_start_str, ip_end_str=ip_end_str,
        msg1=msg1)

    return sql


@elapse
def add_to_table():
    path = "c:/ip_info/result/ip_info_"
    # path = "C:\Users\Administrator\Desktop/ip_info_"
    conn = getMySQLConnection()
    for i in range(161, 162):
        path_ = path + str(i) + ".txt"

        cur = conn.cursor()
        with open(path_, "r") as f:
            lines = f.readlines()
            for line in lines:
                sql = get_add_to_table_sql(line.strip())
                try:
                    cur.execute(sql)
                except IntegrityError, e:
                    print "IntegrityError sql:" + sql
                    # pass
                except Exception:
                    print traceback.format_exc()
        cur.close()
        conn.commit()
        print "add file to db finish:" + path_
    conn.close()


def convet_int2Ip(int_ip):
    return socket.inet_ntoa(struct.pack('!L', int_ip))


def convert_ip2Int(ip):
    return socket.ntohl(struct.unpack("I", socket.inet_aton(str(ip)))[0])


def convert_to_next_d(int_ip):
    result = ""
    tmp = int_ip + 256
    tmp1 = tmp % 256
    tmp = tmp - tmp1
    result = convet_int2Ip(tmp)
    return result


def calculate_step_ip(int_ip_start, int_ip_end):
    ll = []
    while int_ip_start < int_ip_end:
        ll.append(convert_to_next_d(int_ip_start))
        int_ip_start = int_ip_start + 256
    return ll[:-1]


def check_continuity():
    print u'======== 开始判断地址段的连续性 ========'
    timeStart = time.time()
    resNum = 0
    conn = getMySQLConnection()
    cur = conn.cursor()
    sql = "SELECT `IP_START`, `IP_END` FROM kb_ip_address_merge ORDER BY IP_START,IP_END LIMIT 0, 10000000"

    path = "c:/ip_info/z_all_need_req_ip.txt"
    count = cur.execute(sql)
    print 'find %d records' % count
    if count:
        res = cur.fetchall()
        result = []
        data = None
        for index, d in enumerate(res):
            if index % 100000 == 0:
                print index

            item = {}
            item['IP_START'] = d[0]
            item['IP_END'] = d[1]
            if data and data['IP_END'] + 1 == item['IP_START']:
                pass
            else:
                if data:
                    print data['IP_END'], item['IP_START']
                    d_tmp_list = calculate_step_ip(data['IP_END'], item['IP_START'])
                    result += d_tmp_list
                    resNum += 1
            data = item
        for index, line in enumerate(result):
            result[index] = line + "\n"
        with open(path, "w") as f:
            f.writelines(result)
    cur.close()
    conn.close()
    print '%d 条数据存在不连续性' % resNum

    timeEnd = time.time()
    print u'\n\n\n==================处理结束 耗时 %f 秒 =================\n\n\n' % (timeEnd - timeStart)


def merge_date():
    print u'======== 开始合并 ========'
    timeStart = time.time()
    conn = getMySQLConnection()
    cur = conn.cursor()
    sql = "SELECT `IP_START`, `IP_END`, `COUNTRY` FROM KB_IP_ADDRESS_ALL ORDER BY IP_START,IP_END LIMIT 9999000, 10000000"

    path = "c:/ip_info/z_merge_result.txt"
    count = cur.execute(sql)
    print 'find %d records' % count
    if count:
        res = cur.fetchall()
        result = []
        data = None
        for index, d in enumerate(res):
            if index % 100000 == 0:
                print index

            item = {}
            item['IP_START'] = d[0]
            item['IP_END'] = d[1]
            item['COUNTRY'] = d[2]

            if data and data['COUNTRY'] == item['COUNTRY']:
                data["IP_END"] = item['IP_END']
            else:
                if data is None:
                    data = item
                    continue
                else:
                    result.append(data)
                    data = item

        result_out = []
        for line in result:
            arr = line["COUNTRY"].split(" ")
            country = ''
            msg = ''
            if len(arr) == 0:
                pass
            elif len(arr) == 1:
                country = arr[0]
            elif len(arr) == 2:
                country = arr[0]
                msg = arr[1]
            else:
                print "country error arr len gt 2"

            result_out.append(
                (",".join([str(line['IP_START']), str(line["IP_END"]), country, msg]) + '\n').encode("utf8"))
        with open(path, "w") as f:
            f.writelines(result_out)
    cur.close()
    conn.close()
    print '合并后剩余%d 条数据' % len(result)

    timeEnd = time.time()
    print u'\n\n\n==================处理结束 耗时 %f 秒 =================\n\n\n' % (timeEnd - timeStart)


def get_merge_sql(line):
    country = ""
    area = ""
    city = ""
    code = ""

    arr = line.split(",")
    ip_start = arr[0]
    ip_end = arr[1]
    ip_start_str = convet_int2Ip(int(ip_start))
    ip_end_str = convet_int2Ip(int(ip_end))
    all_country = arr[2]
    msg1 = all_country
    msg = arr[3]
    if all_country.find("省") > -1 or all_country.find("市") > -1 or all_country.find(
            "自治区") > -1 or all_country.find("特别行政区") > -1 or all_country.find("中国") > -1 \
            or all_country.find("教育网") > -1 or all_country.find("阿里云") > -1:
        country = "中国"
        code = "CN"
        if all_country.find("省") > -1:
            arr_country = all_country.split("省")
            area = arr_country[0] + "省"
            if len(arr_country) > -1:
                city = arr_country[1]
        elif all_country.find("自治区") > -1:
            arr_country = all_country.split("自治区")
            area = arr_country[0] + "自治区"
            if len(arr_country) > -1:
                city = arr_country[1]
        elif all_country.find("特别行政区") > -1:
            arr_country = all_country.split("特别行政区")
            area = arr_country[0] + "特别行政区"
            if len(arr_country) > -1:
                city = arr_country[1]
        elif all_country.find("北京市") > -1 or all_country.find("天津市") > -1 or all_country.find(
                "上海市") > -1 or all_country.find(
            "重庆市") > -1:
            arr_country = all_country.split("市")
            area = arr_country[0] + "市"
            if len(arr_country) > -1:
                city = arr_country[1]
        elif all_country.find("教育网") > -1:
            pass
        elif all_country.find("中国") > -1:
            pass
        elif all_country.find("阿里云") > -1:
            area = "浙江省"
        else:
            print "error" + line
    else:
        country = all_country

    sql = "INSERT INTO `kb_ip_address_merge`" \
          "VALUES ('{ip_start}', '{ip_end}', '0', '{country}', '{area}', '{city}', '0', '0', '{msg}', " \
          "'{code}', '', '{ip_start_str}', '{ip_end_str}','{msg1}');".format(
        ip_start=ip_start, ip_end=ip_end, country=country, area=area, city=city, msg=msg, ip_start_str=ip_start_str,
        ip_end_str=ip_end_str, msg1=msg1, code=code)
    return sql


def add_merge_data_to_db():
    print u'======== 开始合并到数据库 ========'
    timeStart = time.time()
    conn = getMySQLConnection()
    cur = conn.cursor()
    path = "c:/ip_info/z_merge_result.txt"
    with open(path) as f:
        lines = f.readlines()
        for line in lines:
            sql = get_merge_sql(line.strip())
            try:
                cur.execute(sql)
            except Exception:
                print traceback.format_exc()
    cur.close()
    conn.commit()
    conn.close()

    timeEnd = time.time()
    print u'==================处理结束 耗时 %f 秒 =================' % (timeEnd - timeStart)


def is_city_geo_exist():
    # 遍历爬出来的结果集，查看未知信息是否存在
    print u'======== is_city_geo_exist ========'
    timeStart = time.time()
    conn = getMySQLConnection()
    cur = conn.cursor()
    sql = "SELECT area, city from kb_ip_address_merge WHERE code='CN' GROUP BY area,city"
    count = cur.execute(sql)
    print 'find %d records' % count
    resNum = 0
    if count:
        res = cur.fetchall()
        for re in res:
            area = re[0]
            city = re[1]
            if city.find(u"自治州") > -1:
                city = city[:-3]
            elif city.find(u"市") > -1 or city.find(u'州') > -1 or city.find(u'县') > -1:
                city = city[:-1]
            elif city.find(u'地区') > -1:
                city = city[:-2]
            area = area.encode("utf8")
            city = city.encode("utf8")
            sql = "SELECT PROVINCE, city from kb_city WHERE DISTRICT like'{city}%'".format(
                area=area, city=city)
            count1 = cur.execute(sql)
            if count1 == 0:
                resNum += 1
                print "{area},{city} don't exist".format(area=area, city=city)
            elif count1 > 10:
                print "{area},{city} don't exist".format(area=area, city=city)
            else:
                pass
                # print count1
    timeEnd = time.time()
    print u'==================处理结束 耗时 %f 秒 =================' % (timeEnd - timeStart)
    print resNum


def supplement_country_geo():
    print u'======== is_city_geo_exist ========'
    timeStart = time.time()
    conn = getMySQLConnection()
    cur = conn.cursor()
    sql = "SELECT country, latitude, longitude from kb_ip_address WHERE COUNTRY!='中国' GROUP BY COUNTRY"
    count = cur.execute(sql)
    resNum = 0
    print 'find %d records' % count
    if count:
        res = cur.fetchall()
        for re in res:
            country = re[0].encode("utf8")
            lat = re[1]
            lon = re[2]
            if lat is None:
                lat = 0
            if lon is None:
                lon = 0
            sql = "SELECT ID from kb_country_geo WHERE COUNTRY_ZH = '{country}'".format(country=country)
            count1 = cur.execute(sql)
            if count1 == 0:
                print "don't find country " + country
                resNum += 1
            else:
                re = cur.fetchall()[0]
                id = re[0]
                sql = "UPDATE kb_country_geo SET latitude = {lat},longitude ={lon} WHERE id = {id}".format(id=id,
                                                                                                           lat=lat,
                                                                                                           lon=lon)
                cur.execute(sql)

    cur.close()
    conn.commit()
    conn.close()
    timeEnd = time.time()
    print u'==================处理结束 耗时 %f 秒 =================' % (timeEnd - timeStart)
    print "total:" + str(resNum)


def is_country_geo_exist():
    timeStart = time.time()
    conn = getMySQLConnection()
    cur = conn.cursor()
    sql = "SELECT COUNTRY from kb_ip_address_merge GROUP BY COUNTRY"
    count = cur.execute(sql)
    resNum = 0
    print 'find %d records' % count
    if count:
        res = cur.fetchall()
        for re in res:
            country = re[0].encode("utf8")
            sql = "SELECT ID from kb_country_geo WHERE COUNTRY_ZH like '%{country}%'".format(country=country)
            count1 = cur.execute(sql)
            if count1 == 0:
                print "don't find country " + country
                resNum += 1
            else:
                pass

    cur.close()
    conn.commit()
    conn.close()
    timeEnd = time.time()
    print u'==================处理结束 耗时 %f 秒 =================' % (timeEnd - timeStart)
    print "resNum:" + str(resNum)


def update_country():
    timeStart = time.time()
    conn = getMySQLConnection()
    cur = conn.cursor()
    sql = "SELECT COUNTRY from kb_ip_address_merge WHERE COUNTRY != '' and COUNTRY != '中国' GROUP BY COUNTRY"
    count = cur.execute(sql)
    resNum = 0
    print 'find %d records' % count
    if count:
        res = cur.fetchall()
        for re in res:
            country = re[0].encode("utf8")
            if country == "印度" or country == "俄罗斯":
                sql1 = "SELECT CODE_2,LATITUDE,LONGITUDE from kb_country_geo WHERE COUNTRY_ZH like '{country}'".format(
                    country=country)
            else:
                sql1 = "SELECT CODE_2,LATITUDE,LONGITUDE from kb_country_geo WHERE COUNTRY_ZH like '%{country}%'".format(
                    country=country)
            count1 = cur.execute(sql1)
            if count1 == 0:
                print "don't find country " + country
                resNum += 1
            else:
                res1 = cur.fetchall()[0]
                code = res1[0]
                lat = res1[1]
                lon = res1[2]
                if lat is None or lon is None:
                    continue
                sql2 = "UPDATE kb_ip_address_merge SET latitude = {lat},longitude ={lon},code='{code}' " \
                       "WHERE COUNTRY = '{country}'".format(lat=lat, lon=lon, code=code, country=country)

                cur.execute(sql2)

    cur.close()
    conn.commit()
    conn.close()
    timeEnd = time.time()
    print u'==================处理结束 耗时 %f 秒 =================' % (timeEnd - timeStart)
    print "resNum:" + str(resNum)


def update_city():
    timeStart = time.time()
    conn = getMySQLConnection()
    cur = conn.cursor()
    sql = "SELECT area, city from kb_ip_address_merge WHERE code='CN' GROUP BY area,city"
    count = cur.execute(sql)
    print 'find %d records' % count
    resNum = 0
    if count:
        res = cur.fetchall()
        for re in res:
            code = "CN"
            area_ori = re[0]
            city_ori = re[1]
            area_ori = area_ori.encode("utf8")
            city_ori = city_ori.encode("utf8")
            area = re[0]
            city = re[1]
            if area == "":
                area = u'北京市'

            if city.find(u"自治州") > -1:
                city = city[:-3]
            elif city.find(u"市") > -1 or city.find(u'州') > -1 or city.find(u'县') > -1:
                if city == u'福州':
                    pass
                else:
                    city = city[:-1]
            elif city.find(u'地区') > -1:
                city = city[:-2]
            area = area.encode("utf8")
            city = city.encode("utf8")
            sql = "SELECT latitude, longitude, PROVINCE, city from kb_city WHERE PROVINCE = '{area}' and DISTRICT like'{city}%'".format(
                area=area, city=city)
            count1 = cur.execute(sql)
            if count1 == 0:
                resNum += 1
                print "{area},{city} don't exist".format(area=area, city=city)
            elif count1 >= 1:
                re1 = cur.fetchall()[0]
                lat = re1[0]
                lon = re1[1]
                sql1 = "UPDATE kb_ip_address_merge SET latitude = {lat},longitude ={lon}, code='{code}' " \
                       "WHERE area = '{area}' and city='{city}' and code ='CN'".format(lat=lat, lon=lon, code=code,
                                                                                       area=area_ori,
                                                                                       city=city_ori)
                cur.execute(sql1)
                print "{area},{city}  ".format(area=area, city=city) + str(count1)
            else:
                print "error---------------------------------"

    cur.close()
    conn.commit()
    conn.close()
    timeEnd = time.time()
    print u'==================处理结束 耗时 %f 秒 =================' % (timeEnd - timeStart)
    print "resNum:" + str(resNum)


def merge_two_db():
    print u'======== 合并数据库 ========'
    timeStart = time.time()
    resNum = 0
    conn = getMySQLConnection()
    cur = conn.cursor()
    sql = "SELECT `IP_START`, `IP_END` FROM kb_ip_address ORDER BY IP_START,IP_END limit 1000000,500000"
    count = cur.execute(sql)
    print 'find %d records' % count
    if count:
        res = cur.fetchall()
        data = None
        for index, d in enumerate(res):
            if index % 1000 == 0:
                print index, resNum

            item = {}
            item['IP_START'] = d[0]
            item['IP_END'] = d[1]
            if data and data['IP_END'] + 1 == item['IP_START']:
                pass
            else:
                # resNum +=1
                if data:
                    print data['IP_END'], item['IP_START'], convert_int2Ip(data['IP_END']), convert_int2Ip(
                        item['IP_START'])
                    # 算出来的空隙完全被merge库的某条记录覆盖的情况
                    tmp_ip = data['IP_END'] - 268435455

                    if tmp_ip <= 0:
                        tmp_ip = 0
                    sql1 = "SELECT IP_START,IP_END,IP_START_STR,IP_END_STR,COUNTRY,AREA,CITY,LATITUDE,LONGITUDE,MESSAGE,CODE from kb_ip_address_merge " \
                           "WHERE IP_START >= {tmp_ip} and IP_START<{ip1} and IP_END > {ip2}".format(ip1=data['IP_END'],
                                                                                                     ip2=item[
                                                                                                         'IP_START'],
                                                                                                     tmp_ip=tmp_ip)

                    # 算出来的空隙包含merge库里的多条记录
                    # sql1 = "SELECT IP_START,IP_END,IP_START_STR,IP_END_STR,COUNTRY,AREA from kb_ip_address_merge " \
                    #            "WHERE IP_START>{ip1} and IP_END < {ip2}".format(ip1=data['IP_END'],
                    #                                                           ip2=item['IP_START'])
                    timeStart1 = time.time()
                    count1 = cur.execute(sql1)
                    timeStart2 = time.time()
                    # print "one query %f" % (timeStart2 - timeStart1)
                    if count1 == 0:
                        # print "{start},{end},{start_str},{end_str},{count}".format(start=str(data['IP_END']),
                        #                                                            end=str(item['IP_START']),
                        #                                                            start_str=convert_int2Ip(
                        #                                                                data['IP_END']),
                        #                                                            end_str=convert_int2Ip(
                        #                                                                item['IP_START']),
                        #                                                            count=str(
                        #                                                                count1))
                        # print "ssss"
                        pass
                    elif count1 == 1:
                        resNum += 1
                        re = cur.fetchall()[0]
                        # ip_s = re[0]
                        # ip_e = re[1]
                        # ip_s_s = re[2]
                        # ip_e_s = re[3]
                        ip_s = data['IP_END'] + 1
                        ip_e = item['IP_START'] - 1
                        ip_s_s = convert_int2Ip(ip_s)
                        ip_e_s = convert_int2Ip(ip_e)
                        country = re[4].encode("utf8")
                        area = re[5].encode("utf8")
                        city = re[6].encode("utf8")
                        lat = re[7]
                        lon = re[8]
                        msg = re[9].encode("utf8")
                        code = re[10].encode("utf8")

                        if lat is None:
                            lat = 'null'
                        if lon is None:
                            lon = 'null'
                        sql2 = "INSERT INTO `kb_ip_address` VALUES ('{ip_s}', '{ip_e}', '0', " \
                               "'{country}', '{area}', '{city}', {lat}, {lon}, '{msg}', '{code}'," \
                               " '', '{ip_s_s}', '{ip_e_s}')".format(ip_e=ip_e, ip_s=ip_s, country=country,
                                                                     area=area, city=city, lat=lat, lon=lon,
                                                                     msg=msg, code=code, ip_s_s=ip_s_s,
                                                                     ip_e_s=ip_e_s)

                        # timeStart1 = time.time()
                        cur.execute(sql2)
                        # timeStart2 = time.time()
                        # print "one insert %f" % (timeStart2 - timeStart1)
                        # print "{start},{end},{start_str},{end_str},{count}".format(start=str(data['IP_END']),
                        #                                                            end=str(item['IP_START']),
                        #                                                            start_str=convert_int2Ip(
                        #                                                                data['IP_END']),
                        #                                                            end_str=convert_int2Ip(
                        #                                                                item['IP_START']),
                        #                                                            count=str(
                        #                                                                count1))
                        pass
                    else:
                        # print "{start},{end},{start_str},{end_str},{count}".format(start=str(data['IP_END']),
                        #                                                            end=str(item['IP_START']),
                        #                                                            start_str=convert_int2Ip(
                        #                                                                data['IP_END']),
                        #                                                            end_str=convert_int2Ip(
                        #                                                                item['IP_START']),
                        #                                                            count=str(
                        #                                                                count1))

                        pass
            data = item

    cur.close()
    conn.close()
    print '%d 条数据已处理' % resNum

    timeEnd = time.time()
    print u'\n\n\n==================处理结束 耗时 %f 秒 =================\n\n\n' % (timeEnd - timeStart)


def merge_two_db_1():
    print u'======== 合并数据库 ========'
    timeStart = time.time()
    resNum = 0
    conn = getMySQLConnection()
    cur = conn.cursor()
    sql = "SELECT `IP_START`, `IP_END` FROM kb_ip_address ORDER BY IP_START,IP_END"

    count = cur.execute(sql)
    print 'find %d records' % count
    if count:
        res = cur.fetchall()
        result = []
        data = None
        for index, d in enumerate(res):
            if index % 1000 == 0:
                print index, resNum

            item = {}
            item['IP_START'] = d[0]
            item['IP_END'] = d[1]
            if data and data['IP_END'] + 1 == item['IP_START']:
                pass
            else:
                # resNum += 1
                if data:
                    # 算出来的空隙包含merge库里的多条记录


                    sql1 = "SELECT IP_START,IP_END,IP_START_STR,IP_END_STR,COUNTRY,AREA,CITY,LATITUDE,LONGITUDE,MESSAGE,CODE from kb_ip_address_merge " \
                           "WHERE IP_START>{ip1} and IP_START < {ip2} and IP_END < {ip2}".format(ip1=data['IP_END'],
                                                                                                 ip2=item['IP_START'])

                    # timeStart1 = time.time()
                    count1 = cur.execute(sql1)
                    # timeStart2 = time.time()
                    # print "one insert %f" % (timeStart2 - timeStart1)
                    if count1 == 0:
                        # print "{start},{end},{start_str},{end_str},{count}".format(start=str(data['IP_END']),
                        #                                                            end=str(item['IP_START']),
                        #                                                            start_str=convert_int2Ip(
                        #                                                                data['IP_END']),
                        #                                                            end_str=convert_int2Ip(
                        #                                                                item['IP_START']),
                        #                                                            count=str(
                        #                                                                count1))
                        # print "ssss"
                        pass
                    elif count1 >= 1:
                        resNum += 1
                        # res = cur.fetchall()
                        # for re in res:
                        #     ip_s = re[0]
                        #     ip_e = re[1]
                        #     ip_s_s = re[2]
                        #     ip_e_s = re[3]
                        #     country = re[4].encode("utf8")
                        #     area = re[5].encode("utf8")
                        #     city = re[6].encode("utf8")
                        #     lat = re[7]
                        #     lon = re[8]
                        #     msg = re[9].encode("utf8")
                        #     code = re[10].encode("utf8")
                        #
                        #     if lat is None:
                        #         lat = 'null'
                        #     if lon is None:
                        #         lon = 'null'
                        #     sql2 = "INSERT INTO `kb_ip_address` VALUES ('{ip_s}', '{ip_e}', '0', " \
                        #            "'{country}', '{area}', '{city}', {lat}, {lon}, '{msg}', '{code}'," \
                        #            " '', '{ip_s_s}', '{ip_e_s}')".format(ip_e=ip_e, ip_s=ip_s, country=country,
                        #                                                  area=area, city=city, lat=lat, lon=lon,
                        #                                                  msg=msg, code=code, ip_s_s=ip_s_s,
                        #                                                  ip_e_s=ip_e_s)
                        #     cur.execute(sql2)
                        # # print "{start},{end},{start_str},{end_str},{count}".format(start=str(data['IP_END']),
                        # #                                                            end=str(item['IP_START']),
                        # #                                                            start_str=convert_int2Ip(
                        # #                                                                data['IP_END']),
                        # #                                                            end_str=convert_int2Ip(
                        # #                                                                item['IP_START']),
                        # #                                                            count=str(
                        # #                                                                count1))
                        pass
                    else:
                        # print "{start},{end},{start_str},{end_str},{count}".format(start=str(data['IP_END']),
                        #                                                            end=str(item['IP_START']),
                        #                                                            start_str=convert_int2Ip(
                        #                                                                data['IP_END']),
                        #                                                            end_str=convert_int2Ip(
                        #                                                                item['IP_START']),
                        #                                                            count=str(
                        #                                                                count1))

                        pass
            data = item
    cur.close()
    conn.close()
    print '%d 条数据已处理' % resNum

    timeEnd = time.time()
    print u'\n\n\n==================处理结束 耗时 %f 秒 =================\n\n\n' % (timeEnd - timeStart)


def merge_two_db_2():
    print u'======== 合并数据库 ========'
    timeStart = time.time()
    resNum = 0
    conn = getMySQLConnection()
    cur = conn.cursor()
    sql = "SELECT `IP_START`, `IP_END` FROM kb_ip_address ORDER BY IP_START,IP_END"

    count = cur.execute(sql)
    print 'find %d records' % count
    if count:
        res = cur.fetchall()
        result = []
        data = None
        for index, d in enumerate(res):
            if index % 1000 == 0:
                print index, resNum

            item = {}
            item['IP_START'] = d[0]
            item['IP_END'] = d[1]
            if data and data['IP_END'] + 1 == item['IP_START']:
                pass
            else:
                if data:
                    print data['IP_END'], item['IP_START'], convert_int2Ip(data['IP_END']), convert_int2Ip(
                        item['IP_START'])

                    tmp_ip = data['IP_END'] - 20220671
                    if tmp_ip <= 0:
                        tmp_ip = 0
                    # 算出来的空隙左边界大于merge的某条数据的左边界，空隙右边界大于merge的某条数据的右边界
                    sql1 = "SELECT IP_START,IP_END,IP_START_STR,IP_END_STR,COUNTRY,AREA,CITY,LATITUDE,LONGITUDE,MESSAGE,CODE from kb_ip_address_merge " \
                           "WHERE IP_START > {tmp_ip} and IP_START <= {ip1} and IP_END <= {ip2} and IP_END > {ip1}".format(
                        ip1=data['IP_END'],
                        ip2=item['IP_START'], tmp_ip=tmp_ip)

                    # timeStart1 = time.time()
                    count1 = cur.execute(sql1)
                    # timeStart2 = time.time()
                    # print "one insert %f" % (timeStart2 - timeStart1)
                    if count1 == 0:
                        # print "{start},{end},{start_str},{end_str},{count}".format(start=str(data['IP_END']),
                        #                                                            end=str(item['IP_START']),
                        #                                                            start_str=convert_int2Ip(
                        #                                                                data['IP_END']),
                        #                                                            end_str=convert_int2Ip(
                        #                                                                item['IP_START']),
                        #                                                            count=str(
                        #                                                                count1))
                        # print 1
                        pass
                    elif count1 == 1:
                        # resNum += 1
                        print "{start},{end},{start_str},{end_str},{count}".format(start=str(data['IP_END']),
                                                                                   end=str(item['IP_START']),
                                                                                   start_str=convert_int2Ip(
                                                                                       data['IP_END']),
                                                                                   end_str=convert_int2Ip(
                                                                                       item['IP_START']),
                                                                                   count=str(
                                                                                       count1))

                        re = cur.fetchall()[0]
                        ip_s = data['IP_END'] + 1
                        ip_e = re[1]
                        if ip_e == item['IP_START']:
                            ip_e = ip_e - 1
                        ip_s_s = convert_int2Ip(ip_s)
                        ip_e_s = convert_int2Ip(ip_e)
                        country = re[4].encode("utf8")
                        area = re[5].encode("utf8")
                        city = re[6].encode("utf8")
                        lat = re[7]
                        lon = re[8]
                        msg = re[9].encode("utf8")
                        code = re[10].encode("utf8")

                        if lat is None:
                            lat = 'null'
                        if lon is None:
                            lon = 'null'
                        sql2 = "INSERT INTO `kb_ip_address` VALUES ('{ip_s}', '{ip_e}', '0', " \
                               "'{country}', '{area}', '{city}', {lat}, {lon}, '{msg}', '{code}'," \
                               " '', '{ip_s_s}', '{ip_e_s}')".format(ip_e=ip_e, ip_s=ip_s, country=country,
                                                                     area=area, city=city, lat=lat, lon=lon,
                                                                     msg=msg, code=code, ip_s_s=ip_s_s,
                                                                     ip_e_s=ip_e_s)
                        cur.execute(sql2)

                        # print 2
                        pass
                    else:
                        # print "{start},{end},{start_str},{end_str},{count}".format(start=str(data['IP_END']),
                        #                                                            end=str(item['IP_START']),
                        #                                                            start_str=convert_int2Ip(
                        #                                                                data['IP_END']),
                        #                                                            end_str=convert_int2Ip(
                        #                                                                item['IP_START']),
                        #                                                            count=str(
                        #                                                                count1))
                        print 3
                        pass
            data = item
    cur.close()
    conn.close()
    print '%d 条数据已处理' % resNum

    timeEnd = time.time()
    print u'\n\n\n==================处理结束 耗时 %f 秒 =================\n\n\n' % (timeEnd - timeStart)


def merge_two_db_3():
    print u'======== 合并数据库 ========'
    timeStart = time.time()
    resNum = 0
    conn = getMySQLConnection()
    cur = conn.cursor()
    sql = "SELECT `IP_START`, `IP_END` FROM kb_ip_address ORDER BY IP_START,IP_END"

    count = cur.execute(sql)
    print 'find %d records' % count
    if count:
        res = cur.fetchall()
        result = []
        data = None
        for index, d in enumerate(res):
            if index % 1000 == 0:
                print index, resNum

            item = {}
            item['IP_START'] = d[0]
            item['IP_END'] = d[1]
            if data and data['IP_END'] + 1 == item['IP_START']:
                pass
            else:
                if data:
                    print data['IP_END'], item['IP_START'], convert_int2Ip(data['IP_END']), convert_int2Ip(
                        item['IP_START'])
                    # resNum += 1
                    # # 算出来的空隙左边界小于merge的某条数据的左边界，空隙右边界小于merge的某条数据的右边界
                    sql1 = "SELECT IP_START,IP_END,IP_START_STR,IP_END_STR,COUNTRY,AREA,CITY,LATITUDE,LONGITUDE,MESSAGE,CODE from kb_ip_address_merge " \
                           "WHERE IP_START < {ip2} and IP_START >= {ip1} and IP_END >= {ip2} ".format(
                        ip1=data['IP_END'],
                        ip2=item['IP_START'])

                    # timeStart1 = time.time()
                    count1 = cur.execute(sql1)
                    # timeStart2 = time.time()
                    # print "one insert %f" % (timeStart2 - timeStart1)
                    if count1 == 0:
                        # print "{start},{end},{start_str},{end_str},{count}".format(start=str(data['IP_END']),
                        #                                                            end=str(item['IP_START']),
                        #                                                            start_str=convert_int2Ip(
                        #                                                                data['IP_END']),
                        #                                                            end_str=convert_int2Ip(
                        #                                                                item['IP_START']),
                        #                                                            count=str(
                        #                                                                count1))
                        # print 1
                        pass
                    elif count1 == 1:
                        resNum += 1
                        print "{start},{end},{start_str},{end_str},{count}".format(start=str(data['IP_END']),
                                                                                   end=str(item['IP_START']),
                                                                                   start_str=convert_int2Ip(
                                                                                       data['IP_END']),
                                                                                   end_str=convert_int2Ip(
                                                                                       item['IP_START']),
                                                                                   count=str(
                                                                                       count1))

                        re = cur.fetchall()[0]
                        ip_s = re[0]
                        if ip_s == data['IP_END']:
                            ip_s += 1
                        ip_e = item['IP_START'] - 1
                        ip_s_s = convert_int2Ip(ip_s)
                        ip_e_s = convert_int2Ip(ip_e)
                        country = re[4].encode("utf8")
                        area = re[5].encode("utf8")
                        city = re[6].encode("utf8")
                        lat = re[7]
                        lon = re[8]
                        msg = re[9].encode("utf8")
                        code = re[10].encode("utf8")

                        if lat is None:
                            lat = 'null'
                        if lon is None:
                            lon = 'null'
                        sql2 = "INSERT INTO `kb_ip_address` VALUES ('{ip_s}', '{ip_e}', '0', " \
                               "'{country}', '{area}', '{city}', {lat}, {lon}, '{msg}', '{code}'," \
                               " '', '{ip_s_s}', '{ip_e_s}')".format(ip_e=ip_e, ip_s=ip_s, country=country,
                                                                     area=area, city=city, lat=lat, lon=lon,
                                                                     msg=msg, code=code, ip_s_s=ip_s_s,
                                                                     ip_e_s=ip_e_s)
                        cur.execute(sql2)

                        # print 2
                        pass
                    else:
                        # print "{start},{end},{start_str},{end_str},{count}".format(start=str(data['IP_END']),
                        #                                                            end=str(item['IP_START']),
                        #                                                            start_str=convert_int2Ip(
                        #                                                                data['IP_END']),
                        #                                                            end_str=convert_int2Ip(
                        #                                                                item['IP_START']),
                        #                                                            count=str(
                        #                                                                count1))
                        print 3
                        pass
            data = item
    cur.close()
    conn.close()
    print '%d 条数据已处理' % resNum

    timeEnd = time.time()
    print u'\n\n\n==================处理结束 耗时 %f 秒 =================\n\n\n' % (timeEnd - timeStart)


def merge_two_db_4():
    print u'======== 合并数据库 ========'
    timeStart = time.time()
    resNum = 0
    conn = getMySQLConnection()
    cur = conn.cursor()
    sql = "SELECT `IP_START`, `IP_END` FROM KB_IP_ADDRESS ORDER BY IP_START,IP_END"

    count = cur.execute(sql)
    print 'find %d records' % count
    if count:
        res = cur.fetchall()
        result = []
        data = None
        for index, d in enumerate(res):
            # if index % 1000 == 0:
            # print index, resNum

            item = {}
            item['IP_START'] = d[0]
            item['IP_END'] = d[1]
            if data and data['IP_END'] + 1 == item['IP_START']:
                pass
            else:
                if data:
                    resNum += 1
                    print data['IP_END'], item['IP_START'], convert_int2Ip(data['IP_END']), convert_int2Ip(
                        item['IP_START'])

                    # # # 算出来的空隙左边界小于merge的某条数据的左边界，空隙右边界小于merge的某条数据的右边界
                    # sql1 = "SELECT IP_START,IP_END,IP_START_STR,IP_END_STR,COUNTRY,AREA,CITY,LATITUDE,LONGITUDE,MESSAGE,CODE from kb_ip_address_merge " \
                    #        "WHERE IP_START < {ip2} and IP_START >= {ip1} and IP_END > {ip2} ".format(
                    #     ip1=data['IP_END'],
                    #     ip2=item['IP_START'])
                    #
                    # # timeStart1 = time.time()
                    # count1 = cur.execute(sql1)
                    # # timeStart2 = time.time()
                    # # print "one insert %f" % (timeStart2 - timeStart1)
                    # if count1 == 0:
                    #     # print "{start},{end},{start_str},{end_str},{count}".format(start=str(data['IP_END']),
                    #     #                                                            end=str(item['IP_START']),
                    #     #                                                            start_str=convert_int2Ip(
                    #     #                                                                data['IP_END']),
                    #     #                                                            end_str=convert_int2Ip(
                    #     #                                                                item['IP_START']),
                    #     #                                                            count=str(
                    #     #                                                                count1))
                    #     # print 1
                    #     pass
                    # elif count1 == 1:
                    #     resNum += 1
                    #     print "{start},{end},{start_str},{end_str},{count}".format(start=str(data['IP_END']),
                    #                                                                end=str(item['IP_START']),
                    #                                                                start_str=convert_int2Ip(
                    #                                                                    data['IP_END']),
                    #                                                                end_str=convert_int2Ip(
                    #                                                                    item['IP_START']),
                    #                                                                count=str(
                    #                                                                    count1))
                    #     #
                    #     re = cur.fetchall()[0]
                    #     ip_s = re[0]
                    #     if ip_s == data['IP_END']:
                    #         ip_s += 1
                    #     ip_e = item['IP_START'] - 1
                    #     ip_s_s = convert_int2Ip(ip_s)
                    #     ip_e_s = convert_int2Ip(ip_e)
                    #     country = re[4].encode("utf8")
                    #     area = re[5].encode("utf8")
                    #     city = re[6].encode("utf8")
                    #     lat = re[7]
                    #     lon = re[8]
                    #     msg = re[9].encode("utf8")
                    #     code = re[10].encode("utf8")
                    #
                    #     if lat is None:
                    #         lat = 'null'
                    #     if lon is None:
                    #         lon = 'null'
                    #     sql2 = "INSERT INTO `kb_ip_address` VALUES ('{ip_s}', '{ip_e}', '0', " \
                    #            "'{country}', '{area}', '{city}', {lat}, {lon}, '{msg}', '{code}'," \
                    #            " '', '{ip_s_s}', '{ip_e_s}')".format(ip_e=ip_e, ip_s=ip_s, country=country,
                    #                                                  area=area, city=city, lat=lat, lon=lon,
                    #                                                  msg=msg, code=code, ip_s_s=ip_s_s,
                    #                                                  ip_e_s=ip_e_s)
                    #     # cur.execute(sql2)
                    #     #
                    #     print 2
                    #     pass
                    # else:
                    #     # print "{start},{end},{start_str},{end_str},{count}".format(start=str(data['IP_END']),
                    #     #                                                            end=str(item['IP_START']),
                    #     #                                                            start_str=convert_int2Ip(
                    #     #                                                                data['IP_END']),
                    #     #                                                            end_str=convert_int2Ip(
                    #     #                                                                item['IP_START']),
                    #     #                                                            count=str(
                    #     #                                                                count1))
                    #     print 3
                    #     pass
            data = item
    cur.close()
    conn.close()
    print '%d 条数据已处理' % resNum

    timeEnd = time.time()
    print u'\n\n\n==================处理结束 耗时 %f 秒 =================\n\n\n' % (timeEnd - timeStart)


def convert_to_redis():
    print u'======== 合并数据库 ========'
    timeStart = time.time()
    conn = getMySQLConnection()
    cur = conn.cursor()
    sql = "SELECT * FROM KB_IP_ADDRESS ORDER BY IP_START,IP_END"

    count = cur.execute(sql)
    result = []
    print 'find %d records' % count
    if count:
        res = cur.fetchall()
        for re in res:
            IP_START = str(re[0])
            IP_END = str(re[1])
            IP_NETWORK = str(re[2])
            COUNTRY = re[3].encode('utf-8')
            AREA = re[4].encode('utf-8')
            CITY = re[5].encode('utf-8')
            LATITUDE = re[6]
            if LATITUDE is None:
                LATITUDE = ""
            else:
                LATITUDE = str(LATITUDE)
            LONGITUDE = re[7]
            if LONGITUDE is None:
                LONGITUDE = ""
            else:
                LONGITUDE = str(LONGITUDE)
            MESSAGE = re[8].encode('utf-8')
            CODE = re[9]
            if CODE is None:
                CODE = ""
            else:
                CODE = CODE.encode('utf-8')
            COUNTRY_EN = re[10].encode('utf-8')

            result.append(",".join(
                [IP_START, IP_END, IP_NETWORK, COUNTRY, AREA, CITY, LATITUDE, LONGITUDE, MESSAGE, CODE,
                 COUNTRY_EN]) + "\n")
    cur.close()
    conn.close()
    path = r"C:\Users\Administrator\Desktop\GEOIP_DATAS.txt"
    with open(path, "w") as f:
        f.writelines(result)

    timeEnd = time.time()
    print u'\n\n\n==================处理结束 耗时 %f 秒 =================\n\n\n' % (timeEnd - timeStart)


if __name__ == '__main__':
    # print "北京北京".decode('utf8').encode("utf8")[:-1]
    # print MySQLdb.escape_string("Seoul Seoul-t'ukpyolsi Korea Republic".encode('utf-8'))
    # innodb insert 5 million data 2809 seconds
    # add_to_table()
    # check_continuity()
    # merge_date()
    # add_merge_data_to_db()
    # supplement_country_geo()
    # is_city_geo_exist()
    # is_country_geo_exist()
    # update_country()
    # update_city()
    # merge_two_db()
    # merge_two_db_1()
    # merge_two_db_2()
    # merge_two_db_3()
    # merge_two_db_4()
    convert_to_redis()
