# coding: utf-8
import json

from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan


class ES(object):
    '''
    获取ES查询链接，并提供基本查询和统计方法
    '''
    es = None

    @staticmethod
    def init(host, port):
        ES.es = Elasticsearch([
            {'host': host, 'port': port},
        ])

    def get(self, index, doc_type, id, fields=[]):
        if fields == []:
            result = self.es.get(index=index, doc_type=doc_type, id=id)
            if result:
                return result['_source']
            else:
                return None
        else:
            result = self.es.get(index=index, doc_type=doc_type, id=id, fields=fields)
            if result:
                return result
            else:
                return None

    def search(self, index, doc_type, body=None, _source=True, _source_exclude=[], _source_include=[],
               analyzer=None, fields=[], sort='', size=10, from_=0, scroll=None, request_timeout=10):
        if not scroll:
            result = self.es.search(index=index, doc_type=doc_type, body=body,
                                    _source_include=_source_include, from_=from_, size=size, sort=sort,
                                    request_timeout=request_timeout)
        else:
            result = scan(self.es, body=body, index=index, doc_type=doc_type,
                          _source_include=_source_include, from_=from_, size=size, sort=sort, scroll=scroll,
                          request_timeout=request_timeout)
        if result:
            return result

    def index(self, index, doc_type, body, op_type='index', request_timeout=10):
        result = self.es.index(index=index, doc_type=doc_type, body=body, op_type=op_type,
                               request_timeout=request_timeout)
        if result:
            return result
        else:
            return None

    def update(self, index, doc_type, id, body):
        re = None
        try:
            re = self.es.get(index=index, doc_type=doc_type, id=id)['_source']
        except:
            return False
        if re:
            for key, value in body.iteritems():
                re[key] = value
            self.es.index(index=index, doc_type=doc_type, id=id, body=re)
            return True
        else:
            return False

    def bulk(self, index, doc_type, body):
        result = self.es.bulk(index=index, doc_type=doc_type, body=body)
        if result:
            return result
        else:
            return None

    def aggs(self, index, doc_type, field, type='terms', _source=False, _source_exclude=[], _source_include=[], size=10,
             request_timeout=10):
        if type == 'terms':
            body = {"aggs": {field + "_terms": {"terms": {"field": field.__str__(), 'size': size.__str__()}}}}
            result = self.es.search(index=index, doc_type=doc_type, body=json.dumps(body), _source=_source,
                                    _source_exclude=_source_exclude,
                                    _source_include=_source_include, request_timeout=request_timeout)
            return json.loads(json.dumps(result))


if __name__ == '__main__':
    es = ES()
    es.init("192.168.20.110", 9200)

    _id1 = "AVjd46X0ZaOtNJpg52mf"
    _id = "AVjd46H-ZaOtNJpg52mc"
    body = {'handleStatus':1, 'handleMsg':'msgmsg'}
    body1 = {'handleStatus':2, 'handleMsg':'msgmsg'}
    print es.update(index='web_events_index_2016.12.08', doc_type='events_doc', id=_id, body=body)
    print es.update(index='web_events_index_2016.12.08', doc_type='events_doc', id=_id1, body=body1)
