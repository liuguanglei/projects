from gevent import monkey

monkey.patch_all(thread=False)  # must set thread true
# monkey.patch_all()
import gevent
import urllib
import requests


# print "multiprocessing:"+ str(monkey.is_module_patched("multiprocessing"))
# print monkey.is_module_patched("urllib")

# import grequests


# import datetime
# def elapse(func):
#     def deco(*args, **kwargs):
#         starttime = datetime.datetime.now()
#         func(*args, **kwargs)
#         endtime = datetime.datetime.now()
#         print "elapse time: " + str((endtime - starttime).seconds) + " seconds"
#
#     return deco

# def send_grequest():
#     rs = (grequests.get(u) for u in urls)
#     grequests.map(rs)


def send(_urls=None):
    if _urls:
        pass
    else:
        _urls = urls
    for url in _urls:
        # print send_request(url)
        send_request(url)


def send_thread_pool(_urls=None):
    # print "send_thread_pool"
    if _urls:
        pass
    else:
        _urls = urls
    from threadpool import ThreadPool
    from threadpool import makeRequests
    size = 10
    pool = ThreadPool(size)
    requests_pool = makeRequests(send_request, [([url], None) for url in _urls])
    # requests = makeRequests(send_http_lottery, [([www, req], None) for i in range(number)])
    [pool.putRequest(req) for req in requests_pool]
    pool.wait()
    # pool.dismissWorkers(size, do_join=True)


def send_mult_process():
    pass


def send_request1(url):
    global total, params
    total += 1
    resp = None
    if params:
        params = urllib.urlencode(params)
        resp = urllib.urlopen(url, params)
    else:
        resp = urllib.urlopen(url)
    # res = resp.read()
    # print res
    return resp.getcode()


def send_request(url):
    if params:
        r = requests.post(url, params, verify=False)
    else:
        r = requests.get(url, verify=False)

    print r.status_code


def send_request2(url):
    if json_data and headers:
        r = requests.post(url, data=json_data, verify=False, headers=headers)
        print r.text
    else:
        pass


# @elapse
def send_gevent(_urls=None):
    try:
        # print "send_gevent"
        if _urls:
            pass
        else:
            _urls = urls
        jobs = [gevent.spawn(send_request, url) for url in _urls]
        gevent.joinall(jobs)
        [job.value for job in jobs]
    except:
        pass


def send_mult_gevent():
    import multiprocessing
    size = 30
    pool = multiprocessing.Pool(processes=size)
    _size = (len(urls) / size) + 1
    for i in range(size):
        pool.apply_async(send_gevent, (urls[:_size],))
    pool.close()
    pool.join()


def send_mult_process_thread_pool():
    import multiprocessing

    size = 30
    pool = multiprocessing.Pool(processes=size)
    _size = (len(urls) / size) + 1
    for i in range(size):
        pool.apply_async(send_thread_pool, (urls[:_size],))
        # pool.apply_async(send, (urls[:_size],))
    pool.close()
    pool.join()


total = 0
params = {"username": "bistusdfsdf", "password": "passssdfdwd"}
params = {"fastloginfield": "username", "username": "123", "password": "cb962ac59075b964b07152d234b70",
          "quickforward": "yes", "handlekey": "ls"}

headers = {'content-type': 'application/json',
           'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:22.0) Gecko/20100101 Firefox/22.0'}
json_data = "{Username: '123',Password: '123'}"
params = None
if __name__ == '__main__':
    # urls = ["http://www.bj19zx.cn/site/SiteController.aspx/SignIn"] * 30000
    urls = [
               "http://www.xxr0312.com/search.php?mod=forum&searchid=175&orderby=lastpost&ascdesc=desc&searchsubmit=yes&kw=123"] * 30000
    # urls = ["https://192.168.10.201/"] * 10000
    # urls = ["http://127.0.0.1:8000/"] * 100
    # urls = ["https://www.baidu.com/"] * 30000
    # urls = ["http://opac-lib.bistu.edu.cn:8080/opac/openlink.php?strSearchType=title&match_flag=forward&historyCount=1&strText=123&doctype=ALL&with_ebook=on&displaypg=20&showmode=list&sort=CATA_DATE&orderby=desc&dept=ALL"] * 10000

    # send()
    # send_thread_pool()
    # send_gevent()
    # send_mult_gevent()
    # send_grequest()
    # send_mult_process_thread_pool()
    # send_mult_gevent()

    import timeit

    # print timeit.timeit("send_gevent()", setup="from __main__ import send_gevent", number=1)
    print timeit.timeit("send_mult_gevent()", setup="from __main__ import send_mult_gevent", number=1)
    # print timeit.timeit("send()", setup="from __main__ import send", number=1)
    # print timeit.timeit("send_thread_pool()", setup="from __main__ import send_thread_pool", number=1)
    # print timeit.timeit("send_grequest()", setup="from __main__ import send_grequest", number=1)
    from multiprocessing import Value

    # v = Value('i', 0)
    # print timeit.timeit("send_mult_process_thread_pool()", setup="from __main__ import send_mult_process_thread_pool", number=1)
    # print v.value


    print total
