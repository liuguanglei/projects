from gevent import monkey

monkey.patch_all(thread=False)
#monkey.patch_all()
import gevent
import urllib

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


def send_request(url):
    global total
    total += 1
    resp = urllib.urlopen(url)
    resp.read()
    return resp.getcode()


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
    print "send_mult_gevent"
    import multiprocessing
    size = 30
    pool = multiprocessing.Pool(processes=size)
    print "range"
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
if __name__ == '__main__':
    #urls = ["https://www.liudon.org/1299.html"] * 1000
    # urls = ["https://192.168.10.201/"] * 10000
    # urls = ["http://127.0.0.1:8000/"] * 100
    # urls = ["https://www.baidu.com/"] * 30000
    urls = ["http://s.bistu.edu.cn/was5/web/search?channelid=234439&searchword=1"] * 30000

    # send()
    # send_thread_pool()
    # send_gevent()
    # send_mult_gevent()
    # send_grequest()
    # send_mult_process_thread_pool()
    # send_mult_gevent()

    import timeit

    #print timeit.timeit("send_gevent()", setup="from __main__ import send_gevent", number=1)
    print timeit.timeit("send_mult_gevent()", setup="from __main__ import send_mult_gevent", number=1)
    # print timeit.timeit("send()", setup="from __main__ import send", number=1)
    # print timeit.timeit("send_thread_pool()", setup="from __main__ import send_thread_pool", number=1)
    # print timeit.timeit("send_grequest()", setup="from __main__ import send_grequest", number=1)
    from multiprocessing import Value

    # v = Value('i', 0)
    # print timeit.timeit("send_mult_process_thread_pool()", setup="from __main__ import send_mult_process_thread_pool", number=1)
    # print v.value


    print total
