# coding: utf-8

import json
import time
from esUtil import ES

es = ES()
es.init("192.168.89.132", 9200)


def add_item(index, es_type, item):
    es.index(index, es_type, item)


def get_json():
    path = "c:/temp/es.json"

    with open(path, 'r') as f:
        data = f.read()
    dd = json.loads(data)
    hints = dd['hits']['hits']
    for i, h in enumerate(hints):
        if i != 0 and i % 200 == 0:
            print i
            time.sleep(5)
        item = h['_source']
        index = h['_index']
        es_type = h['_type']
        add_item(index, es_type, item)


def test_add():
    es.index('test', '1', {"aaa": "111"})


if __name__ == '__main__':
    # test_add()
    get_json()
