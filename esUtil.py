# coding: utf-8
import json

from elasticsearch import Elasticsearch
from elasticsearch.helpers import scan
from django.conf import settings


class ES(object):
    '''
    获取ES查询链接，并提供基本查询和统计方法
    '''
    es = None

    def __init__(self):
        if not self.es:
            self.init(settings.ELASTICSEARCH['host'], settings.ELASTICSEARCH['port'])

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
