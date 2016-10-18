#! usr/bin/python
# -*- coding:utf-8 -*-

import httplib
import os
import shutil
import urllib
import urllib2
import cookielib


class Lottery:
    def __init__(self):
        opener = None
        cookie = None
        cookie_value = None

    def send_http(self, www, req):
        conn = httplib.HTTPConnection(www)
        cookie_value = '_lcas_uuid=223720485; _lcas_uuid=223720485; _lhc_uuid=sp_57850ecd81ece2.24662928; cookie_old_user_ad_time_2803225468=1; cookie_old_user_ad_num_2803225468=1; cookie_old_user_ad_2803225468=1; _lcas_uuid=223720485; _adwr=110406678%23http%253A%252F%252Ftrend.baidu.lecai.com%252Fssq%252F; LSID=sn86p6041c1qsnrjlaoil5ivu7; _adwp=110406678.5006763439.1468338246.1473152446.1473160629.4; _adwc=110406678; lehecai_request_control_stats=2; bds_yRlmiCbrv56CcjfMwS21DkqP=expires_in%3D2592000%26refresh_token%3D22.20952ff8fa9a7ed3260a9612f4e5b873.315360000.1788514951.742743018-106251%26access_token%3D21.d2f17babafa6c1a1df45000ebbe0af7d.2592000.1475746951.742743018-106251%26session_secret%3D78a73b4d2072dd61f89160ae7da157d9%26session_key%3D9mnRIBmE8Q%252FxQVSJ9zKP0ObkuNY1fEmGTJavnBZkvtQxTTQCZ37h6zm3vxz2t8qu3uYNodPTrqJRZ6IQDyf%252Bn3z6ZVyAjwA%253D%26scope%3Dbasic%2Bsuper_msg%26uid%3D742743018%26uname%3D186%252A%252A%252A%252A%252A348%26portrait%3D152c3541; _adwb=110406678; Hm_lvt_6c5523f20c6865769d31a32a219a6766=1473130088,1473130114; Hm_lpvt_6c5523f20c6865769d31a32a219a6766=1473160643; paypassword=sig%3D6ffedb764d3c8d543aa2aae69081e0d6%2Cuid%3D2803225468%2Cts%3D1473160642%2Cexpire%3D1200%2Cstatus%3D0%2Crc%3Dcd2a1aea4ee31c190ba551e2b5375d08; lehecai_request_control_userinfo=1; Hm_lvt_9b75c2b57524b5988823a3dd66ccc8ca=1473130088,1473130114; Hm_lpvt_9b75c2b57524b5988823a3dd66ccc8ca=1473160643'
        accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        accept_encoding = 'gzip, deflate, sdch'
        accept_language = 'zh-CN,zh;q=0.8'
        referer = 'http://baidu.lecai.com/lottery/draw/list/50'
        user_agent = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        conn.request("GET", req,
                     headers={'User-agent': user_agent, 'Accept': accept, 'Accept-encoding': accept_encoding,
                              'Accept-language': accept_language,
                              'Referer': referer, 'Cookie': cookie_value})
        re1 = conn.getresponse()
        data = re1.read()
        conn.close()
        return data

    def send_http_1(self, url):

        cookie_value = '_lhc_uuid=sp_57850ecd81ece2.24662928; _adwr=112321473%23http%253A%252F%252Fbaidu.lecai.com%252Flottery%252Fdraw%252F; cookie_old_user_ad_time_2803225468=1; cookie_old_user_ad_num_2803225468=1; cookie_old_user_ad_2803225468=1; bds_yRlmiCbrv56CcjfMwS21DkqP=expires_in%3D2592000%26refresh_token%3D22.f81e006fd3530cfa63ccc4030efe5488.315360000.1788878231.742743018-106251%26access_token%3D21.ad74867f93da11f6eccc0237b3677c74.2592000.1476110231.742743018-106251%26session_secret%3De0a7e49eec23bee89d5d345f6350a09a%26session_key%3D9mnRJaIXg2YtE6QjEJ9E6jdHkUv8aly7aMz%252FysnC2MIyS%252B8DzvhIlj%252BcMKTurFV1dVvyzwKHGp07x4jV%252BzcbbtIhituBvzE%253D%26scope%3Dbasic%2Bsuper_msg%26uid%3D742743018%26uname%3D186%252A%252A%252A%252A%252A348%26portrait%3D152c3541; LSID=9pfmes2f8ko4qr949okl42jnn0; lehecai_request_control_stats=2; _adwp=110406678.5006763439.1468338246.1473518189.1473521856.5; _adwb=110406678; _adwc=110406678; Hm_lvt_9b75c2b57524b5988823a3dd66ccc8ca=1473130088,1473130114; Hm_lpvt_9b75c2b57524b5988823a3dd66ccc8ca=1473521856; lc_login_response=%7B%22code%22%3A0%2C%22message%22%3A%22%22%2C%22data%22%3A%7B%22uid%22%3A%222157031462%22%2C%22username%22%3A%2218600958348%22%2C%22discuz%22%3A%22gXUL1obAtcuZEPwB3Y1BHpYvzPWzTByZKGZ9r2lKJqAQPK%5C%2F6GGmXNotEP2bY7IySI4oGxTe1WcK8mtexlME4RKgoXRN58NirTX0llBeKd6T8S1Bh%5C%2F%2B5IKAx92l9Xjc0YkWOp5IXY%2BCMZxHytt3MrxdKRA1cOpQnQ%5C%2FBMR%5C%2FatA8PfWOjQMSAILZMiJp2kpxuf3ayEK%5C%2FB%5C%2FRNXQtwo07PYI2zTzHkoa7W%2BMvt74q02Cowrh%5C%2FzyIsXNU6f7ygt8THP7xlKtw1c7eX0dMsaKhrE83qp8vSvVZ5EooRa8vtsZLNhwKLA1SF5u0ISZzi7HycdLm1Frcbn5SrJXG1sziAopb4prx5Rzw58nKSqem5bV1snO2yhH6rBvu85htXOudgWd7SekemJ2FT6PxSSmfzveNV%5C%2F3AcwChdcH5KDvLpTZ8RLEYnYnLn9uozxmSKJziml15WFlNL4RJrJEpJdAtRHU8l9vcVihhoW5baHBs%2B09RsAiaP70NQtvMcUKSFM6ciC2Eu0xatgyvfD0iYplraNyDyo05ElDu9JJALJhHfVFmWk79XDjCZrLGTb%2BGWAzU0JvxfUewSjyjbLMgxx7R59Ozkgb0%2BKmuHa%2BpRp7KhMHn7pXCeosAppNgj4JTOeBjUbOW3DCLqUS2pt%5C%2FvVffLnhfGZ9EoE%5C%2FTpWo4B10dX2ehTcnTy1P5tzWLCqY1PZYHzgh%2BRYDUYciC5%5C%2FizZtDrvD6aVjjhTAEJFYfYsAQtPFGi03hgDUI%5C%2Fk%2Bg761G9hbCb5QKRjOVrJ%5C%2F2KW6t23KMqtLo6tFp0C%5C%2F8QSIwjW1KN3dbmwXCFCZEGX92Sub3alF96zjqxlnJQES1csTKDQbL5bX2hrY%2BWAWN4dv7JzomkeIPfndEbpWOob683qRb8idX0%5C%2FHSG3b4xkuw%5C%2FRb9229tUGWABDWPNsR4xzXxiEwy0xOm34i%2Bz%5C%2FKKBvce6pJbGAZnXfWPLGqFo1cfWAid86%2BbfAL27by02RLb9DNQZ02jwEVWcbHHqyK2NxAv%5C%2FT%5C%2FNiMpzALxp%2Bo0SHiZgOBI%2BMyI07YdE5u3M%5C%2FrUbWaWdwAB7F7HFly4JrtnW%5C%2FOrNrWpN6Mwwfrxlk6jyKyiqXplewP2RCUf2HVvi5xdnUJB32puTSnP2Q5aErC%5C%2F8tcqKOrX%2Bt9r4Nwh5A5ZR6BI5hIWj7R7Tc982dfM1F%5C%2FfTl8pgAfHuXcEsV0gW9SbMNSObETtkIS9OxEw8weaj1VMFNJ8UtR0m0Ib%2BNKyGB%2Bn1ELCZ93RRvGzrWJuiW0%3D%22%7D%2C%22redirect%22%3A%22http%3A%5C%2F%5C%2Fbaidu.lecai.com%5C%2F%22%2C%22exception%22%3A%22%22%7D; Hm_lvt_6c5523f20c6865769d31a32a219a6766=1473130088,1473130114,1473506695; Hm_lpvt_6c5523f20c6865769d31a32a219a6766=1473521861; paypassword=sig%3D84c3e0fbd12130c1ba35172d56c56d16%2Cuid%3D2157031462%2Cts%3D1473521859%2Cexpire%3D1200%2Cstatus%3D0%2Crc%3D7f710aa5c2da22a0180e1fc75f777193; lehecai_request_control_userinfo=1; _lcas_uuid=1827463803'
        # cookie_value = self.cookie_value
        accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        accept_encoding = 'gzip, deflate, sdch'
        accept_language = 'zh-CN,zh;q=0.8'
        referer = 'http://baidu.lecai.com/lottery/draw/list/50'
        user_agent = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
        headers = {'User-agent': user_agent, 'Accept': accept, 'Accept-encoding': accept_encoding,
                   'Accept-language': accept_language,
                   'Referer': referer, 'Cookie': cookie_value}
        # website = raw_input('请输入网址:')

        # cookie = self.cookie
        # cookie = cookielib.MozillaCookieJar('C:\\temp\\cookie.txt')
        # self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))

        req = urllib2.Request(url=url, data=None, headers=headers)
        resp = self.opener.open(req)
        data = resp.read()
        resp.close()
        return data

    def split_url(self, url):
        url_new = url.replace('http://', '').replace('https://', '')
        index1 = url_new.find('/')
        if index1 > 0:
            www = url_new[0:index1]
            request_url = url_new[index1:]
            return [www, request_url]
        else:
            return [url, '/']

    def get_all_data(self, dest):
        if os.path.exists(dest) is False:
            os.mkdir(dest)

        for i in range(2003, 2017):
            print i
            url = 'http://baidu.lecai.com/lottery/draw/phase_result_download.php?file_format=txt&lottery_type=50&year=' + str(
                i)
            # www = self.split_url(url)[0]
            # req = self.split_url(url)[1]
            # data = self.send_http(www, req)
            data = self.send_http_1(url)
            path = dest + os.path.sep + str(i) + '.txt'

            with open(path, 'w') as f:
                f.write(data)

    def get_verify_code(self, url):
        pic = self.opener.open(url).read()
        with open('c:/temp/verifyImg.jpg', 'wb') as emptyPic:
            emptyPic.write(pic)

    def login(self):

        verify = raw_input("请输入验证码:")
        username = '18600958348'
        passwd = 'lglcomcn'

        data = {"username": username, "passwd": passwd, "verify": verify,
                "referer": "http://www.lecai.com/"}  # 登陆用户名和密码
        post_data = urllib.urlencode(data)  # 将post消息化成可以让服务器编码的方式

        # 自己设置User-Agent（可用于伪造获取，防止某些网站防ip注入）
        headers = {"User-agent": "Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1"}
        # website = raw_input('请输入网址:')
        website = 'http://www.lecai.com/user/ajax_login.php'
        req = urllib2.Request(website, post_data, headers)
        content = self.opener.open(req)
        self.cookie_value = content.headers.dict['set-cookie']
        print self.cookie_value
        print content.read()  # linux下没有gbk编码，只有utf-8编码

    def main_login(self):

        cookie_path = 'C:\\temp\\cookie.txt'
        # self.cookie = cookielib.CookieJar()  # 获取cookiejar实例
        self.cookie = cookielib.MozillaCookieJar(cookie_path)
        # self.cookie = cookielib.LWPCookieJar(cookie_path)

        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(self.cookie))
        verify_code_url = 'http://www.lecai.com/captcha.php'
        self.get_verify_code(verify_code_url)
        self.login()
        self.cookie.save()


import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Table, Column, INTEGER, VARCHAR, DATE, FLOAT
import traceback
import re

Base = declarative_base()


class Lottery_Obj(Base):
    __tablename__ = 'lottery_obj'

    lo_id = Column('lo_id', INTEGER, primary_key=True, nullable=False)
    number = Column('collector_name', VARCHAR(10))
    red_0 = Column('red_0', INTEGER)
    red_1 = Column('red_1', INTEGER)
    red_2 = Column('red_2', INTEGER)
    red_3 = Column('red_3', INTEGER)
    red_4 = Column('red_4', INTEGER)
    red_5 = Column('red_5', INTEGER)
    blue = Column('blue', INTEGER)
    open_date = Column('open_date', DATE)
    standby0 = Column('standby0', VARCHAR(50))
    standby1 = Column('standby1', INTEGER)
    standby2 = Column('standby2', FLOAT)


class PreHandle:
    _session = sessionmaker()

    def __init__(self, path):
        self._path = path

        self._count_number = 0
        self._result_red = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
            8: 0,
            9: 0,
            10: 0,
            11: 0,
            12: 0,
            13: 0,
            14: 0,
            15: 0,
            16: 0,
            17: 0,
            18: 0,
            19: 0,
            20: 0,
            21: 0,
            22: 0,
            23: 0,
            24: 0,
            25: 0,
            26: 0,
            27: 0,
            28: 0,
            29: 0,
            30: 0,
            31: 0,
            32: 0,
            33: 0
        }
        self._result_blue = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0,
            8: 0,
            9: 0,
            10: 0,
            11: 0,
            12: 0,
            13: 0,
            14: 0,
            15: 0,
            16: 0
        }

    @classmethod
    def db_init(cls, db_user, db_passwd, db_ip, db_name):
        engine = create_engine(
            'mysql://' +
            db_user + ':' +
            db_passwd + '@' +
            db_ip + '/' +
            db_name + '?charset=utf8',
            echo=True,
            poolclass=sqlalchemy.pool.QueuePool,
            pool_size=100,
            pool_recycle=7200)
        if engine is not None:
            try:
                base = Base
                base.metadata.create_all(engine)
                cls._session.configure(bind=engine)
                return True
            except Exception:
                exstr = traceback.format_exc()
                print exstr
                return False
        else:
            print 'init_db false!'
            return False

    def _get_session(self):
        """Get the ORM’s “handle” to the database,session

        Args:
            None
        Return:
            session or None
        """

        if PreHandle._session is not None:
            return PreHandle._session()
        else:
            return None

    def insert_to_db(self):
        try:
            files = os.listdir(self._path)
            list = []
            for file in files:

                pattern_data = '\d{4}'

                if re.match(pattern_data, file) is None:
                    continue
                else:
                    file_path = os.path.join(self._path, file)

                    with open(file_path, 'r') as f:
                        lines = f.readlines()
                        cc_list = []
                        for line in lines:
                            arr = line.split('    ')

                            number = arr[0]

                            r_arr = arr[1].split(',')
                            red_0 = int(r_arr[0])
                            red_1 = int(r_arr[1])
                            red_2 = int(r_arr[2])
                            red_3 = int(r_arr[3])
                            red_4 = int(r_arr[4])
                            red_5 = int(r_arr[5].split('|')[0])

                            blue = int(arr[1].split('|')[1])

                            open_date = arr[2]

                            lo = Lottery_Obj()
                            lo.number = number
                            lo.red_0 = red_0
                            lo.red_1 = red_1
                            lo.red_2 = red_2
                            lo.red_3 = red_3
                            lo.red_4 = red_4
                            lo.red_5 = red_5

                            lo.blue = blue

                            lo.open_date = open_date.strip()

                            list.append(lo)
            self.analyze(list)
            self.add_item(list)

        except Exception:
            exstr = traceback.format_exc()
            print exstr

    def add_item(self, list):
        try:
            session = self._get_session()
            for obj in list:
                session.add(obj)

            session.commit()
            return True
        except Exception:
            exstr = traceback.format_exc()
            print exstr
            return False

        finally:
            session.close()

    def empty_table(self):
        try:
            session = self._get_session()
            session.query(Lottery_Obj.lo_id).filter(Lottery_Obj.lo_id > 0).delete()
            session.commit()
            return True
        except Exception:
            exstr = traceback.format_exc()
            print exstr
            return False
        finally:
            session.close()

    def analyze(self, list):
        for lo in list:
            self._count_number += 1

            self._result_red[lo.red_0] += 1
            self._result_red[lo.red_1] += 1
            self._result_red[lo.red_2] += 1
            self._result_red[lo.red_3] += 1
            self._result_red[lo.red_4] += 1
            self._result_red[lo.red_5] += 1

            self._result_blue[lo.blue] += 1

    def formate_print(self):

        sorted_red = sorted(self._result_red.items(), key=lambda d: d[1], reverse=True)
        sorted_blue = sorted(self._result_blue.items(), key=lambda d: d[1], reverse=True)

        print self._count_number
        print sorted_red
        print sorted_blue


if __name__ == '__main__':
    # lot = Lottery()
    # dest_path = u'D:\\我的文件\\双色球\\data\\'
    # lot.main_login()
    # lot.get_all_data(dest_path)

    db_user = 'root'
    db_passwd = ''
    db_ip = '192.168.0.201'
    db_name = 'lottery'
    PreHandle.db_init(db_user=db_user, db_passwd=db_passwd, db_ip=db_ip, db_name=db_name)

    data_path = u'D:\\我的文件\\双色球\\data\\'
    ph = PreHandle(data_path)
    ph.empty_table()
    ph.insert_to_db()
    ph.formate_print()
